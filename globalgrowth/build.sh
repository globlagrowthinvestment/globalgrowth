#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install AWS CLI (if needed)
pip install awscli

# Upgrade setuptools and wheel
pip install --upgrade setuptools wheel
pip install ez_setup

# Install requirements
pip install -r requirements.txt

# Collect static files (if applicable for Django projects)
python manage.py collectstatic --no-input

# Apply database migrations (if applicable for Django projects)
python manage.py migrate