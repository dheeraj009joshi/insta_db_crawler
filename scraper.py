import json
import os
from datetime import datetime
from hikerapi import Client
from config import token
from helper import get_scraper_data
from db import collection


class Scraper:
    def __init__(self, token):
        print("[*] Initializing Scraper...")
        self.cl = Client(token=token)

    def scrape_post_comments(self, post_id, count):
        print(f"[+] Scraping comments for post ID: {post_id}")
        try:
            comments = self.cl.media_comments(id=post_id, count=count)
            return [item.get("text", "") for item in comments]
        except Exception as e:
            print(f"[!] Error fetching comments: {e}")
            return []

    def scrape_top_reels_with_keyword(self, query, count):
        print(f"[+] Scraping top {count} reels for keyword: '{query}'")
        reels_max_id = ""
        results_total = []

        while len(results_total) < count:
            try:
                res = self.cl.fbsearch_reels_v2(query=query, reels_max_id=reels_max_id)
                print(f"[✓] API fetched batch with {len(res.get('reels_serp_modules', [{}])[0].get('clips', []))} items")

                clips = res.get("reels_serp_modules", [{}])[0].get("clips", [])
                results = []

                for item in clips:
                    media = item.get("media", {})
                    user = media.get("user", {})
                    caption = media.get("caption", {})
                    video_versions = media.get("video_versions", [])

                    data = {
                        "description": caption.get("text", ""),
                        "post_id": media.get("pk", ""),
                        "videoUrl": video_versions[0]["url"] if video_versions else "",
                        "user_info": {
                            "name": user.get("full_name", ""),
                            # "bio": user.get("bio", ""),
                            "username": user.get("username", ""),
                            "userId": user.get("id", "")
                        },
                        "createTime": datetime.fromtimestamp(media.get("taken_at", 0)).isoformat(),
                        "reshare_count": media.get("reshare_count", 0),
                        "playCount": media.get("play_count", 0),
                        "comment_count": media.get("comment_count", 0),
                    }

                    results.append(data)
                    results_total.append(data)

                    # print(f"[•] Collected reel: {data['post_id']} - ...")

                # # Send data to helper for processing
                # get_scraper_data(results, self)
                # print(f"[→] Batch processed. Total so far: {len(results_total)}")

                # Handle pagination
                if res.get("has_more"):
                    print("has max id ", res.get("reels_max_id", ""))
                    reels_max_id = res.get("reels_max_id", "")
                else:
                    print("[✓] No more pages available.")
                    break


            except Exception as e:
                print(f"[!] Error during scraping loop: {e}")
                pass

        return results_total[:count]

aa=Scraper(token=token)
aa.scrape_top_reels_with_keyword(query="sleep better", count=20000)