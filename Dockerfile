# Use an official Python runtime as a parent image
FROM python:3.11-slim as builder

# Set the working directory in the builder stage
WORKDIR /app

# Copy only the necessary files first to leverage Docker cache
COPY pyproject.toml ./
COPY brick/ ./brick/

# Install the brick package
RUN pip install --no-cache-dir .

# Create a non-root user and switch to it
RUN addgroup --system app && adduser --system --group app
USER app

# Copy your application code (e.g., worker.py)
COPY --chown=app:app . .