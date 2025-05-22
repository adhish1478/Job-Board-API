
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install netcat for wait-for-db.sh
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure wait-for-db.sh is executable
RUN chmod +x wait-for-db.sh

# Expose port
EXPOSE 8000

# Entrypoint
CMD ["./wait-for-db.sh", "sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]