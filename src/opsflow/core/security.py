from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from opsflow.core.config import settings


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Превращает сырой пароль в безопасный хеш для сохранения в БД."""
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Сравнивает введенный пользователем пароль с хешем из БД."""
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(subject: str | Any, expires_delta: timedelta | None = None) -> str:
    """Генерирует подписанный JWT-токен."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"sub": str(subject), "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any] | None:
    """Проверяет подпись и срок действия токена. Возвращает payload или None."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except InvalidTokenError:
        return None