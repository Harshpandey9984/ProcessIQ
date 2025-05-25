@echo off
echo ===================================
echo Starting Minimal Backend Server
echo ===================================

echo Installing required packages...
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] pydantic python-multipart

echo Starting server...
python minimal_backend.py

pause
