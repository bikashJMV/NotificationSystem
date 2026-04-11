import logging
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from app.core.limiter import limiter
from app.schemas.email import EmailRequest, ApiResponse, EventEnum
from app.services.email import send_with_retry
from app.services.logger import log_email_event
from app.core.security import verify_api_key

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", status_code=200, tags=["Health", "Root"])
async def root():
    """Root / Health check endpoint. No authentication required. Returns service status, HTTP status code, and supported events."""
    return ApiResponse(
        status="success",
        status_code=200,
        message="Notification Microservice is running",
        timestamp=datetime.now(timezone.utc).isoformat(),
        data={
            "service": "email-microservice",
            "version": "1.0.0",
            "supported_events": [e.value for e in EventEnum]
        }
    )


@router.post("/send/event", status_code=202)
@limiter.limit("200/minute")
async def send_event(
    request: Request,
    payload: EmailRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    """Queue email event for processing via background tasks with retry logic"""
    request_id = str(uuid.uuid4())

    log_email_event(request_id, payload.dict(), status="queued")

    background_tasks.add_task(send_with_retry, request_id, payload.dict())

    return ApiResponse(
        status="success",
        status_code=202,
        message="Event queued for processing",
        timestamp=datetime.now(timezone.utc).isoformat(),
        data={"request_id": request_id}
    )
