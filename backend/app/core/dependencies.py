from typing import Optional
from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from bson import ObjectId
from ..core.auth import verify_token
from ..db.database import get_database
from ..db.repositories.user_repository import UserRepository
from ..models.user import UserInDB

security = HTTPBearer()

async def get_current_user(
    authorization: Optional[HTTPAuthorizationCredentials] = Depends(security),
    token: Optional[str] = Cookie(None, alias="access_token")
) -> UserInDB:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Try to get token from Authorization header first, then cookie
    token_value = None
    if authorization:
        token_value = authorization.credentials
    elif token:
        token_value = token
    
    if not token_value:
        raise credentials_exception
    
    try:
        payload = verify_token(token_value)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except HTTPException:
        raise credentials_exception
    
    db = get_database()
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_id(ObjectId(user_id))
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_user_optional(
    authorization: Optional[HTTPAuthorizationCredentials] = Depends(security),
    token: Optional[str] = Cookie(None, alias="access_token")
) -> Optional[UserInDB]:
    """Get current user if authenticated, otherwise None"""
    try:
        return await get_current_user(authorization, token)
    except HTTPException:
        return None
