import os
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union
from jose import jwt

SECRET_KEY = os.environ.get(
    "SIGNING_SECRET", "08b77b8a2e95ea79315d5102607497d19994181dacc5a5131e470f72dc505bb8"
)
ALGORITHM = os.environ.get("SIGNING_ALGORITHM", "HS256")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    try:
        return jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
    except:
        return False
