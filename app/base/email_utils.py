from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.auth.utils import create_access_token
from app.base.templates import render_template
from app.config.app_settings import settings


def create_url_for_confirm(user_id: str):
    token = create_access_token(
        {"sub": user_id}, settings.SMTP_TOKEN_EXPIRE_DAYS)
    url = f"{settings.APP_BASE_URL}{
        settings.APP_PREFIX}/auth/confirm_email/{token}"
    return url


def create_url_for_restore(user_id: str):
    token = create_access_token(
        {"sub": user_id}, settings.SMTP_TOKEN_EXPIRE_DAYS)
    url = f"{settings.APP_BASE_URL}{
        settings.APP_PREFIX}/auth/restore_password/{token}"
    return url


def preparing_for_email(
    subject: str,
    by: str,
    to: str,
    template_name: str,
    **kwargs,
) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = by
    msg["To"] = to
    html = render_template(
        template_name,
        **kwargs,
    )
    part = MIMEText(html, "html")
    msg.attach(part)

    return msg
