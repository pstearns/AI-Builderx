from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import HTTPBearer
from ..core.auth import create_access_token, verify_password
from ..core.dependencies import get_current_user
from ..core.settings import get_settings
from ..db.database import get_database
from ..db.repositories.user_repository import UserRepository
from ..models.user import User, UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()

@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, response: Response):
    """Create a new user account"""
    db = get_database()
    user_repo = UserRepository(db)
    
    # Check if user already exists
    existing_user = await user_repo.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    created_user = await user_repo.create_user(user)
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(created_user.id)}, expires_delta=access_token_expires
    )
    
    # Set HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.JWT_EXPIRE_MINUTES * 60
    )
    
    return User(**created_user.dict())

@router.post("/login", response_model=User)
async def login(user_credentials: UserLogin, response: Response):
    """Login user and return access token"""
    db = get_database()
    user_repo = UserRepository(db)
    
    # Authenticate user
    user = await user_repo.authenticate_user(user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    # Set HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.JWT_EXPIRE_MINUTES * 60
    )
    
    return User(**user.dict())

@router.post("/logout")
async def logout(response: Response):
    """Logout user by clearing the access token cookie"""
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user
