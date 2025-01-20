import os
import time
from flask import Flask, render_template, Response, request
from yt_dlp import YoutubeDL

app = Flask(__name__)

# Буфер для хранения прогресса
progress_buffer = []

def download_playlist_with_progress(playlist_url):
    global progress_buffer
    progress_buffer.clear()  # Очистка буфера перед началом загрузки
    browsers = ['firefox', 'chrome', 'msedge', 'brave', 'vivaldi', 'opera']
    DOWNLOAD_PATH = os.path.join(os.path.expanduser('~'), 'Downloads')
    print(f"Используемая папка для загрузки: {DOWNLOAD_PATH}")
    
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)

    options = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(DOWNLOAD_PATH, '%(title)s.%(ext)s'),
        'noplaylist': False,
    }

    def progress_hook(d):
        """Хук для обработки сообщений прогресса."""
        if d['status'] == 'downloading':
            progress_buffer.append(f"Загрузка файла {d['info_dict']['title']}: {d['_percent_str']} завершено")
        elif d['status'] == 'finished':
            progress_buffer.append(f"Файл {d['info_dict']['title']} успешно загружен!")

    for browser in browsers:
        try:
            options['cookiesfrombrowser'] = (browser,)
            progress_buffer.append(f"Попытка использования куков из {browser}...")

            # Настройка хуков
            options['progress_hooks'] = [progress_hook]

            with YoutubeDL(options) as ydl:
                ydl.download([playlist_url])
            progress_buffer.append(f"Куки из {browser} успешно использованы.")
            break
        except Exception as e:
            progress_buffer.append(f"Не удалось использовать {browser}: {e}")

    if not progress_buffer:
        progress_buffer.append("Ошибка: не удалось использовать куки ни одного из браузеров.")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        playlist_url = request.form.get("playlist_url")
        if playlist_url:
            return render_template('progress.html', playlist_url=playlist_url)
        else:
            return render_template(
                "result.html",
                title="Ошибка!",
                message="Ссылка на плейлист отсутствует.",
                details="Пожалуйста, введите корректную ссылку на плейлист YouTube и попробуйте снова.",
            )
    return render_template("index.html")

@app.route('/progress_stream')
def progress_stream():
    def generate():
        while True:
            if progress_buffer:
                message = progress_buffer.pop(0)
                yield f"data: {message}\n\n"
            else:
                time.sleep(1)  # Ожидание новых сообщений
    playlist_url = request.args.get("playlist_url")
    if not playlist_url:
        return Response("data: Ошибка: ссылка на плейлист отсутствует.\n\n", content_type="text/event-stream")
    # Запускаем загрузку в фоне
    from threading import Thread
    thread = Thread(target=download_playlist_with_progress, args=(playlist_url,))
    thread.start()
    return Response(generate(), content_type="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True)