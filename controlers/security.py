from datetime import timedelta
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, Security, status
from fastapi.security import OAuth2PasswordRequestForm

from security.token import Token, User
from security.utility import authenticate_user, create_access_token, get_current_active_user
from utils.constants import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(tags=["seguridad"])


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password) #modificar la autenticacion para hacerlo por bd
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": user.rol.scopes}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")