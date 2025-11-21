from fastapi import HTTPException, status
from typing import Any, Optional, Dict


# Base custom exception class
class BaseCustomException(HTTPException):
    """Base exception class with additional metadata support"""
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code
        self.metadata = metadata or {}


# Authentication & Authorization Exceptions
class AuthenticationError(BaseCustomException):
    def __init__(self, detail: str = "Authentication failed", error_code: str = "AUTH_FAILED"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
            error_code=error_code
        )


class TokenExpiredError(BaseCustomException):
    def __init__(self, detail: str = "Token has expired"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="TOKEN_EXPIRED"
        )


class InvalidTokenError(BaseCustomException):
    def __init__(self, detail: str = "Invalid token"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="INVALID_TOKEN"
        )


class PermissionError(BaseCustomException):
    def __init__(self, detail: str = "Insufficient permissions", error_code: str = "PERMISSION_DENIED"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code=error_code
        )


# Resource Exceptions
class NotFoundError(BaseCustomException):
    def __init__(self, detail: str = "Resource not found", resource_type: Optional[str] = None):
        error_code = f"{resource_type.upper()}_NOT_FOUND" if resource_type else "NOT_FOUND"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code=error_code
        )


class AlreadyExistsError(BaseCustomException):
    def __init__(self, detail: str = "Resource already exists", resource_type: Optional[str] = None):
        error_code = f"{resource_type.upper()}_ALREADY_EXISTS" if resource_type else "ALREADY_EXISTS"
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code=error_code
        )


# Validation Exceptions
class ValidationError(BaseCustomException):
    def __init__(self, detail: str = "Validation error", field: Optional[str] = None):
        metadata = {"field": field} if field else {}
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="VALIDATION_ERROR",
            metadata=metadata
        )


class InvalidInputError(BaseCustomException):
    def __init__(self, detail: str = "Invalid input provided"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="INVALID_INPUT"
        )


# Database Exceptions
class DatabaseError(BaseCustomException):
    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="DATABASE_ERROR"
        )


class DatabaseConnectionError(BaseCustomException):
    def __init__(self, detail: str = "Database connection failed"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
            error_code="DB_CONNECTION_ERROR"
        )


# Business Logic Exceptions
class BusinessLogicError(BaseCustomException):
    def __init__(self, detail: str = "Business logic error", error_code: str = "BUSINESS_ERROR"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code=error_code
        )


# File & Upload Exceptions
class FileUploadError(BaseCustomException):
    def __init__(self, detail: str = "File upload failed"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="FILE_UPLOAD_ERROR"
        )


class FileNotFoundError(NotFoundError):
    def __init__(self, detail: str = "File not found", filename: Optional[str] = None):
        super().__init__(detail=detail, resource_type="file")
        if filename:
            self.metadata["filename"] = filename


class InvalidFileTypeError(BaseCustomException):
    def __init__(self, detail: str = "Invalid file type", allowed_types: Optional[list] = None):
        metadata = {"allowed_types": allowed_types} if allowed_types else {}
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="INVALID_FILE_TYPE",
            metadata=metadata
        )


# Rate Limiting & Quota Exceptions
class RateLimitExceededError(BaseCustomException):
    def __init__(self, detail: str = "Rate limit exceeded", retry_after: Optional[int] = None):
        headers = {"Retry-After": str(retry_after)} if retry_after else None
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            headers=headers,
            error_code="RATE_LIMIT_EXCEEDED"
        )


class QuotaExceededError(BaseCustomException):
    def __init__(self, detail: str = "Quota exceeded"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            error_code="QUOTA_EXCEEDED"
        )


# External Service Exceptions
class ExternalServiceError(BaseCustomException):
    def __init__(self, detail: str = "External service error", service_name: Optional[str] = None):
        metadata = {"service": service_name} if service_name else {}
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=detail,
            error_code="EXTERNAL_SERVICE_ERROR",
            metadata=metadata
        )


class ServiceUnavailableError(BaseCustomException):
    def __init__(self, detail: str = "Service temporarily unavailable"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
            error_code="SERVICE_UNAVAILABLE"
        )
