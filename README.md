🎬 Terminal ASCII Video Player
Version 2.0.0
A powerful Python-based CLI tool that transforms videos into real-time ASCII art. Whether it's a local .mp4 or a link from YouTube, X (Twitter), or Twitch, this tool renders every frame directly in your Windows terminal.
✨ Features
Interactive Menu: Browse and select local .mp4 files using your arrow keys.
Multi-Platform Support: Paste a URL to download and play videos from YouTube, Twitch, X, and more (via yt-dlp).
Auto-Detection: Automatically adapts to your terminal's width and height.
Smooth Playback: Optimized frame rendering with pause/resume support and real-time FPS syncing.
Windows Optimized: Built specifically for the Windows console with colorama and msvcrt support.
🚀 Quick Start
1. Prerequisites
OS: Windows 10 or later.
Python: 3.7 or higher.
FFmpeg (Optional): Highly recommended for better video quality and audio merging.
2. Installation
Clone the repository and install the required dependencies:
powershell
pip install yt-dlp opencv-python Pillow colorama
Use code with caution.

3. Running the Tool
Simply run the script to enter the interactive menu:
powershell
python vidterm.py
Use code with caution.

🎮 Controls
Key	Action
UP / DOWN	Navigate the file menu
ENTER	Select file / Confirm setting
SPACE	Pause / Resume playback
Q / ESC	Quit player or Exit application
🛠️ Configuration
The tool offers several internal settings to customize your experience:
Quality Selection: Choose between 360p, 480p, 720p, 1080p, or best.
ASCII Ramps:
Simple: Uses only @ characters.
Gradient: Uses a 10-character ramp .:-=+*#%@ for better detail.
Aspect Correction: Automatically compensates for terminal character height-to-width ratios.
📦 Requirements & Dependencies
yt-dlp: For handling video downloads.
opencv-python: For frame extraction and grayscale processing.
Pillow: For high-quality image resizing and downscaling.
colorama: For ANSI escape sequences on Windows.
📝 License
This project is open-source. Feel free to fork, modify, and improve it!
Pro Tip: For the best visual experience, use a font like Consolas or Courier New in your terminal and reduce the font size to allow for higher "resolution" ASCII art.
