import json
import os
from datetime import datetime
from hikerapi import Client
from helper import get_scraper_data



# scraper=Client(token=token)

# hh=scraper.hashtag_medias_recent_v2(hashtag)
# aaa=open("hashtag.json", "w")   
# aaa.write(json.dumps(hh, indent=4)) 






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
    def post_by_id(self, post_id):
        print(f"[+] Fetching post by ID: {post_id}")
        try:
            post = self.cl.media_by_id_v1(id=post_id)
            return post
        except Exception as e:
            print(f"[!] Error fetching post: {e}")
            return None

    def scrape_top_hashtag_posts(self, hashtag, count,collection):
        print(f"[+] Scraping top {count} posts for hashtag: '{hashtag}'")

        page_id = ""
        results_total = 0
        while results_total<count:

            try:
                posts=[]
                posts_raw=[]
                data =  self.cl.hashtag_medias_top_v2(name=hashtag,page_id=page_id)
                posts_sections =  data["response"]["sections"]
                try:
                    posts_raw.extend(posts_sections[0]["layout_content"]["one_by_two_item"]["clips"]["items"])
                except:
                    pass
                for section in posts_sections[1:]:
                    posts_raw.extend(section["layout_content"]["medias"])
                results_total+= len(posts_raw)
                print(results_total)
                for item in posts_raw:
                  
                    media = item.get("media", {})
                    user = media.get("user", {})
                    caption = media.get("caption", {})
                    video_versions = media.get("video_versions", [])
                    print(media.get("pk", ""))
                    data_2 = {
                        "type":media.get("media_type",0),
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
                 
                    posts.append(data_2)
                get_scraper_data(posts,collection, self)
                print(f"[→] Batch processed. Total so far: {(results_total)}")


                page_id =data["next_page_id"]
                print(page_id)
            except Exception as e:
                print(f"[!] Error fetching hashtag posts: {e}")
                pass
            


    def scrape_top_reels_with_keyword(self, query, count):
        print(f"[+] Scraping top {count} reels for keyword: '{query}'")
        reels_max_id = ""
        results_total = 0

        while results_total < count:
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
                        "type":media.get("media_type",0),
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
                    results_total+=1

                    # print(f"[•] Collected reel: {data['post_id']} - ...")
                print(results[-1].get("post_id", ""))
                # Send data to helper for processing
                get_scraper_data(results, self)
                print(f"[→] Batch processed. Total so far: {len(results_total)}")

                # Handle pagination
               
                print("has max id ", res.get("reels_max_id", ""))
                reels_max_id = res.get("reels_max_id", "")
              


            except Exception as e:
                print(f"[!] Error during scraping loop: {e}")
                pass

        return results_total[:count]

# aa=Scraper(token=token)
# # aa.scrape_top_reels_with_keyword(query="sleep better", count=20000)

# aa.scrape_top_hashtag_posts(hashtag="sleepbetter", count=20000)