from datetime import datetime, timezone, timedelta

def fetch_current_date() -> str:
    """Get current IST date - calculated from UTC + 5:30"""
    ist = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    return ist.strftime("%d-%m-%Y")
