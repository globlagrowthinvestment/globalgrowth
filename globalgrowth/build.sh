#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

pip install awscli

pip install --upgrade setuptools pip
pip install --upgrade wheel

# Install requirements
pip install -r requirements.txt


# Collect static files (if applicable)
python manage.py collectstatic --no-input

# Apply database migrations (if applicable)
python manage.py migrate
