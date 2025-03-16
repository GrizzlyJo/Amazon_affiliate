import requests
import json
import time
import schedule
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import os
from flask import Flask

# Initialize Flask app
app = Flask(__name__)

# Dummy port (for testing or deployment purposes)
PORT = os.environ.get("PORT", 8080)  # Default to 8080 if not set in the environment

# Amazon API credentials
AMAZON_ACCESS_KEY = "YOUR_AMAZON_ACCESS_KEY"
AMAZON_SECRET_KEY = "YOUR_AMAZON_SECRET_KEY"
ASSOCIATE_TAG = "YOUR_TRACKING_ID"

# Facebook API credentials
PAGE_ID = "YOUR_PAGE_ID"
PAGE_ACCESS_TOKEN = "YOUR_PAGE_ACCESS_TOKEN"

# Load previously posted deals to prevent reposting
def load_posted_deals():
    try:
        with open("posted_deals.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_posted_deals(posted_deals):
    with open("posted_deals.json", "w") as file:
        json.dump(posted_deals, file)

# Function to get best deals from Amazon
def get_amazon_deals():
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
    
    # Check for successful response
    if response.status_code != 200:
        print("Error fetching Amazon deals")
        return []

    # Parse the XML response
    root = ET.fromstring(response.content)
    deals = []
    
    for item in root.findall(".//Item"):
        title = item.find(".//Title").text
        image_url = item.find(".//MediumImage/URL").text
        old_price = float(item.find(".//OfferSummary/LowestNewPrice/FormattedPrice").text.replace('$', '').strip())
        new_price = float(item.find(".//OfferSummary/LowestNewPrice/FormattedPrice").text.replace('$', '').strip())
        link = item.find(".//DetailPageURL").text + f"?tag={ASSOCIATE_TAG}"
        
        deal = {
            "title": title,
            "image": image_url,
            "old_price": old_price,
            "new_price": new_price,
            "link": link
        }
        deals.append(deal)
    
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
    
    # Check if the post was successful
    if response.status_code == 200:
        print("Successfully posted to Facebook")
    else:
        print(f"Failed to post on Facebook: {response.json()}")

# Scheduler to run every hour
def job():
    posted_deals = load_posted_deals()
    deals = get_amazon_deals()
    
    if deals:
        for deal in deals:
            # Check if the deal was already posted
            deal_id = deal['link'].split('/')[-1]
            if deal_id not in posted_deals or datetime.now() - datetime.strptime(posted_deals[deal_id], "%Y-%m-%d %H:%M:%S") > timedelta(days=30):
                post_to_facebook(deal)
                posted_deals[deal_id] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        save_posted_deals(posted_deals)

# Flask route to start the bot
@app.route('/start-bot', methods=['GET'])
def start_bot():
    schedule.every(1).hour.do(job)
    return "Bot started and will post deals every hour."

# Flask route to get current status
@app.route('/status', methods=['GET'])
def status():
    return "Amazon Facebook Bot is running!"

if __name__ == "__main__":
    # Run the Flask app on the specified port
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

