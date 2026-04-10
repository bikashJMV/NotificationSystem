import logging
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.schemas.email import EventPayload
from app.services.email import send_event_email
from app.services.logger import log_email_event
from app.core.security import verify_api_key

logger = logging.getLogger(__name__)
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

EVENT_MAP = {
    "user.created": {
        "template": "welcome.html",
        "subject": "Welcome to Asset Manager!"
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

async def process_email_event(payload: EventPayload, request_id: str):
    event_info = EVENT_MAP.get(payload.event_name)
    if not event_info:
        log_email_event(payload.event_name, payload.recipient_email, "N/A", "FAILED", request_id, "Unknown event type")
        return

    try:
        await send_event_email(
            recipient=payload.recipient_email,
            subject=event_info["subject"],
            template_name=event_info["template"],
            template_data=payload.data,
            cc=payload.cc
        )
        log_email_event(payload.event_name, payload.recipient_email, event_info["subject"], "SUCCESS", request_id, None)
    except Exception as e:
        logger.error(f"Error processing email event: {e}")
        log_email_event(payload.event_name, payload.recipient_email, event_info["subject"], "FAILED", request_id, str(e))

@router.get("/", status_code=200, tags=["Health", "Root"])
async def root():
    """
    Root / Health check endpoint. No authentication required.
    Returns service status, HTTP status code, and supported events.
    """
    return {
        "status": "ok",
        "status_code": 200,
        "service": "email-microservice",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": "Asset Manager Email Microservice is running securely.",
        "supported_events": list(EVENT_MAP.keys())
    }


@router.post("/send/event", status_code=202)
@limiter.limit("60/minute")
async def send_event(
    request: Request,
    payload: EventPayload,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    """
    Triggers an email based on the event_name mapping.
    Processes the sending asynchronously.
    """
    request_id = str(uuid.uuid4())

    if payload.event_name not in EVENT_MAP:
        raise HTTPException(status_code=400, detail=f"Invalid event_name. Supported events: {list(EVENT_MAP.keys())}")

    # Add the processing to background tasks
    background_tasks.add_task(process_email_event, payload, request_id)
    
    return {
        "message": "Event received and email dispatch queued.",
        "event": payload.event_name,
        "request_id": request_id
    }
