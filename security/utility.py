import random
import string
from typing import Annotated
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from pydantic import ValidationError
from config.db import get_db
from security.token import TokenData
from repository.usuario import Usuario as UsuarioRepo
from models.usuario import Usuario
from utils.constants import ESTADO_INACTIVO, SECRET_KEY, ALGORITHM
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"admin": "Acceso administrativo",
            "user": "Acceso usuarios de los clientes",
            "refresh": "Scope para refresh token"})

pwd_context = CryptContext(schemes=["bcrypt"],
                           deprecated="auto",
                           bcrypt__rounds=15)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def generate_password():
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices(caracteres, k=10))


def authenticate_user(username: str,
                      password: str):
    db = next(get_db())
    user = UsuarioRepo.get_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(security_scopes: SecurityScopes,
                           token: Annotated[str, Depends(oauth2_scheme)]):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    db = next(get_db())
    user = UsuarioRepo.get_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: Annotated[Usuario, Security(get_current_user, scopes=["user"])],
):
    if current_user.estado == ESTADO_INACTIVO:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def validate_refresh_token(
        security_scopes: SecurityScopes,
        token: Annotated[str, Depends(oauth2_scheme)]):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    db = next(get_db())
    user = UsuarioRepo.get_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return token_data
