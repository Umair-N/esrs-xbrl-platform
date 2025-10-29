import re
from typing import Optional, List
from datetime import datetime, timedelta


def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username: str) -> bool:
    # Username should be 3-30 characters, alphanumeric and underscores only
    pattern = r'^[a-zA-Z0-9_]{3,30}$'
    return re.match(pattern, username) is not None

def validate_password(
    password: str,
    user_id: Optional[str] = None,
    personal_info: Optional[List[str]] = None,
    previous_passwords: Optional[List[str]] = None,
    last_password_change: Optional[datetime] = None
) -> tuple[bool, Optional[str]]:
    """
    Validate password strength based on comprehensive security requirements.
    
    Args:
        password: The password to validate
        user_id: User's ID to check if password matches username
        personal_info: List of personal information (birthdays, names, addresses, phone numbers)
        previous_passwords: List of previous password hashes to check against (last 3)
        last_password_change: Date of last password change to check expiration
    
    Returns: (is_valid, error_message)
    """
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
        return False, "Password must contain at least one special character"
    
    if user_id and password.lower() == user_id.lower():
        return False, "Password must not be identical to user ID"
    
    if personal_info:
        password_lower = password.lower()
        for info in personal_info:
            if info and len(info) >= 3:  
                if info.lower() in password_lower:
                    return False, "Password must not contain personal information (names, birthdays, addresses, phone numbers)"
    
    common_passwords = [
        'password', '12345678', 'qwerty', 'abc123', 'monkey',
        'letmein', 'trustno1', 'dragon', 'baseball', 'iloveyou',
        'master', 'sunshine', 'ashley', 'bailey', 'shadow',
        'superman', 'password1', 'welcome', 'admin', 'login'
    ]
    if password.lower() in common_passwords:
        return False, "Password is too common and easily guessable"
    
    if re.match(r'^(.)\1+$', password): 
        return False, "Password must not be a simple pattern"
    
    if re.match(r'^(012345|123456|234567|345678|456789|567890)', password):
        return False, "Password must not contain sequential patterns"
    
    if re.match(r'^(abcdef|bcdefg|cdefgh|defghi)', password, re.IGNORECASE):
        return False, "Password must not contain sequential patterns"
    
    if previous_passwords:

        if password in previous_passwords[-3:]:
            return False, "Password must differ from your previous 3 passwords"
    
    if last_password_change:
        expiration_date = last_password_change + timedelta(days=365)
        if datetime.now() > expiration_date:
            return False, "Password has expired. Passwords must be changed every year"
    
    return True, None

def sanitize_filename(filename: str) -> str:
    """Remove or replace unsafe characters in filename"""
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = filename.strip(' .')
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:250] + ('.' + ext if ext else '')
    
    return filename
