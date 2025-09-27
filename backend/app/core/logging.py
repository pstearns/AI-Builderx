import logging
import sys
from typing import Any, Dict
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)

logger = logging.getLogger(__name__)

def log_request(request: Request, response_data: Any = None):
    """Log HTTP request details"""
    logger.info(
        f"Request: {request.method} {request.url.path} - "
        f"Client: {request.client.host if request.client else 'unknown'} - "
        f"Status: {getattr(response_data, 'status_code', 'N/A')}"
    )

def log_error(error: Exception, context: str = ""):
    """Log error with context"""
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)

def create_error_response(status_code: int, detail: str, error_code: str = None) -> Dict[str, Any]:
    """Create standardized error response"""
    error_response = {
        "error": {
            "code": error_code or f"HTTP_{status_code}",
            "message": detail
        }
    }
    return error_response

async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with structured logging"""
    log_error(exc, f"HTTP Exception: {request.method} {request.url.path}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content=create_error_response(exc.status_code, exc.detail)
    )

async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handle Pydantic validation errors"""
    log_error(exc, f"Validation Error: {request.method} {request.url.path}")
    
    return JSONResponse(
        status_code=422,
        content=create_error_response(422, "Validation error", "VALIDATION_ERROR")
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    log_error(exc, f"General Exception: {request.method} {request.url.path}")
    
    return JSONResponse(
        status_code=500,
        content=create_error_response(500, "Internal server error", "INTERNAL_ERROR")
    )
