from scraper import Scraper
from config import token ,count ,keyword


scraper = Scraper(token=token)
def main():
    print(f"Scraping top reels with keyword: {keyword}")
    # reels = scraper.scrape_top_reels_with_keyword(query=keyword, count=count)
    reels = scraper.scrape_top_hashtag_posts(hashtag="sleepbetter", count=20000)

if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()  # only necessary if freezing to executable, but harmless
    main()
# main()
    