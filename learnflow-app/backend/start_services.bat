@echo off
REM Start LearnFlow backend services

echo Starting LearnFlow backend services...

REM Check if virtual environment exists, if not create it
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Start the backend API server
echo Starting LearnFlow API server on port 8000...
start /b uvicorn main:app --host 0.0.0.0 --port 8000 --reload

echo LearnFlow backend services started successfully!
echo API available at: http://localhost:8000
echo API documentation available at: http://localhost:8000/docs

pause