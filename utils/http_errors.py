from fastapi import HTTPException, status

token_invalid = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Access Token invalid",
    headers={"WWW-Authenticate": "Bearer"},
)

no_permissions = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Insufficient permissions",
    headers={"WWW-Authenticate": "Bearer"},
)

incorrect_password = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
)
