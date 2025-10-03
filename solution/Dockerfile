FROM python:3.11-slim

WORKDIR /app

# Security update
RUN apt-get update && apt-get upgrade -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy and run
COPY case.py .
CMD ["python", "case.py"]
