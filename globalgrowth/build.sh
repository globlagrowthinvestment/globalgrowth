#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Collect static files (if applicable)
python manage.py collectstatic --no-input

# Apply database migrations (if applicable)
python manage.py migrate
