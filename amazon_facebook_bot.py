import os
import requests
import json
import time
import schedule
from datetime import datetime, timedelta
import boto3
from flask import Flask

# Amazon API credentials
AMAZON_ACCESS_KEY = os.environ.get("AMAZON_ACCESS_KEY")
AMAZON_SECRET_KEY = os.environ.get("AMAZON_SECRET_KEY")
ASSOCIATE_TAG = os.environ.get("ASSOCIATE_TAG")

# Facebook API credentials
PAGE_ID = os.environ.get("PAGE_ID")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")

# Initialize Flask app
app = Flask(__name__)

# Function to get best deals from Amazon
def get_amazon_deals():
    # Amazon API request to get best-sellers
    endpoint = "https://webservices.amazon.ca/onca/xml"
    params = {
        "Service": "AWSECommerceService",
        "Operation": "ItemSearch",
        "SearchIndex": "All",
        "ResponseGroup": "Images,ItemAttributes,Offers",
        "Sort": "salesrank",
        "AWSAccessKeyId": AMAZON_ACCESS_KEY,
        "AssociateTag": ASSOCIATE_TAG
    }
    response = requests.get(endpoint, params=params)
    
    # Parse the XML response (simplified for now)
    # This part should be updated to properly handle the Amazon API response
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
    
    fb_api_url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/photos"
    data = {
        "url": image_url,
        "caption": message,
        "access_token": PAGE_ACCESS_TOKEN
    }
    response = requests.post(fb_api_url, data=data)
    print(response.json())

# Post immediately when the app starts
def post_on_start():
    deals = get_amazon_deals()
    if deals:
        post_to_facebook(deals[0])

# Scheduler to run every hour
def job():
    deals = get_amazon_deals()
    if deals:
        post_to_facebook(deals[0])

# Flask routes
@app.route('/')
def index():
    return "Amazon Facebook Bot is running!"

@app.route('/start-bot')
def start_bot():
    post_on_start()
    return "Bot started and posted the first deal!"

# Run the app and post as soon as the Flask server starts
if __name__ == "__main__":
    post_on_start()  # Post as soon as the server starts
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


