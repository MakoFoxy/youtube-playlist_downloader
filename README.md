YouTube Playlist Downloader

Welcome to YouTube Playlist Downloader, a simple web application that allows you to download YouTube playlists directly to your Downloads folder.
Features

    Real-Time Progress Tracking: See the progress of each video being downloaded in real time.
    Automatic Folder Detection: Videos are saved to the user's Downloads folder for easy access.
    Browser Cookie Support: Uses browser cookies for authentication and better compatibility.
    Modern Interface: A clean, responsive web interface for ease of use.

Live Demo

You can try the application here: YouTube Playlist Downloader
How to Use

    Open the link: https://youtube-playlist-downloader-lu9b.onrender.com.
    Paste the URL of the YouTube playlist into the input box.
    Click the Download button.
    Track the download progress in real-time on the progress page.
    Once completed, check your Downloads folder for the downloaded videos.

Requirements

    A modern web browser (Chrome, Firefox, Edge, etc.)
    Stable internet connection

Donation

Thank you for using this service! If you find it helpful, consider supporting the development:

Card Number: 4405 6398 6394 6396

Your support is greatly appreciated! 🙌
Technical Details
Tools and Technologies Used

    Backend: Python Flask
    Frontend: HTML, CSS, JavaScript
    Video Downloading: yt-dlp
    Hosting: Render.com

Folder Structure

.
├── youtube.py              # Main application file
├── templates
│   ├── index.html      # Main page
│   ├── progress.html   # Progress page
│   ├── result.html     # Result/error page
├── static
│   ├── styles.css      # Styles for the frontend
│   ├── scripts.js      # Scripts for client-side logic
├── downloads           # Directory where videos are saved
└── README.md           # Project documentation

Installation for Local Use

    Clone the repository:

git clone https://github.com/yourusername/youtube-playlist-downloader.git
cd youtube-playlist-downloader

Install dependencies:

pip install -r requirements.txt

Run the application:

    python youtube.py

    Open http://127.0.0.1:5000 in your browser.

Thank you for using YouTube Playlist Downloader! Your feedback and support are invaluable. 😊