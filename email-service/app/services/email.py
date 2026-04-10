from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.core.config import settings

TEMPLATE_FOLDER = Path(__file__).parent.parent / "templates"

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=TEMPLATE_FOLDER
)

fm = FastMail(conf)

async def send_event_email(recipient: str, subject: str, template_name: str, template_data: dict):
    """
    Send an templated email using fastapi-mail background capabilities
    """
    message = MessageSchema(
        subject=subject,
        recipients=[recipient],
        template_body=template_data,
        subtype=MessageType.html
    )
    
    await fm.send_message(message, template_name=template_name)
