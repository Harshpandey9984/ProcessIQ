@echo off
cd C:\Intel hackathon Project\digital-twin-platform
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > C:\Intel hackathon Project\digital-twin-platform\logs\backend.log 2>&1
