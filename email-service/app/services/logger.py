import logging
from supabase import create_client, Client
from app.core.config import settings

logger = logging.getLogger(__name__)

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def log_email_event(event_name: str, recipient: str, subject: str, status: str, error_details: str = None):
    """
    Log the email event sync (to insert via Fastapi Background Tasks)
    """
    try:
        data = {
            "event_name": event_name,
            "recipient_email": recipient,
            "subject": subject,
            "status": status,
            "error_details": error_details
        }
        supabase.table("email_logs").insert(data).execute()
    except Exception as e:
        logger.error(f"Failed to log email event to Supabase: {e}")
