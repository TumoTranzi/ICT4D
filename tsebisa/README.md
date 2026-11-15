# Tsebisa – Community Service Delivery Reporting System

**DIIC3110 – Information and Communication Technology for Development (ICT4D)**  
Limkokwing University of Creative Technology  
Group Assignment (40%) – Working Solution (Deliverable B)

**Group members:** Moabi Lereng, Tumo Koloi, Ts’epo Leboto, Ts’epo Mohlaoli

---

## What is Tsebisa?

Tsebisa (Sesotho for “inform / notify”) is a lightweight pilot system that allows community members to report everyday service delivery problems (water, roads, refuse, street lights, etc.) and receive an immediate reference number. The partner organisation sees the reports on a simple dashboard and can update their status.

The design follows ICT4D principles of **appropriate technology** for Lesotho:

- Works conceptually on feature phones (USSD/SMS style flow)
- Sesotho-first interface
- Very low data requirement (web simulation for the pilot)
- Simple enough to hand over and maintain

---

## How to run the pilot prototype

### 1. Install dependencies

```bash
cd tsebisa
pip install -r requirements.txt
```

### 2. Start the server

```bash
python app.py
```

### 3. Open in a browser

| Page | URL |
|------|-----|
| Home | http://127.0.0.1:5000/ |
| Citizen reporting | http://127.0.0.1:5000/report |
| Partner dashboard | http://127.0.0.1:5000/dashboard |
| User guide | http://127.0.0.1:5000/guide |

The first time you run it, a SQLite database (`tsebisa.db`) is created automatically.

---

## Pilot testing with real users

1. Explain the purpose in Sesotho (reporting problems so the office can see them).
2. Let each pilot user complete at least one report on a phone or shared device.
3. Collect feedback: Was the language clear? Were the steps too many? Did they trust it?
4. Make changes (iteration 1 and 2) and document what changed.
5. Show the partner the dashboard and practise updating statuses.

**Recommended pilot size:** 8–15 people.

---

## Project structure

```
tsebisa/
├── app.py                 # Main Flask application
├── requirements.txt
├── README.md
├── tsebisa.db             # Created on first run (SQLite)
├── templates/             # HTML pages
│   ├── base.html
│   ├── home.html
│   ├── report_language.html
│   ├── report_category.html
│   ├── report_details.html
│   ├── report_success.html
│   ├── dashboard.html
│   ├── report_view.html
│   └── guide.html
└── docs/
    ├── USER_GUIDE_EN.md
    ├── USER_GUIDE_ST.md
    └── TECHNICAL.md
```

---

## Connecting a real USSD / SMS gateway (future)

The endpoint `/api/ussd` is prepared for integration with services such as Africa’s Talking.  
In a production version you would:

1. Register a USSD short code / SMS short code.
2. Point the gateway to `/api/ussd`.
3. Parse the incoming session text and map it to the same menu logic.
4. Send SMS acknowledgements via the gateway API.

For the student pilot the web simulation is sufficient and much easier to test and demonstrate.

---

## Licence

This pilot code is released under the MIT Licence so the partner community or a local organisation can freely use, modify and continue it after the course.

---

## Contact (group)

For questions about the pilot, contact the group members via the course channels.
