# import csv

# from db import collection,collection2

# # === Open CSV file for writing ===
# with open("output.csv", "w", newline='', encoding='utf-8') as csvfile:
#     fieldnames = ["post_id", "description", "videoUrl", "username", "createTime", "playCount","transcript", "comment_count", "comments"]
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()

#     # === Iterate through documents ===
#     for doc in collection.find({}):
#         row = {
#             "post_id": doc.get("post_id", {}),
#             "description": doc.get("description", ""),
#             "videoUrl": doc.get("videoUrl", ""),
#             "username": doc.get("user_info", {}),
#             "createTime": doc.get("createTime", ""),
#             "playCount": doc.get("playCount", {}),
#             "transcript": doc.get("transcript", {}),
#             "comment_count": doc.get("comment_count", {}),
#             "comments": " | ".join([c.strip() for c in doc.get("comments", []) if c.strip()])
#         }
#         writer.writerow(row)
#     for doc in collection2.find({}):
#         row = {
#             "post_id": doc.get("post_id", {}),
#             "description": doc.get("description", ""),
#             "videoUrl": doc.get("videoUrl", ""),
#             "username": doc.get("user_info", {}),
#             "createTime": doc.get("createTime", ""),
#             "playCount": doc.get("playCount", {}),
#              "transcript": doc.get("transcript", {}),
#             "comment_count": doc.get("comment_count", {}),
#             "comments": " | ".join([c.strip() for c in doc.get("comments", []) if c.strip()])
#         }
#         writer.writerow(row)

# print("✅ Exported to output2.csv")

from scraper import Scraper

aa=Scraper(token="0daja8wqtv3o16jpszpj582tbyduul3t")

comments=aa.scrape_post_comments(
    post_id="3376532501647980689",
    count=1000
)

print(comments)

