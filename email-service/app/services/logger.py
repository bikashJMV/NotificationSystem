import logging
from supabase import create_client, Client
from app.config import settings

logger = logging.getLogger(__name__)

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def log_email_event(request_id: str, payload: dict, status: str, retry_count: int = 0, dispatched_date: str = None, error: str = None):
    """Log email event to Supabase with full audit trail"""
    try:
        data = {
            "request_id": request_id,
            "event_name": payload['event_name'],
            "recipient_email": payload['primary_recipient']['email'],
            "cc_emails": payload.get('all_admin_emails', []),
            "subject": "Email notification",
            "status": status,
            "retry_count": retry_count,
            "error_details": error,
            "asset_category": payload['asset_data']['category'],
            "asset_model": payload['asset_data']['model_no'],
            "asset_id": payload['asset_data']['asset_id'],
            "dispatched_date": dispatched_date
        }
        supabase.table("email_logs").insert(data).execute()
    except Exception as e:
        logger.error(f"Failed to log email event to Supabase (Request {request_id}): {e}")
