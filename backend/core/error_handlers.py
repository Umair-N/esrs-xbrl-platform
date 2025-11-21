"""
Global error handlers for the FastAPI application.
These handlers catch exceptions and return standardized error responses.
"""

import logging
import traceback
from typing import Union
from datetime import datetime

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError as PydanticValidationError
from sqlalchemy.exc import (
    SQLAlchemyError,
    IntegrityError,
    OperationalError,
    DatabaseError as SQLDatabaseError,
)
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.exceptions import (
    BaseCustomException,
    DatabaseError,
    DatabaseConnectionError,
    AlreadyExistsError,
)

logger = logging.getLogger(__name__)


def create_error_response(
    status_code: int,
    detail: str,
    error_code: str = None,
    metadata: dict = None,
    request_id: str = None,
    path: str = None,
) -> JSONResponse:
    """
    Create a standardized error response.

    Args:
        status_code: HTTP status code
        detail: Error message
        error_code: Custom error code for client-side handling
        metadata: Additional error metadata
        request_id: Request ID for tracking
        path: Request path where error occurred

    Returns:
        JSONResponse with standardized error format
    """
    error_response = {
        "error": {
            "status_code": status_code,
            "message": detail,
            "timestamp": datetime.utcnow().isoformat(),
        }
    }

    if error_code:
        error_response["error"]["code"] = error_code

    if metadata:
        error_response["error"]["metadata"] = metadata

    if request_id:
        error_response["error"]["request_id"] = request_id

    if path:
        error_response["error"]["path"] = path

    return JSONResponse(
        status_code=status_code,
        content=error_response,
    )


async def custom_exception_handler(
    request: Request,
    exc: BaseCustomException
) -> JSONResponse:
    """
    Handler for custom application exceptions.

    Args:
        request: The incoming request
        exc: The custom exception

    Returns:
        JSONResponse with error details
    """
    request_id = getattr(request.state, "request_id", None)

    logger.warning(
        f"Custom exception: {exc.error_code or 'UNKNOWN'} - {exc.detail}",
        extra={
            "error_code": exc.error_code,
            "status_code": exc.status_code,
            "path": request.url.path,
            "method": request.method,
            "request_id": request_id,
        }
    )

    return create_error_response(
        status_code=exc.status_code,
        detail=exc.detail,
        error_code=exc.error_code,
        metadata=exc.metadata,
        request_id=request_id,
        path=request.url.path,
    )


async def http_exception_handler(
    request: Request,
    exc: Union[StarletteHTTPException, Exception]
) -> JSONResponse:
    """
    Handler for standard HTTP exceptions.

    Args:
        request: The incoming request
        exc: The HTTP exception

    Returns:
        JSONResponse with error details
    """
    request_id = getattr(request.state, "request_id", None)

    logger.warning(
        f"HTTP exception: {exc.status_code} - {exc.detail}",
        extra={
            "status_code": exc.status_code,
            "path": request.url.path,
            "method": request.method,
            "request_id": request_id,
        }
    )

    return create_error_response(
        status_code=exc.status_code,
        detail=exc.detail,
        error_code="HTTP_ERROR",
        request_id=request_id,
        path=request.url.path,
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """
    Handler for request validation errors (Pydantic validation).

    Args:
        request: The incoming request
        exc: The validation error

    Returns:
        JSONResponse with validation error details
    """
    request_id = getattr(request.state, "request_id", None)

    errors = []
    for error in exc.errors():
        error_detail = {
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        }
        errors.append(error_detail)

    logger.warning(
        f"Validation error on {request.method} {request.url.path}",
        extra={
            "errors": errors,
            "path": request.url.path,
            "method": request.method,
            "request_id": request_id,
        }
    )

    return create_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Validation error",
        error_code="VALIDATION_ERROR",
        metadata={"errors": errors},
        request_id=request_id,
        path=request.url.path,
    )


