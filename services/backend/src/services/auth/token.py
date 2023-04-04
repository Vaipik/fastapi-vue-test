from datetime import datetime, timedelta
from typing import Optional
import os

from jose import jwt


def create_access_token(data: dict, expires_in_seconds: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_in_seconds is None:
        expire = datetime.utcnow() + timedelta(
            seconds=float(os.environ.get("JWT_ACCESS_TOKEN_EXPIRE"))
        )
    else:
        expire = datetime.utcnow() + expires_in_seconds

    to_encode.update({
        "exp": expire
    })
    encoded_jwt = jwt.encode(
        to_encode,
        key=os.environ.get("SECRET_KEY"),
        algorithm=os.environ.get("JWT_ALGORITHM")
    )
    return encoded_jwt

