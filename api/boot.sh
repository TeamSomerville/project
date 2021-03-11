#!/bin/bash
source venv/bin/activate
exec gunicorn -b :5000 --access-logfile - --error-logfile - travel:app --workers 1 --timeout 60 --threads 2
