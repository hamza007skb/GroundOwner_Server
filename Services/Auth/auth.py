from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status
from .auth_credentials import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        print(f"Token being verified: {token}")  # Debugging
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded payload: {payload}")  # Debugging
        email: str = payload.get("email")
        if email is None:
            print("Email not found in token")
            raise credentials_exception
        return email
    except JWTError as e:
        print(f"JWT Error: {e}")  # Debugging
        raise credentials_exception



def get_current_user(token: str = Depends(oauth2_scheme)):
    print(f"Token received in get_current_user: {token}")  # Debugging
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_email = verify_token(token, credentials_exception)
    print(f"Email from token: {user_email}")  # Debugging
    return user_email


