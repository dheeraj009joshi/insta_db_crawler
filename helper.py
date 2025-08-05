import os
import whisper
import torchaudio
import subprocess
import requests
from multiprocessing import Queue, Process
from concurrent.futures import ThreadPoolExecutor, as_completed
from worker.transcribe import whisper_worker



# ============================
# Whisper Multiprocess Manager
# ============================

class WhisperManager:
    def __init__(self):
        print("[*] Starting Whisper worker...")
        self.task_queue = Queue()
        self.result_queue = Queue()
        self.worker = Process(target=whisper_worker, args=(self.task_queue, self.result_queue))
        self.worker.start()

    def transcribe(self, idx, video_path):
        self.task_queue.put((idx, video_path))
        return self.result_queue.get()

    def shutdown(self):
        print("[*] Shutting down Whisper worker...")
        self.task_queue.put("STOP")
        self.worker.join()
        print("[✓] Whisper worker stopped.")


# ============================
# Video Downloader
# ============================

def download_tiktok_video(video_url: str, output_path: str = "video.mp4"):
    try:
        headers = {
            'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        }

        print(f"[↓] Downloading video from: {video_url}")
        response = requests.get(video_url, headers=headers, stream=True)

        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"[✓] Video downloaded: {output_path}")
            return output_path
        else:
            print(f"[!] Failed to download. Status: {response.status_code} - {response.reason}")
            return None
    except Exception as e:
        print(f"[!] Error downloading video: {e}")
        return None


# ============================
# Post Processor
# ============================

def get_scraper_data(posts,collection, scraper):
    whisper_manager = WhisperManager()
    augmented_posts = []
    ss=scraper.scrape_post_comments

    
    def process_post(post, idx):
        try:
            filename = f"{post['post_id']}.mp4"
            video_file = download_tiktok_video(post["videoUrl"], filename)

            if not video_file:
                print(f"[!] Skipping {post['post_id']} due to failed download.")
                return post
            if post["type"]==2:
            # Inner tasks: transcription and comment fetching
                print(f"[→] Transcribing {filename}")
                _, transcript = whisper_manager.transcribe(idx, video_file)
                post["transcript"] = transcript
            else:
                print(f"[→] Skipping transcription for non-video post {post['post_id']}")
                post["transcript"] = ""
            print(f"[→] Fetching comments for {post['post_id']}")
            comments = ss(post["post_id"], 100)
            print(comments)
            if not comments:
                print(f"[!] No comments found for {post['post_id']}")
            else:
                print(f"[✓] Retrieved {len(comments)} comments")

            post["comments"] = comments

            print(f"[✓] Done processing post {post['post_id']}")
        except Exception as error:
            print(f"[!] Error processing post {post['post_id']}: {error}")
        finally:
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                    print(f"[x] Deleted temp file: {filename}")
                except:
                    print(f"[!] Could not delete file: {filename}")
        return post

    try:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_post, post, idx) for idx, post in enumerate(posts)]

            for future in as_completed(futures):
                result = future.result()
                result["_id"]=str(result.get("post_id"))
                augmented_posts.append(result)
                print(f"[📥] Inserting post: {result.get('post_id')}")
                try:
                    collection.insert_one(result)
                except Exception as e:
                    print(f"[!] Error inserting post {result.get('post_id')}: {e}")

    finally:
        whisper_manager.shutdown()

    return augmented_posts
