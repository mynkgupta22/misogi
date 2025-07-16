from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.auth import auth_backend, fastapi_users
from app.api.v1.endpoints import documents, integrations
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix=f"{settings.API_V1_STR}/auth/jwt",
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_register_router(),
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_verify_router(),
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_users_router(),
    prefix=f"{settings.API_V1_STR}/users",
    tags=["users"]
)

# API routes
app.include_router(
    documents.router,
    prefix=f"{settings.API_V1_STR}",
    tags=["documents"]
)

app.include_router(
    integrations.router,
    prefix=f"{settings.API_V1_STR}",
    tags=["integrations"]
)

@app.get("/")
async def root():
    return {"message": "Welcome to Research Assistant API"} 
    return {"message": "Welcome to Multimodal Research Assistant API"} 