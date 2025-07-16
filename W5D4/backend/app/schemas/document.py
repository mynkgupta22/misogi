from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class DocumentBase(BaseModel):
    title: str
    file_type: str
    metadata: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(DocumentBase):
    title: Optional[str] = None
    file_type: Optional[str] = None

class DocumentResponse(DocumentBase):
    id: int
    file_path: str
    created_at: datetime
    updated_at: datetime
    owner_id: int

    class Config:
        from_attributes = True

class QueryHistoryBase(BaseModel):
    query: str
    response: str

class QueryHistoryCreate(QueryHistoryBase):
    pass

class QueryHistoryResponse(QueryHistoryBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True 