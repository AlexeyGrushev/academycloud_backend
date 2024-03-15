from fastapi import HTTPException, status


http_exc_401_unauthorized = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Refused to complete request due to lack of valid authentication.",
    headers={"WWW-Authenticate": "Bearer"},
)

http_exc_400_bad_email = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="This email is already occupied. Try to use another one.",
)

http_exc_400_bad_login = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="This login is already occupied. Come up with another one.",
)

http_exc_400_bad_data = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The user is not found,"
    " check the correctness of the email and password",
)
