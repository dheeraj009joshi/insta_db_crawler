from scraper import Scraper
from config import token, hashtags, count 
from db import db
from concurrent.futures import ThreadPoolExecutor

scraper = Scraper(token=token)

def scrape_for_hashtag(tag):
    # Create a valid MongoDB collection name
    collection_name = f"reels_{tag.strip('#').replace(' ', '_').lower()}"
    
    # Create the collection dynamically
    collection = db[collection_name]

    print(f"Scraping top reels for: {tag} → Collection: {collection_name}")
    
    # Pass the collection to the scraper
    reels = scraper.scrape_top_hashtag_posts(hashtag=tag, count=count, collection=collection)
    
    return reels

def main():
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(scrape_for_hashtag, hashtags)

if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    main()
