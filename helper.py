import os
import whisper
import torchaudio
import subprocess
import requests
from multiprocessing import Queue, Process
from concurrent.futures import ThreadPoolExecutor, as_completed
from worker.transcribe import whisper_worker
from db import collection


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

def get_scraper_data(posts, scraper):
    whisper_manager = WhisperManager()
    augmented_posts = []
    ss=scraper.scrape_post_comments

    def transcribe_video(video_path):
        model = whisper.load_model("base")  # You can cache/load outside this func for speed
        return model.transcribe(video_path)["text"]

    def fetch_comments(scraper, post_id):
        return scraper.scrape_post_comments(post_id, 100)
    def process_post(post, scraper):
        try:
            post_id = post["post_id"]
            filename = f"{post_id}.mp4"
            video_path = download_tiktok_video(post["videoUrl"], filename)

            if not video_path:
                print(f"[!] Failed to download video: {post_id}")
                return None

            # Run transcription and comments in parallel
            with ThreadPoolExecutor(max_workers=2) as executor:
                transcribe_future = executor.submit(transcribe_video, video_path)
                comment_future = executor.submit(fetch_comments, scraper, post_id)

                transcript = transcribe_future.result()
                comments = comment_future.result()

            post["transcript"] = transcript
            post["comments"] = comments
            post["_id"] = str(post_id)

            print(f"[✓] Finished: {post_id}")
            return post

        except Exception as e:
            print(f"[!] Error processing post {post_id}: {e}")
            return None

        finally:
            if os.path.exists(filename):
                os.remove(filename)
        

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
