import json
import time
import requests
import schedule
import os
from datetime import datetime, timedelta

# Facebook API credentials
FACEBOOK_PAGE_ACCESS_TOKEN = "your_facebook_access_token"
FACEBOOK_PAGE_ID = "your_facebook_page_id"

# Amazon API credentials
AMAZON_ASSOCIATE_TAG = "your_amazon_tag"
AMAZON_ACCESS_KEY = "your_amazon_access_key"
AMAZON_SECRET_KEY = "your_amazon_secret_key"

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
    # Replace this with an actual request to the Amazon API
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
    message = f"🔥 Deal Alert! {deal['title']} is now {deal['price']}!\n\n{deal['url']}\n\n(This post contains an affiliate link)"
    url = f"https://graph.facebook.com/{FACEBOOK_PAGE_ID}/feed"
    payload = {"message": message, "access_token": FACEBOOK_PAGE_ACCESS_TOKEN}
    response = requests.post(url, data=payload)
    return response.status_code == 200

# Main function to post deals
def publish_deals():
    posted_deals = load_posted_deals()
    best_deals = get_best_amazon_deals()
    
    for deal in best_deals:
        if not was_posted_recently(deal, posted_deals):
            if post_to_facebook(deal):
                posted_deals[deal["url"]] = datetime.now().strftime("%Y-%m-%d")
                save_posted_deals(posted_deals)
            time.sleep(5)  # Avoid Facebook API rate limits

# Schedule the bot to run every 3 hours
schedule.every(3).hours.do(publish_deals)

# Get the port from environment variables (Render expects it to be set)
port = int(os.environ.get("PORT", 5000))  # Use a dummy port, won't be used

# Run continuously in the background (no HTTP server, just background execution)
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)

