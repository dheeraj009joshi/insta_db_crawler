import csv

from db import collection

# === Open CSV file for writing ===
with open("output.csv", "w", newline='', encoding='utf-8') as csvfile:
    fieldnames = ["post_id", "description", "videoUrl", "username", "createTime", "playCount", "comment_count", "comments"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # === Iterate through documents ===
    for doc in collection.find():
        row = {
            "post_id": doc.get("post_id", {}),
            "description": doc.get("description", ""),
            "videoUrl": doc.get("videoUrl", ""),
            "username": doc.get("user_info", {}),
            "createTime": doc.get("createTime", ""),
            "playCount": doc.get("playCount", {}),
            "comment_count": doc.get("comment_count", {}),
            "comments": " | ".join([c.strip() for c in doc.get("comments", []) if c.strip()])
        }
        writer.writerow(row)

print("✅ Exported to output.csv")





