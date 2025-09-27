import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from bson import ObjectId
import sys
import os

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app
from app.core.auth import verify_password, get_password_hash, create_access_token
from app.models.user import UserCreate, UserLogin

client = TestClient(app)

class TestAuth:
    """Test authentication functionality"""
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert verify_password(password, hashed)
        assert not verify_password("wrongpassword", hashed)
    
    def test_jwt_token_creation(self):
        """Test JWT token creation and verification"""
        user_id = str(ObjectId())
        token = create_access_token(data={"sub": user_id})
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    @patch('app.api.auth.UserRepository')
    async def test_signup_success(self, mock_user_repo):
        """Test successful user signup"""
        mock_repo_instance = AsyncMock()
        mock_user_repo.return_value = mock_repo_instance
        
        # Mock user creation
        mock_user = AsyncMock()
        mock_user.id = ObjectId()
        mock_user.email = "test@example.com"
        mock_user.name = "Test User"
        mock_user.dict.return_value = {
            "id": mock_user.id,
            "email": "test@example.com", 
            "name": "Test User"
        }
        mock_repo_instance.get_user_by_email.return_value = None
        mock_repo_instance.create_user.return_value = mock_user
        
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "name": "Test User"
        }
        
        response = client.post("/auth/signup", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"
        assert "id" in data
    
    @patch('app.api.auth.UserRepository')
    async def test_signup_duplicate_email(self, mock_user_repo):
        """Test signup with duplicate email"""
        mock_repo_instance = AsyncMock()
        mock_user_repo.return_value = mock_repo_instance
        
        # Mock existing user
        mock_existing_user = AsyncMock()
        mock_repo_instance.get_user_by_email.return_value = mock_existing_user
        
        user_data = {
            "email": "existing@example.com",
            "password": "testpassword123",
            "name": "Test User"
        }
        
        response = client.post("/auth/signup", json=user_data)
        
        assert response.status_code == 400
        assert "already registered" in response.json()["error"]["message"]
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["error"]["message"]
    
    def test_logout(self):
        """Test logout functionality"""
        response = client.post("/auth/logout")
        
        assert response.status_code == 200
        assert response.json()["message"] == "Successfully logged out"

class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_healthz(self):
        """Test health check endpoint"""
        response = client.get("/healthz")
        
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
