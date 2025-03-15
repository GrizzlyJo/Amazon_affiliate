# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install any dependencies your app needs
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script into the container
COPY amazon_facebook_bot.py .

# Expose a dummy port (Render requires it, but it won't be used)
EXPOSE 5000

# Ensure the script runs when the container starts
CMD ["python", "amazon_facebook_bot.py"]
