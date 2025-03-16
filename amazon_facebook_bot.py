import requests
import json
import time
import schedule
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import boto3
import os  # Add this import to fix the issue

# Dummy port (for testing or deployment purposes)
PORT = os.environ.get("PORT", 8080)  # Default to 8080 if not set in the environment

# Amazon API credentials
AMAZON_ACCESS_KEY = "YOUR_AMAZON_ACCESS_KEY"
AMAZON_SECRET_KEY = "YOUR_AMAZON_SECRET_KEY"
ASSOCIATE_TAG = "YOUR_TRACKING_ID"

# Facebook API credentials
PAGE_ID = "YOUR_PAGE_ID"
PAGE_ACCESS_TOKEN = "YOUR_PAGE_ACCESS_TOKEN"

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

# Scheduler to run every hour
def job():
    deals = get_amazon_deals()
    if deals:
        post_to_facebook(deals[0])

schedule.every(1).hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(60)

