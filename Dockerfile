# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /app

# Copy the local code to the container
COPY . /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script into the container
COPY ./wait-for-postgres.sh /app/wait-for-postgres.sh
RUN chmod +x /app/wait-for-postgres.sh

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose Gunicorn port
EXPOSE 8000

# Run the application with Gunicorn
CMD ["gunicorn", "your_django_project.wsgi:application", "-b", "0.0.0.0:8000"]