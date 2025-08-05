from scraper import Scraper
from config import token, count
from concurrent.futures import ThreadPoolExecutor
from db import db
scraper = Scraper(token=token)


def main():
    tag="naturalDeodorant"
    # Create a valid MongoDB collection name
    collection_name = f"{tag.strip('#').replace(' ', '_').lower()}"
    
    # Create the collection dynamically
    collection = db[collection_name]

    print(f"Scraping top reels for: {tag} → Collection: {collection_name}")
    
    # Pass the collection to the scraper
    reels = scraper.scrape_top_hashtag_posts(hashtag=tag, count=count, collection=collection)
    
    
if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    main()
