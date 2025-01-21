import os
import time
from flask import Flask, render_template, Response, request, send_from_directory
from yt_dlp import YoutubeDL
from threading import Thread
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
from queue import Queue

app = Flask(__name__)
progress_queue = Queue()

def extract_playlist_id(url):
    query = parse_qs(urlparse(url).query)
    return query.get('list', [None])[0]

def fetch_playlist_videos(playlist_id, api_key):    
    youtube = build('youtube', 'v3', developerKey=api_key)
    video_ids = []
    request = youtube.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=50
    )

    while request:
        response = request.execute()
        video_ids.extend(item['snippet']['resourceId']['videoId'] for item in response['items'])
        request = youtube.playlistItems().list_next(request, response)

    return video_ids
    
def download_videos(video_ids):
    video_urls = [f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids]

    for video_url in video_urls:
        download_videoplaylist_with_progress(video_url)
    
def download_videoplaylist_with_progress(videoplaylist_url):
    DOWNLOAD_PATH = os.environ.get('DOWNLOAD_PATH', os.path.join(os.getcwd(), 'downloads'))
    print(f"Download folder used: {DOWNLOAD_PATH}")
    
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)

    options = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(DOWNLOAD_PATH, '%(title)s.%(ext)s'),
        'noplaylist': False,
    }

    def progress_hook(d):
        """Хук для обработки прогресса."""
        if d['status'] == 'downloading':
            message = f"Downloading file {d['info_dict']['title']}: {d['_percent_str']} completed"
            progress_queue.put(message)
        elif d['status'] == 'finished':
            message = f"File {d['info_dict']['title']} downloaded successfully!"
            progress_queue.put(message)

    options['progress_hooks'] = [progress_hook]   

    try:
        with YoutubeDL(options) as ydl:
            ydl.download([videoplaylist_url])
    except Exception as e:
        progress_queue.put(f"Error during download: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        playlist_url = request.form.get("playlist_url")
        if playlist_url:
            playlist_id = extract_playlist_id(playlist_url)
            if playlist_id:
                api_key = "AIzaSyCX21f1UAqdBE6TGolNIYHA1WxaiNR7aOU"
                if not api_key:
                    return render_template(
                        "result.html",
                        title="Error!",
                        message="API key not configured.",
                        details="Please set the API key as an environment variable.",
                    )
                
                try:
                    video_ids = fetch_playlist_videos(playlist_id, api_key)
                    if not video_ids:
                        return render_template(
                            "result.html",
                            title="Error!",
                            message="No videos found in the playlist.",
                            details="The provided playlist is empty or inaccessible.",
                        )
                    # Запускаем процесс загрузки
                    thread = Thread(target=download_videos, args=(video_ids,))
                    thread.start()
                    return render_template('progress.html', playlist_url=playlist_url)
                except Exception as e:
                    return render_template(
                        "result.html",
                        title="Error!",
                        message="Failed to fetch playlist videos.",
                        details=str(e),
                    )
            return render_template(
                "result.html",
                title="Error!",
                message="Could not extract playlist ID.",
                details="The provided URL is invalid or does not contain a playlist ID.",
            )
    return render_template("index.html")

@app.route('/progress_stream')
def progress_stream():
    def generate():
        while True:
            if not progress_queue.empty():
                message = progress_queue.get()
                yield f"data: {message}\n\n"
            else:
                time.sleep(1)

    return Response(generate(), content_type="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True)