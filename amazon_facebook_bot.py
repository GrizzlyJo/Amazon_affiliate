import json
import time
import requests
import schedule
import os
from datetime import datetime, timedelta
from threading import Thread

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
    message = f"🔥 Deal Alert! {deal['title']} is now {deal['price']}!\n\n{deal['url']}\n\n(This post contains an affiliate link)"
    url = f"https://graph.facebook.com/{FACEBOOK_PAGE_ID}/feed"
    payload = {"message": message, "access_token": FACEBOOK_PAGE_ACCESS_TOKEN}
    
    print(f"Posting to Facebook: {message}")
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("✅ Successfully posted to Facebook!")
        return True
    else:
        print(f"❌ Failed to post! Status Code: {response.status_code}, Response: {response.text}")
        return False

# Main function to post deals
def publish_deals():
    print("🔄 Checking for new deals to post...")
    posted_deals = load_posted_deals()
    best_deals = get_best_amazon_deals()
    
    for deal in best_deals:
        if not was_posted_recently(deal, posted_deals):
            print(f"🚀 Posting deal: {deal['title']}")
            if post_to_facebook(deal):
                posted_deals[deal["url"]] = datetime.now().strftime("%Y-%m-%d")
                save_posted_deals(posted_deals)
            time.sleep(5)
    print("✅ Deal posting check completed.")

# Schedule the bot to run every hour
schedule.every(1).hour.do(publish_deals)

# Keep the scheduler running in the background
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # Run the bot immediately at startup
    publish_deals()
    
    # Start the scheduler in a separate thread
    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.start()

