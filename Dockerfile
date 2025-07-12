FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nmap \
    wkhtmltopdf \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Note: Nikto and Wapiti would need to be installed separately
# or use a different base image that includes them
# This Dockerfile focuses on the Python application setup

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create results directory
RUN mkdir -p results

# Expose port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]