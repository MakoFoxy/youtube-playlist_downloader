import os
from flask import Flask, request, render_template
from yt_dlp import YoutubeDL

app = Flask(__name__)
DOWNLOAD_PATH = os.path.join(os.getcwd(), 'downloads')

def download_playlist(playlist_url):
    options = {
        'format': 'best[ext=mp4]',  # Скачивать видео в формате MP4
        'outtmpl': os.path.join(DOWNLOAD_PATH, '%(title)s.%(ext)s'),  # Путь сохранения
        'noplaylist': False,  # Скачивать весь плейлист
    }

    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)

    with YoutubeDL(options) as ydl:
        ydl.download([playlist_url])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        playlist_url = request.form.get('playlist_url')
        if playlist_url:
            try:
                download_playlist(playlist_url)
                return f"Видео из плейлиста по адресу {playlist_url} успешно загружены в папку: {DOWNLOAD_PATH}"
            except Exception as e:
                return f"Произошла ошибка: {e}"
        else:
            return "Ссылка на плейлист отсутствует!"

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
