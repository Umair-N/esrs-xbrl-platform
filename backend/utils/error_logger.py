"""
Enhanced error logging utilities for the application.
Provides structured logging for errors with additional context.
"""

import logging
import traceback
import sys
from typing import Optional, Dict, Any
from datetime import datetime
from functools import wraps

logger = logging.getLogger(__name__)


class ErrorLogger:
    """Centralized error logging with structured context"""

    @staticmethod
    def log_error(
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
        severity: str = "error",
    ) -> None:
        """
        Log an error with structured context.

        Args:
            error: The exception to log
            context: Additional context information
            user_id: User ID if available
            request_id: Request ID for tracking
            severity: Log severity level (debug, info, warning, error, critical)
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
        }

        if context:
            log_data["context"] = context

        if user_id:
            log_data["user_id"] = user_id

        if request_id:
            log_data["request_id"] = request_id

        log_method = getattr(logger, severity.lower(), logger.error)
        log_method(
            f"{type(error).__name__}: {str(error)}",
            extra=log_data,
            exc_info=error,
        )

    @staticmethod
    def log_database_error(
        error: Exception,
        operation: str,
        table: Optional[str] = None,
        query: Optional[str] = None,
        request_id: Optional[str] = None,
    ) -> None:
        """
        Log database-specific errors with operation context.

        Args:
            error: The database exception
            operation: The database operation being performed
            table: The table involved
            query: The query that failed (if applicable)
            request_id: Request ID for tracking
        """
        context = {"operation": operation}

        if table:
            context["table"] = table

        if query:
            # Sanitize query to remove sensitive data
            context["query"] = query[:200]  # Limit query length in logs

        ErrorLogger.log_error(
            error=error,
            context=context,
            request_id=request_id,
            severity="error",
        )

    @staticmethod
    def log_validation_error(
        error: Exception,
        field: Optional[str] = None,
        value: Optional[Any] = None,
        request_id: Optional[str] = None,
    ) -> None:
        """
        Log validation errors with field context.

        Args:
            error: The validation exception
            field: The field that failed validation
            value: The invalid value (be careful with sensitive data)
            request_id: Request ID for tracking
        """
        context = {}

        if field:
            context["field"] = field

        if value is not None:
            # Don't log sensitive values like passwords
            if field and any(sensitive in field.lower() for sensitive in ["password", "token", "secret", "key"]):
                context["value"] = "[REDACTED]"
            else:
                context["value"] = str(value)[:100]  # Limit value length

        ErrorLogger.log_error(
            error=error,
            context=context,
            request_id=request_id,
            severity="warning",
        )

    @staticmethod
    def log_api_error(
        error: Exception,
        endpoint: str,
        method: str,
        status_code: Optional[int] = None,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
    ) -> None:
        """
        Log API endpoint errors.

        Args:
            error: The exception
            endpoint: The API endpoint
            method: HTTP method
            status_code: HTTP status code
            user_id: User ID if available
            request_id: Request ID for tracking
        """
        context = {
            "endpoint": endpoint,
            "method": method,
        }

        if status_code:
            context["status_code"] = status_code

        ErrorLogger.log_error(
            error=error,
            context=context,
            user_id=user_id,
            request_id=request_id,
            severity="error",
        )

    @staticmethod
    def log_external_service_error(
        error: Exception,
        service_name: str,
        operation: str,
        request_id: Optional[str] = None,
    ) -> None:
        """
        Log errors from external service calls.

        Args:
            error: The exception
            service_name: Name of the external service
            operation: The operation being performed
            request_id: Request ID for tracking
        """
        context = {
            "service": service_name,
            "operation": operation,
        }

        ErrorLogger.log_error(
            error=error,
            context=context,
            request_id=request_id,
            severity="error",
        )


def log_exceptions(
    logger_func: Optional[callable] = None,
    reraise: bool = True,
    default_return: Any = None,
):
    """
    Decorator to automatically log exceptions in functions.

    Args:
        logger_func: Custom logging function (defaults to ErrorLogger.log_error)
        reraise: Whether to reraise the exception after logging
        default_return: Value to return if exception is caught and not reraised

    Example:
        @log_exceptions()
        def risky_operation():
            # code that might fail
            pass

        @log_exceptions(reraise=False, default_return=[])
        def get_users():
            # returns [] on error instead of raising
            pass
    """

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                log_func = logger_func or ErrorLogger.log_error
                context = {
                    "function": func.__name__,
                    "module": func.__module__,
                }
                log_func(error=e, context=context)

                if reraise:
                    raise
                return default_return

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log_func = logger_func or ErrorLogger.log_error
                context = {
                    "function": func.__name__,
                    "module": func.__module__,
                }
                log_func(error=e, context=context)

                if reraise:
                    raise
                return default_return

        # Return appropriate wrapper based on function type
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator


def get_error_details(error: Exception) -> Dict[str, Any]:
    """
    Extract detailed information from an exception.

    Args:
        error: The exception to analyze

    Returns:
        Dictionary with error details
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()

    details = {
        "type": type(error).__name__,
        "message": str(error),
        "module": getattr(error, "__module__", None),
    }

    if exc_traceback:
        tb_list = traceback.extract_tb(exc_traceback)
        if tb_list:
            last_frame = tb_list[-1]
            details["file"] = last_frame.filename
            details["line"] = last_frame.lineno
            details["function"] = last_frame.name

    return details


def format_error_for_logging(
    error: Exception,
    include_traceback: bool = True,
) -> str:
    """
    Format an error for logging with consistent structure.

    Args:
        error: The exception to format
        include_traceback: Whether to include full traceback

    Returns:
        Formatted error string
    """
    details = get_error_details(error)

    formatted = f"[{details['type']}] {details['message']}"

    if details.get("file") and details.get("line"):
        formatted += f" (at {details['file']}:{details['line']})"

    if include_traceback:
        formatted += f"\n{traceback.format_exc()}"

    return formatted
