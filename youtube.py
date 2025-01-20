import os
import time
from flask import Flask, render_template, Response, request
from yt_dlp import YoutubeDL
from threading import Thread

app = Flask(__name__)

# Потокобезопасный буфер для прогресса
from queue import Queue
progress_queue = Queue()

def download_playlist_with_progress(playlist_url):
    DOWNLOAD_PATH = os.path.join(os.path.expanduser('~'), 'Downloads')
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
            ydl.download([playlist_url])
    except Exception as e:
        progress_queue.put(f"Error during download: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        playlist_url = request.form.get("playlist_url")
        if playlist_url:
            return render_template('progress.html', playlist_url=playlist_url)
        else:
            return render_template(
                "result.html",
                title="Error!",
                message="The link to the playlist is missing.",
                details="Please enter the correct YouTube playlist link and try again.",
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

    playlist_url = request.args.get("playlist_url")
    if not playlist_url:
        return Response("data: Error: link to playlist missing.\n\n", content_type="text/event-stream")
    
    # Запускаем загрузку в фоновом потоке
    thread = Thread(target=download_playlist_with_progress, args=(playlist_url,))
    thread.start()
    return Response(generate(), content_type="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True)