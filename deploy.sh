#!/bin/bash

# BeRAM Website Deployment Script
# This script deploys the BeRAM website to a production server

# Exit on error
set -e

echo "Starting deployment of BeRAM website..."

# Pull latest changes
echo "Pulling latest changes from repository..."
git pull

# Install or update dependencies
echo "Installing/updating dependencies..."
pip install -r requirements.txt

# Run tests
echo "Running tests..."
pytest

# Create logs directory if it doesn't exist
echo "Setting up logs directory..."
mkdir -p logs

# Set environment to production
export FLASK_ENV=production

# Restart Gunicorn (using systemd)
echo "Restarting Gunicorn service..."
sudo systemctl restart beram

# Restart Nginx
echo "Restarting Nginx..."
sudo systemctl restart nginx

echo "Deployment completed successfully!"
