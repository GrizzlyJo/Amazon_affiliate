import json
import time
import requests
import schedule
import os
from datetime import datetime, timedelta
from flask import Flask

app = Flask(__name__)

# Facebook API credentials
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "your_facebook_access_token")
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID", "your_facebook_page_id")

# Amazon API credentials
AMAZON_ASSOCIATE_TAG = os.getenv("AMAZON_ASSOCIATE_TAG", "your_new_amazon_tag")

# File to track posted deals
POSTED_DEALS_FILE = "posted_deals.json"

# Load posted deals history
def load_posted_deals():
    try:
        with open(POSTED_DEALS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save posted deals history
def save_posted_deals(deals):
    with open(POSTED_DEALS_FILE, "w") as file:
        json.dump(deals, file, indent=4)

# Get the best Amazon deals (Mock function, replace with real API call)
def get_best_amazon_deals():
    return [
        {"title": "Wireless Headphones", "url": "https://amzn.to/example1", "price": "$99.99"},
        {"title": "Gaming Mouse", "url": "https://amzn.to/example2", "price": "$49.99"}
    ]

# Check if a deal was posted in the last 30 days
def was_posted_recently(deal, posted_deals):
    if deal["url"] in posted_deals:
        last_posted = datetime.strptime(posted_deals[deal["url"]], "%Y-%m-%d")
        if datetime.now() - last_posted < timedelta(days=30):
            return True
    return False

# Publish a deal on Facebook
def post_to_facebook(deal):
    message = f"🔥 Deal Alert! {deal['title']} is now {deal['price']}!\n\n{deal['url']}\n\n(This post contai


