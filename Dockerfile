FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install any dependencies your app needs
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script into the container
COPY amazon_facebook_bot.py .

# Make sure the script runs when the container starts
CMD ["python", "amazon_facebook_bot.py"]
