import os
import requests
import json
import time
import schedule
from datetime import datetime, timedelta
import boto3
from flask import Flask

import requests
import json
import time
import schedule
from datetime import datetime, timedelta
from flask import Flask

# Amazon API credentials
AMAZON_ACCESS_KEY = "YOUR_AMAZON_ACCESS_KEY"
AMAZON_SECRET_KEY = "YOUR_AMAZON_SECRET_KEY"
ASSOCIATE_TAG = "YOUR_TRACKING_ID"

# Facebook API credentials
PAGE_ID = "YOUR_PAGE_ID"  # Your Facebook page ID
PAGE_ACCESS_TOKEN = "YOUR_PAGE_ACCESS_TOKEN"  # Your Facebook page access token

# Flask app setup with dummy port
app = Flask(__name__)

# Function to get best deals from Amazon
def get_amazon_deals():
    # Amazon API request to get best-sellers (simplified for now)
    deals = [
        {
            "title": "Sample Product",
            "image": "https://example.com/product.jpg",
            "old_price": 199.99,
            "new_price": 99.99,
            "link": f"https://www.amazon.ca/dp/PRODUCT_ID?tag={ASSOCIATE_TAG}"
        }
    ]
    return deals

# Function to format post in English & French
def format_facebook_post(deal):
    return (
        f"🔥 {deal['title']} 🔥\n\n"
        f"💰 **Before:** ${deal['old_price']} → **Now:** ${deal['new_price']}!\n"
        f"🛒 Buy now: {deal['link']}\n\n"
        f"(Affiliate link - We may earn a commission)\n\n"
        f"---\n\n"
        f"🔥 {deal['title']} 🔥\n\n"
        f"💰 **Avant:** {deal['old_price']}$ → **Maintenant:** {deal['new_price']}$!\n"
        f"🛒 Acheter maintenant: {deal['link']}\n\n"
        f"(Lien affilié - Nous pouvons toucher une commission)"
    )

# Function to post on Facebook
def post_to_facebook(deal):
    message = format_facebook_post(deal)
    image_url = deal['image']
    
    # URL to post on Facebook
    post_url = f"https://graph.facebook.com/v12.0/{PAGE_ID}/feed"
    
    # Data for the post
    data = {
        "message": message,
        "access_token": PAGE_ACCESS_TOKEN
    }

    # Sending POST request to Facebook Graph API
    response = requests.post(post_url, data=data)
    
    # Debugging the response
    if response.status_code != 200:
        print(f"Error posting to Facebook: {response.status_code}")
        print(response.json())
    else:
        print("Successfully posted to Facebook")

# Scheduler to run every hour
def job():
    # Get Amazon deals
    deals = get_amazon_deals()
    if deals:
        post_to_facebook(deals[0])

# Set up scheduler to run every hour
schedule.every(1).hour.do(job)

# Flask route to trigger posting immediately (for testing)
@app.route('/')
def index():
    job()  # Trigger the job to post immediately
    return "Bot is posting to Facebook!"

# Run Flask app with a dummy port
if __name__ == "__main__":
    # Start the job immediately after the server starts
    job()  # This ensures the bot posts when the app starts

    app.run(host='0.0.0.0', port=8080)  # Exposing on port 8080 (dummy port)
