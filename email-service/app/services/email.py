import asyncio
from fastapi_mail import FastMail, MessageSchema, MessageType
from app.config import settings, mail_config
from app.services.worldtime import fetch_current_date
from app.services.logger import log_email_event

async def send_with_retry(request_id: str, payload: dict, max_retries: int = 3):
    """Send email with exponential backoff retry. Attempts: 1s -> 4s -> 16s"""
    delay = 1
    for attempt in range(max_retries):
        try:
            current_date = fetch_current_date()
            to, cc = resolve_recipients(payload)
            template_info = get_template_info(payload['event_name'])

            template_data = {
                "employee_name": payload['primary_recipient']['name'],
                "admin_name": payload['admin_name'],
                "category": payload['asset_data']['category'],
                "model_no": payload['asset_data']['model_no'],
                "asset_id": payload['asset_data']['asset_id'],
                "date": current_date,
            }

            message = MessageSchema(
                subject=template_info["subject"],
                recipients=to,
                cc=cc,
                template_body=template_data,
                subtype=MessageType.html
            )

            fm = FastMail(mail_config)
            await fm.send_message(message, template_name=template_info["template"])

            log_email_event(request_id, payload, status="success",
                                  retry_count=attempt, dispatched_date=current_date)
            return

        except Exception as e:
            if attempt == max_retries - 1:
                log_email_event(request_id, payload, status="failed",
                                      retry_count=attempt, error=str(e))
                return
            await asyncio.sleep(delay)
            delay *= 4  # exponential: 1s -> 4s -> 16s


def resolve_recipients(payload: dict):
    """To: Employee + Admin who performed the action. CC: All other Admins (empty if all_admin_emails not provided)"""
    to = [payload['primary_recipient']['email'], payload['admin_email']]
    cc = [a for a in payload['all_admin_emails'] if a != payload['admin_email']]
    return to, cc


def get_template_info(event_name: str) -> dict:
    """Map event name to template file and email subject"""
    return {
        "asset.assigned": {
            "template": "asset_assigned.html",
            "subject": "Asset Assigned to You"
        },
        "asset.returned": {
            "template": "asset_returned.html",
            "subject": "Asset Returned Successfully"
        },
        "force.recall.old": {
            "template": "force_recall_old.html",
            "subject": "Important: Asset Force Recalled from You"
        },
        "force.recall.new": {
            "template": "force_recall_new.html",
            "subject": "Asset Assigned to You (Force Recall)"
        },
    }[event_name]
