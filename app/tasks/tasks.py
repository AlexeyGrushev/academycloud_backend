import smtplib
from PIL import Image

from app.config.worker import celery
from app.config.app_settings import settings
from app.base.email_utils import preparing_for_email


@celery.task
def send_user_email(user_email: str, template_name: str, **kwargs):
    with smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        msg = preparing_for_email(
            settings.APP_SUBJECT,
            settings.SMTP_LOGIN,
            user_email,
            template_name,
            **kwargs,
        )
        server.login(settings.SMTP_LOGIN, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_LOGIN, user_email, msg=msg.as_string())


@celery.task
def resize_image(
    input_image_path: str,
    output_image_path: str,
    size: tuple
):
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize(size)
    resized_image.save(output_image_path)
