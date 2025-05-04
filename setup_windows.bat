@echo off
echo Setting up Bailanysta on Windows...

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python from https://www.python.org/downloads/
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing Python dependencies...
pip install -r requirements.txt

REM Install spaCy model
echo Installing spaCy language model...
python -m spacy download en_core_web_sm

REM Download NLTK data
echo Downloading NLTK data...
python -c "import nltk; nltk.download('stopwords')"

REM Create .env file if it doesn't exist
if not exist bailanysta_project\.env (
    echo Creating .env file...
    echo # Database settings > bailanysta_project\.env
    echo DATABASE_NAME=bailanysta >> bailanysta_project\.env
    echo DATABASE_USER=postgres >> bailanysta_project\.env
    echo DATABASE_PASSWORD=gigadandy >> bailanysta_project\.env
    echo DATABASE_HOST=localhost >> bailanysta_project\.env
    echo DATABASE_PORT=5432 >> bailanysta_project\.env
    echo. >> bailanysta_project\.env
    echo # Django settings >> bailanysta_project\.env
    python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(50))" >> bailanysta_project\.env
    echo DEBUG=True >> bailanysta_project\.env
    echo. >> bailanysta_project\.env
    echo # Optional: AI settings >> bailanysta_project\.env
    echo # HUGGINGFACE_TOKEN= >> bailanysta_project\.env
    echo .env file created. Please update database credentials if needed.
)

REM Run migrations
echo Running database migrations...
cd bailanysta_project
python manage.py makemigrations
python manage.py migrate

echo Would you like to create a superuser? (y/n)
set /p create_superuser=
if /i "%create_superuser%"=="y" (
    python manage.py createsuperuser
)

echo Setup complete! You can now run the server with:
echo cd bailanysta_project ^&^& python manage.py runserver

cd ..
pause 