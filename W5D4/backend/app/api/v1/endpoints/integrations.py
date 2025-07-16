from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import aiohttp
from docx import Document as DocxDocument
from fpdf import FPDF
import markdown

from app.core.auth import fastapi_users
from app.models.user import User
from app.models.document import Document
from app.db.session import get_async_session
from app.core.config import settings

router = APIRouter()

current_active_user = fastapi_users.current_user(active=True)

async def get_document_or_404(
    document_id: int,
    user: User,
    session: AsyncSession
) -> Document:
    query = select(Document).where(
        Document.id == document_id,
        Document.owner_id == user.id
    )
    result = await session.execute(query)
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return document

@router.get("/documents/{document_id}/export")
async def export_document(
    document_id: int,
    format: str = Query(..., regex="^(pdf|docx|md)$"),
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Export document in various formats"""
    document = await get_document_or_404(document_id, user, session)
    
    if format == "pdf":
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=document.content)
        return Response(
            pdf.output(dest="S").encode("latin1"),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={document.title}.pdf"}
        )
    
    elif format == "docx":
        doc = DocxDocument()
        doc.add_paragraph(document.content)
        return Response(
            doc.save("memory"),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={document.title}.docx"}
        )
    
    else:  # markdown
        return Response(
            document.content,
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename={document.title}.md"}
        )

@router.post("/documents/{document_id}/share")
async def share_document(
    document_id: int,
    platform: str = Query(..., regex="^(notion|slack|teams)$"),
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Share document to various platforms"""
    document = await get_document_or_404(document_id, user, session)
    
    if platform == "notion":
        # Notion API integration
        async with aiohttp.ClientSession() as client:
            headers = {
                "Authorization": f"Bearer {settings.NOTION_TOKEN}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28"
            }
            data = {
                "parent": {"database_id": settings.NOTION_DATABASE_ID},
                "properties": {
                    "Name": {"title": [{"text": {"content": document.title}}]},
                    "Content": {"rich_text": [{"text": {"content": document.content}}]}
                }
            }
            async with client.post(
                "https://api.notion.com/v1/pages",
                headers=headers,
                json=data
            ) as response:
                if response.status != 200:
                    raise HTTPException(status_code=500, detail="Failed to share to Notion")
    
    elif platform == "slack":
        # Slack API integration
        async with aiohttp.ClientSession() as client:
            data = {
                "channel": settings.SLACK_CHANNEL_ID,
                "text": f"*{document.title}*\n\n{document.content}"
            }
            async with client.post(
                "https://slack.com/api/chat.postMessage",
                headers={"Authorization": f"Bearer {settings.SLACK_TOKEN}"},
                json=data
            ) as response:
                if response.status != 200:
                    raise HTTPException(status_code=500, detail="Failed to share to Slack")
    
    elif platform == "teams":
        # Microsoft Teams API integration
        async with aiohttp.ClientSession() as client:
            data = {
                "text": f"**{document.title}**\n\n{document.content}"
            }
            async with client.post(
                settings.TEAMS_WEBHOOK_URL,
                json=data
            ) as response:
                if response.status != 200:
                    raise HTTPException(status_code=500, detail="Failed to share to Teams")
    
    return {"message": f"Successfully shared to {platform}"} 