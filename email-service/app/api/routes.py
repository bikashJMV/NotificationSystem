import logging
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from app.schemas.email import EventPayload
from app.services.email import send_event_email
from app.services.logger import log_email_event
from app.core.security import verify_api_key

logger = logging.getLogger(__name__)
router = APIRouter()

EVENT_MAP = {
    "user.created": {
        "template": "welcome.html",
        "subject": "Welcome to NotificationSystem!"
    },
    "asset.assigned": {
        "template": "asset_assigned.html",
        "subject": "Action Required: Asset Assigned to You"
    },
    "asset.returned": {
        "template": "asset_returned.html",
        "subject": "Confirmation: Asset Returned Successfully"
    }
}

async def process_email_event(payload: EventPayload):
    event_info = EVENT_MAP.get(payload.event_name)
    if not event_info:
        log_email_event(payload.event_name, payload.recipient_email, "N/A", "FAILED", "Unknown event type")
        return

    try:
        await send_event_email(
            recipient=payload.recipient_email,
            subject=event_info["subject"],
            template_name=event_info["template"],
            template_data=payload.data
        )
        log_email_event(payload.event_name, payload.recipient_email, event_info["subject"], "SUCCESS", None)
    except Exception as e:
        logger.error(f"Error processing email event: {e}")
        log_email_event(payload.event_name, payload.recipient_email, event_info["subject"], "FAILED", str(e))

@router.post("/send/event", status_code=202)
async def send_event(payload: EventPayload, background_tasks: BackgroundTasks, api_key: str = Depends(verify_api_key)):
    """
    Triggers an email based on the event_name mapping.
    Processes the sending asynchronously.
    """
    if payload.event_name not in EVENT_MAP:
        raise HTTPException(status_code=400, detail=f"Invalid event_name. Supported events: {list(EVENT_MAP.keys())}")

    # Add the processing to background tasks
    background_tasks.add_task(process_email_event, payload)
    
    return {"message": "Event received and email dispatch queued.", "event": payload.event_name}
