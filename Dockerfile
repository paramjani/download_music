# Use a lightweight Python image
FROM python:3.11-bullseye


# Install ffmpeg and system dependencies
RUN apt update && apt install -y ffmpeg && apt clean

# Set working directory
WORKDIR /app

# Copy your application code
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Start the Flask app using Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
