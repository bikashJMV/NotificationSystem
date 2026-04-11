import asyncio
from app.services.email import send_event_email

async def test_send():
    await send_event_email(
        recipient="bikash@jmv.co.in",
        subject="Test CC Email",
        template_name="welcome.html",
        template_data={"name": "Test User"},
        cc=["doe692568@gmail.com"]
    )
    print("Email sent!")

if __name__ == "__main__":
    asyncio.run(test_send())
