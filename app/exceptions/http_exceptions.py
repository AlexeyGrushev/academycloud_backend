from fastapi import HTTPException, status


http_exc_401_unauthorized = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Refused to complete request due to lack of valid authentication.",
    headers={"WWW-Authenticate": "Bearer"},
)

http_exc_401_banned_user = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Current user is deactivated",
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

http_exc_400_long_file_name = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="File name is more than 150 characters"
)

http_exc_400_bad_file_type = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="File type does not exists"
)

http_exc_400_email_confirm = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Your email address is already confirmed"
)

http_exc_403_access_denied = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You don't have permission for this action"
)

http_400_bad_item = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Item is already exists"
)

# Ошибки по добавлению заданий

http_400_file_validation = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The file is not what expect"
)

http_400_json_parse_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Failed to read JSON"
)

http_400_bad_lesson_type = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Lesson type does not exists"
)

http_400_item_not_found = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The specified item was not found"
)

http_400_bad_lesson_name = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Lesson name can't be empty"
)

http_400_bad_lesson_reward = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The reward must be indicated by a integer"
)

http_400_bad_lesson = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Current lesson not found"
)

http_400_bad_answer = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The answer format does not match the required task"
)

# -----------------------------

http_404_score_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="No data was found for this user for the selected time period"
)
