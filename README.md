Terminal ASCII Video Player

Interactive CLI tool to play local and online videos directly in your Windows terminal as real-time ASCII art.

📄 Source File: vidterm.py
🔎 Referenced implementation:

Introduction

Terminal ASCII Video Player is a Windows-only interactive command-line application that converts video frames into ASCII characters and renders them in real time inside your terminal.

It supports:

🎬 Local .mp4 files

🌐 Online videos (YouTube, X/Twitter, Twitch, Instagram, TikTok, etc.)

⚙️ Interactive video settings

⏸ Pause / Resume

🎨 Grayscale ramp mode or Pure @ artistic mode

Built with:

opencv-python

Pillow

yt-dlp

colorama

numpy

Table of Contents

Features

Installation

Usage

Controls

Settings Explained

Dependencies

Project Structure

How It Works

Troubleshooting

License

Features

🎞 Converts video frames to ASCII in real time

📁 Auto-detects local MP4 files in current directory

🌍 Downloads videos via yt-dlp

🎚 Adjustable quality (360p–1080p / best)

🖥 Dynamic terminal resizing support

⏯ Pause/resume during playback

🎨 Two ASCII modes:

Detailed grayscale ramp

Pure @ character mode

🧵 Multithreaded keyboard listener

🪟 Optimized for Windows terminal (uses msvcrt)

Installation
1️⃣ Clone or Download

Place vidterm.py in your desired directory.

2️⃣ Install Python Dependencies
pip install yt-dlp opencv-python Pillow colorama numpy
3️⃣ (Recommended) Install FFmpeg

FFmpeg improves quality and enables video/audio merging.

Install via Chocolatey:

choco install ffmpeg
Usage

Run the script:

python vidterm.py
Flow:

Select a local MP4 file OR

Download from URL

Adjust settings

Play video as ASCII art in your terminal

Controls
In Video Selection Menu
Key	Action
↑ / ↓	Navigate
Enter	Select video
D	Download from URL
Q / ESC	Exit
During Playback
Key	Action
Space	Pause / Resume
Q / ESC	Quit playback
Settings Explained
🎥 Quality

Options:

360p

480p

720p

1080p

best

If FFmpeg is installed, best video+audio streams are merged.

Without FFmpeg, fallback to single-file format.

📐 Aspect Ratio

Controls vertical scaling of ASCII output.

Value Range	Effect
0.30–0.40	Wide output
0.45	Default (balanced)
0.55–0.65	Good for fullscreen
0.70–0.95	Tall / maximum height

Tip: For 1440p fullscreen, try 0.70–0.95.

🎨 Pure @ Mode

OFF → Detailed grayscale ramp:

 .:-=+*#%@

ON → Only @ characters (artistic look)

Dependencies

Required Python packages:

yt-dlp

opencv-python

Pillow

numpy

colorama

Standard library modules used:

threading

tempfile

pathlib

shutil

msvcrt

time

sys

os

Project Structure
vidterm.py

Main components:

VideoDownloader – Handles URL downloads via yt-dlp

FrameConverter – Converts video frames to ASCII

TerminalRenderer – Handles terminal rendering

PlaybackState – Thread-safe playback state

VideoSelector – Interactive file selection

SettingsMenu – Interactive settings editor

Player – Core playback engine

How It Works

Video is opened via OpenCV (cv2.VideoCapture)

Each frame is:

Converted to grayscale

Resized based on terminal dimensions

Mapped to ASCII characters

Frame is rendered with ANSI escape codes

Keyboard input is handled in a background thread

Playback sync is maintained using frame timing

Troubleshooting
❌ "Missing required package"

Install dependencies:

pip install yt-dlp opencv-python Pillow colorama numpy
❌ Download fails

Install FFmpeg:

choco install ffmpeg

Ensure URL is supported by yt-dlp

❌ "This tool is designed for Windows"

This project uses msvcrt and is currently Windows-only.

⚠ Video looks squashed or stretched

Adjust the Aspect Ratio setting.

License

No license specified in the source file.
You may add one depending on your distribution needs (e.g., MIT, Apache 2.0, GPL).

Version

2.0.0
