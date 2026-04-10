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

async def send_event_email(
    recipient: str, 
    subject: str, 
    template_name: str, 
    template_data: dict,
    cc: list[str] | str | None = None
):
    """
    Send an templated email using fastapi-mail background capabilities
    """
    final_ccs = []
    
    # Add default CC if configured
    if settings.MAIL_DEFAULT_CC:
        final_ccs.append(settings.MAIL_DEFAULT_CC)
        
    # Add requested CCs
    if cc:
        if isinstance(cc, str):
            final_ccs.append(cc)
        else:
            final_ccs.extend(cc)

    message = MessageSchema(
        subject=subject,
        recipients=[recipient],
        cc=final_ccs if final_ccs else None,
        template_body=template_data,
        subtype=MessageType.html
    )
    
    await fm.send_message(message, template_name=template_name)
