#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# Render Build Script — runs every time you deploy
# ─────────────────────────────────────────────────────────────
set -o errexit   # Exit on error

pip install --upgrade pip
pip install -r requirements.txt

# Collect static files into /staticfiles
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate

# Optional: seed initial data on first deploy
# python manage.py seed_data
