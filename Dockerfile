FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories
RUN mkdir -p /app/logs /app/staticfiles

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Make entrypoint scripts executable
RUN chmod +x /app/entrypoint.sh || true

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=alx_travel_app.settings

# Expose the Django port
EXPOSE 8000

# Default command
CMD ["gunicorn", "alx_travel_app.wsgi:application", "--bind", "0.0.0.0:8000"]