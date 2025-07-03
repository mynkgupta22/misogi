from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
import uuid
from ..models.user import UserCreate, User, Token
from ..utils.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_users,
    save_users,
    verify_token
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register", response_model=User)
async def register(user: UserCreate):
    users_data = get_users()
    
    # Check if email already exists
    if any(u["email"] == user.email for u in users_data["users"].values()):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    user_id = str(uuid.uuid4())
    user_dict = {
        "id": user_id,
        "email": user.email,
        "username": user.username,
        "hashed_password": get_password_hash(user.password),
        "interactions": {
            "viewed": [],
            "liked": [],
            "purchased": []
        }
    }
    
    users_data["users"][user_id] = user_dict
    save_users(users_data)
    
    return User(**{k: v for k, v in user_dict.items() if k != "hashed_password"})

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    users_data = get_users()
    
    # Find user by email
    user = next(
        (u for u in users_data["users"].values() if u["email"] == form_data.username),
        None
    )
    
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception
    
    users_data = get_users()
    user = next(
        (u for u in users_data["users"].values() if u["email"] == token_data.email),
        None
    )
    
    if user is None:
        raise credentials_exception
    
    return User(**{k: v for k, v in user.items() if k != "hashed_password"}) 