async def sqlalchemy_exception_handler(
    request: Request,
    exc: SQLAlchemyError
) -> JSONResponse:
    """
    Handler for SQLAlchemy database errors.

    Args:
        request: The incoming request
        exc: The SQLAlchemy exception

    Returns:
        JSONResponse with database error details
    """
    request_id = getattr(request.state, "request_id", None)

    # Log the full error for debugging
    logger.error(
        f"Database error on {request.method} {request.url.path}: {str(exc)}",
        exc_info=exc,
        extra={
            "path": request.url.path,
            "method": request.method,
            "request_id": request_id,
        }
    )

    # Handle specific database errors
    if isinstance(exc, IntegrityError):
        # Integrity constraint violation (e.g., unique constraint, foreign key)
        detail = "Data integrity error: The operation violates database constraints"
        error_code = "INTEGRITY_ERROR"
        status_code = status.HTTP_409_CONFLICT
    elif isinstance(exc, OperationalError):
        # Database operational errors (connection issues, etc.)
        detail = "Database operation failed: Please try again later"
        error_code = "DB_OPERATIONAL_ERROR"
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        # Generic database error
        detail = "Database error occurred"
        error_code = "DATABASE_ERROR"
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return create_error_response(
        status_code=status_code,
        detail=detail,
        error_code=error_code,
        request_id=request_id,
        path=request.url.path,
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """
    Handler for all unhandled exceptions.
    This is the catch-all handler for any exceptions not caught by other handlers.

    Args:
        request: The incoming request
        exc: The unhandled exception

    Returns:
        JSONResponse with generic error message
    """
    request_id = getattr(request.state, "request_id", None)

    # Log the full traceback for debugging
    logger.error(
        f"Unhandled exception on {request.method} {request.url.path}",
        exc_info=exc,
        extra={
            "exception_type": type(exc).__name__,
            "path": request.url.path,
            "method": request.method,
            "request_id": request_id,
            "traceback": traceback.format_exc(),
        }
    )

    # Don't expose internal error details in production
    detail = "An unexpected error occurred. Please try again later."

    return create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=detail,
        error_code="INTERNAL_SERVER_ERROR",
        request_id=request_id,
        path=request.url.path,
    )


async def value_error_handler(
    request: Request,
    exc: ValueError
) -> JSONResponse:
    """
    Handler for ValueError exceptions.

    Args:
        request: The incoming request
        exc: The ValueError exception

    Returns:
        JSONResponse with error details
    """
    request_id = getattr(request.state, "request_id", None)

    logger.warning(
        f"ValueError on {request.method} {request.url.path}: {str(exc)}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "request_id": request_id,
        }
    )

    return create_error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
        error_code="VALUE_ERROR",
        request_id=request_id,
        path=request.url.path,
    )


async def type_error_handler(
    request: Request,
    exc: TypeError
) -> JSONResponse:
    """
    Handler for TypeError exceptions.

    Args:
        request: The incoming request
        exc: The TypeError exception

    Returns:
        JSONResponse with error details
    """
    request_id = getattr(request.state, "request_id", None)

    logger.error(
        f"TypeError on {request.method} {request.url.path}: {str(exc)}",
        exc_info=exc,
        extra={
            "path": request.url.path,
            "method": request.method,
            "request_id": request_id,
        }
    )

    return create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="A type error occurred while processing your request",
        error_code="TYPE_ERROR",
        request_id=request_id,
        path=request.url.path,
    )


async def key_error_handler(
    request: Request,
    exc: KeyError
) -> JSONResponse:
    """
    Handler for KeyError exceptions.

    Args:
        request: The incoming request
        exc: The KeyError exception

    Returns:
        JSONResponse with error details
    """
    request_id = getattr(request.state, "request_id", None)

    logger.error(
        f"KeyError on {request.method} {request.url.path}: {str(exc)}",
        exc_info=exc,
        extra={
            "path": request.url.path,
            "method": request.method,
            "request_id": request_id,
        }
    )

    return create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="A required key was not found",
        error_code="KEY_ERROR",
        request_id=request_id,
        path=request.url.path,
    )
