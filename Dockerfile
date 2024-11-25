# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock /app/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

# Copy the project files
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Run the Django application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "currency_exchange.wsgi:application"]