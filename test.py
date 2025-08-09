# import csv
# from db import db
# # === Collections to export from ===
# collections = [
#     db["reels_cleanbeauty"],
#     db["reels_cleanskincare"],
#     db["reels_naturaldeodorant"],
#     db["updated_cleanbeauty"],
#     db["updated_cleanskincare"],
#     db["updated_naturaldeodorant"]
# ]

# # === Track seen post_ids ===
# seen_post_ids = set()
# output_lines=[]
# # === Output CSV ===
# with open("output.csv", "w", newline='', encoding='utf-8') as csvfile:
#     fieldnames = ["post_id", "description", "videoUrl", "username", "createTime", "playCount", "transcript", "comment_count", "comments"]
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()

#     for collection in collections:
#         for doc in collection.find({}):
#             post_id = doc.get("post_id")
#             if not post_id or post_id in seen_post_ids:
#                 continue  # skip duplicates or missing

#             seen_post_ids.add(post_id)

#             row = {
#                 "post_id": post_id,
#                 "description": doc.get("description", ""),
#                 "videoUrl": doc.get("videoUrl", ""),
#                 "username": doc.get("user_info", ""),
#                 "createTime": doc.get("createTime", ""),
#                 "playCount": doc.get("playCount", ""),
#                 "transcript": doc.get("transcript", ""),
#                 "comment_count": doc.get("comment_count", ""),
#                 "comments": " | ".join([c.strip() for c in doc.get("comments", []) if isinstance(c, str) and c.strip()])
#             }
#             writer.writerow(row)


#             formatted = (
#                 f'"post_id"={post_id},\n'
#                 f'"description"={doc.get("description", "")},\n'
#                 f'"videoUrl"={doc.get("videoUrl", "")},\n'
#                 f'"username"={doc.get("user_info", "")},\n'
#                 f'"createTime"={doc.get("createTime", "")},\n'
#                 f'"playCount"={doc.get("playCount", "")},\n'
#                 f'"transcript"={doc.get("transcript", "")},\n'
#                 f'"comment_count"={doc.get("comment_count", "")},\n'
#                 f'"comments"="{" | ".join([c.strip() for c in doc.get("comments", []) if isinstance(c, str) and c.strip()])}"\n\n'
#             )
#             output_lines.append(formatted)

# print("✅ Export completed successfully to output.csv")

# output_path = "structured_post_export.txt"
# with open(output_path, "w", encoding="utf-8") as f:
#     f.writelines(output_lines)




from hikerapi import Client
from config import token
cl=Client(token=token)


aa=cl.user_a2("tamil.engineer")
print(aa)