from app.schemas.email import EventPayload

payload1 = EventPayload(
    event_name="user.created",
    recipient_email="test@example.com",
    data={}
)
print("Payload 1 works:", payload1.model_dump())

payload2 = EventPayload(
    event_name="user.created",
    recipient_email="test@example.com",
    cc="cc@example.com",
    data={}
)
print("Payload 2 works:", payload2.model_dump())

payload3 = EventPayload(
    event_name="user.created",
    recipient_email="test@example.com",
    cc=["cc1@example.com", "cc2@example.com"],
    data={}
)
print("Payload 3 works:", payload3.model_dump())
