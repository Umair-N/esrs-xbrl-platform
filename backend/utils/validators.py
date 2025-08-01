from fastapi import HTTPException, status
from utils.helpers import validate_email, validate_password, validate_username


def validate_user_input(email: str, username: str, password: str):
    """Validate user registration input"""

    if not validate_email(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format"
        )

    if not validate_username(username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be 3-30 characters, alphanumeric and underscores only",
        )

    is_valid, error_msg = validate_password(password)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)
