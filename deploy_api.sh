#!/bin/bash

echo "Starting to deploy api..."

rm -rf /project/api
cp -R api /project
cd /project/api
source venv/bin/activate
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl status gunicorn

echo "Finished deploying api."
