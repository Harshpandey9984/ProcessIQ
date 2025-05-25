@echo off
echo ===================================
echo Starting Debug Backend Server
echo ===================================

echo Installing required packages...
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] pydantic python-multipart

echo Starting debug server...
python debug_backend.py

pause
