# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project
COPY . /app/

# Create SQLite database directory and set permissions
RUN mkdir -p /app/data \
    && touch /app/data/db.sqlite3 \
    && chmod 666 /app/data/db.sqlite3

# Run migrations
RUN python manage.py makemigrations \
    && python manage.py migrate

# Expose port
EXPOSE 8000

# Start server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]