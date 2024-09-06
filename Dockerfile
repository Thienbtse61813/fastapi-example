FROM python:3.11-slim

ENV PYTHONPATH=/app

#Install netcat
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# set working directory
WORKDIR /app

COPY alembic.ini .

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code to working directory
COPY . .

# Make start.sh executable
RUN chmod +x start.sh

# Expose port 8000
EXPOSE 8000

# Run uvicorn
CMD ["./start.sh"]
