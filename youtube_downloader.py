import os
from yt_dlp import YoutubeDL

def download_playlist(playlist_url, download_path):
    options = {
        'format': 'best[ext=mp4]',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),  # Шаблон имени файла
        'noplaylist': False,  # Скачивать весь плейлист
    }

    with YoutubeDL(options) as ydl:
        ydl.download([playlist_url])

if __name__ == "__main__":
    # Предустановленные данные
    playlist_url = "https://www.youtube.com/playlist?list=PLeVA7eICJ6d0jhMyQOzFGip1YDNP-PwV9"
    download_path = r"C:\Users\DELL\Downloads\smeshariky"

    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    print("Скачивание началось...")
    try:
        download_playlist(playlist_url, download_path)
        print("Скачивание завершено!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")