# 🚀 Asset Manager - Email Microservice

A standalone, production-ready microservice built with **FastAPI** to handle all automated email notifications for the **Asset Manager** ecosystem. This service acts as a plug-and-play internal system that maps application events (like user creation or asset assignments) directly to beautifully designed HTML templates.

---

## 🏗️ Architecture & How It Works

This service is designed as an **independent plugin**. Instead of embedding email logic inside your main application (Asset Manager, ERP, etc.), those applications simply send a lightweight HTTP POST request to this service.

### Key Logic Flow:
1.  **Request Capture**: The Main Application sends an `event_name` (e.g., `asset.assigned`) and the required `data` (recipient, asset details).
2.  **Security**: The service validates the request using a secure `X-API-Key`.
3.  **Template Mapping**: The service automatically resolves the `event_name` to a high-quality **Jinja2** HTML template.
4.  **Async Dispatch**: Using **FastAPI Background Tasks**, the service acknowledges the request instantly (`202 Accepted`) and sends the email in the background without blocking the main workflow.
5.  **Observability**: Every success or failure is logged natively to an **email_logs** table in **Supabase**.

---

## 🛠️ Technology Stack (Open Source)

| Library | Purpose | License |
| :--- | :--- | :--- |
| **FastAPI** | High-performance web framework for the API layer. | MIT |
| **fastapi-mail** | The core engine used to interface with Gmail SMTP asynchronously. | MIT |
| **Jinja2** | Modern templating engine for rendering dynamic HTML emails. | BSD-3-Clause |
| **Supabase (Python)** | Client for asynchronous logging of email events. | MIT |
| **Pydantic Settings** | Robust configuration management via environment variables. | MIT |
| **Uvicorn** | ASGI server implementation for running the service. | BSD-3-Clause |
| **UV** | Extremely fast Python package manager and resolver. | MIT/Apache |

---

## ⚙️ Setup & Installation

### 1. Prerequisites
- **Python 3.10+**
- **UV** (Recommended for package management)
- **Gmail App Password** (For SMTP relay)

### 2. Environment Configuration
Create a `.env` file in the root directory:
```env
# Mail Credentials
MAIL_USERNAME=your-email@jmv.co.in
MAIL_PASSWORD=your-app-password
MAIL_FROM=your-email@jmv.co.in
MAIL_FROM_NAME=Asset Manager
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_STARTTLS=True
MAIL_SSL_TLS=False

# Observability
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-service-role-key # 🔴 IMPORTANT: Use the Service Role Key, not Anon Key!

# Security
API_KEY=your-secure-internal-api-key
```

### 3. Installation
Using `uv`, installation is nearly instantaneous:
```bash
uv sync
```

### 4. Database Setup (Supabase)
Run the following SQL script in your Supabase SQL Editor to enable logging:
```sql
CREATE TABLE email_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    request_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    event_name TEXT NOT NULL,
    recipient_email TEXT NOT NULL,
    subject TEXT NOT NULL,
    status TEXT NOT NULL,
    error_details TEXT
);
```

---

## 🚀 Usage & API Documentation

### 1. Endpoint: `GET /`
A public endpoint to check service uptime and discover available events. No API key required.
```bash
curl http://localhost:8000/
```

### 2. Endpoint: `POST /send/event`
**Headers Required:**
- `X-API-Key`: Your configured API Key
- `Content-Type`: `application/json`

This endpoint dynamically routes logic based on the `event_name` provided in the JSON body. Below are the specific payload structures required for each scenario.

#### Scenario A: Welcome Email (`user.created`)
Triggered when a new user joins the system.
```json
{
  "event_name": "user.created",
  "recipient_email": "new.employee@example.com",
  "data": {
    "name": "Employee Name"
  }
}
```

#### Scenario B: Asset Assigned (`asset.assigned`)
Triggered when a laptop, phone, or any physical/digital asset is delegated.
```json
{
  "event_name": "asset.assigned",
  "recipient_email": "employee@example.com",
  "data": {
    "name": "Employee Name",
    "asset_name": "MacBook Pro",
    "asset_model": "M3 Max",
    "serial_number": "C02XYZ12345",
    "assigned_date": "2026-04-09"
  }
}
```

#### Scenario C: Asset Returned (`asset.returned`)
Triggered to officially confirm when an asset is returned and logged back into inventory.
```json
{
  "event_name": "asset.returned",
  "recipient_email": "employee@example.com",
  "data": {
    "name": "Employee Name",
    "asset_name": "MacBook Pro",
    "serial_number": "C02XYZ12345",
    "returned_date": "2026-12-31"
  }
}
```

---

## 🧪 Testing Locally

The service includes independent test scripts for all core events. Run them one by one while the server is active:

```bash
# Start the server
uv run uvicorn main:app --reload

# In a new terminal, run tests:
uv run python test_welcome.py
uv run python test_assigned.py
uv run python test_returned.py
```

---

## 📂 Project Structure
```text
email-service/
├── app/
│   ├── api/          # Route definitions
│   ├── core/         # Config and Security middleware
│   ├── schemas/      # Pydantic request models
│   ├── services/     # Email and Logger logic
│   └── templates/    # Premium HTML Jinja2 templates
├── .env              # Sensitive configurations
├── main.py           # Application Entry point
├── pyproject.toml    # Dependencies (UV)
└── test_*.py         # Event-specific test utilities
```

---

## 🔒 Security Note
This service is intended for **internal infrastructure**. It should NOT be exposed directly to the public internet without being behind an authentication layer (like our API Key middleware) or within a private VPC.
