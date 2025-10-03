#!/bin/bash

echo "Starting Deployment..."

# Step 1: Build Docker image
echo "Building Docker image..."
docker build -t cdc-analysis .

# Step 2: Run analysis
echo "Running analysis..."
docker run --rm -v $(pwd)/../data:/app/data:ro cdc-analysis

echo "Done!"
