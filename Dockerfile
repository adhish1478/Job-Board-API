FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy the rest of the application code into the container
COPY . .

# Install netcat for wait-for-db.sh
RUN apt-get update && apt-get install -y netcat-openbsd
# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["./wait-for-db.sh", "sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]