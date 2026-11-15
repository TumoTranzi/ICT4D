# Tsebisa – Technical Documentation (Handover)

## Purpose
This document allows a partner organisation or a future student/technician to understand, run and maintain the Tsebisa pilot system.

## Technology stack
- **Language:** Python 3
- **Framework:** Flask
- **Database:** SQLite (file: `tsebisa.db`)
- **Frontend:** Server-rendered HTML + minimal CSS (mobile-friendly)

## Main features
1. Multi-step citizen reporting flow (language → category → details → reference number)
2. Sesotho and English support
3. Automatic reference number generation (format: TSE-XXXX)
4. Partner dashboard with status updates (Received / In progress / Closed)
5. Simple API placeholders for future USSD/SMS gateway integration

## How to run
```bash
pip install -r requirements.txt
python app.py
```
Server starts on http://127.0.0.1:5000

## Database
Table `reports`:
- id, reference, category, description, location, phone, language, status, created_at, updated_at

Statuses: `received`, `in_progress`, `closed`

## Extending to real USSD/SMS
1. Register with a gateway that supports Lesotho (e.g. Africa’s Talking).
2. Point the gateway’s USSD callback to `/api/ussd`.
3. Parse the `text` parameter (user input) and maintain session state (usually via the gateway’s sessionId).
4. Reply with the next menu text or an end message.
5. Use the gateway’s SMS API to send the reference number and later status updates.

## Security notes for a real deployment
- Add authentication to the dashboard (currently open for pilot simplicity).
- Validate and sanitise all inputs.
- Store phone numbers only as long as needed.
- Back up `tsebisa.db` regularly.
- Serve over HTTPS.

## Licence
MIT – free to use, modify and distribute.
