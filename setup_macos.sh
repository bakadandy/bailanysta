#!/bin/bash
# Setup script for Bailanysta on macOS

echo "Setting up Bailanysta on macOS..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install it using Homebrew:"
    echo "brew install python3"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. It should come with Python3."
    exit 1
fi

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL is not installed. Please install it using Homebrew:"
    echo "brew install postgresql"
    echo "After installation, start PostgreSQL service with:"
    echo "brew services start postgresql"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install spaCy model
echo "Installing spaCy language model..."
python -m spacy download en_core_web_sm

# Download NLTK data
echo "Downloading NLTK data..."
python -c "import nltk; nltk.download('stopwords')"

# Create PostgreSQL database if it doesn't exist
echo "Setting up PostgreSQL database..."
if ! psql -lqt | cut -d \| -f 1 | grep -qw bailanysta; then
    createdb bailanysta
    echo "Database 'bailanysta' created."
else
    echo "Database 'bailanysta' already exists."
fi

# Create .env file if it doesn't exist
if [ ! -f "bailanysta_project/.env" ]; then
    echo "Creating .env file..."
    cat > bailanysta_project/.env << EOF
# Database settings
DATABASE_NAME=bailanysta
DATABASE_USER=postgres
DATABASE_PASSWORD=
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Django settings
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(50))")
DEBUG=True

# Optional: AI settings
# HUGGINGFACE_TOKEN=
EOF
    echo ".env file created. Please update database credentials if needed."
fi

# Run migrations
echo "Running database migrations..."
cd bailanysta_project
python manage.py makemigrations
python manage.py migrate

echo "Would you like to create a superuser? (y/n)"
read -r create_superuser
if [ "$create_superuser" = "y" ] || [ "$create_superuser" = "Y" ]; then
    python manage.py createsuperuser
fi

echo "Setup complete! You can now run the server with:"
echo "cd bailanysta_project && python manage.py runserver" 