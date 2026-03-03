# Terminal ASCII Video Player — Setup Guide (Windows)

## Quick Start

### Step 1: Install Python via Chocolatey

Open **PowerShell as Administrator** and run:

```powershell
choco install python
```

If you don't have Chocolatey, install it first:
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### Step 2: Verify Python Installation

```powershell
python --version
pip --version
```

### Step 3: Install Required Python Packages

```powershell
pip install yt-dlp opencv-python Pillow colorama
```

### Step 4 (Optional): Install FFmpeg

For better video quality (recommended):
```powershell
choco install ffmpeg
```

### Step 5: Run the Tool

```powershell
python vidterm.py "https://www.youtube.com/watch?v=XXXXXXXXXXX"
```

Replace the URL with an actual YouTube, X (Twitter), or Twitch video.

---

## Features

✅ **Download & Play** — Supports YouTube, X (Twitter), Twitch, and any yt-dlp-compatible site
✅ **ASCII Art** — Converts every frame pixel into "@" characters (or grayscale ramp)
✅ **Auto-Detect** — Automatically sizes to your terminal
✅ **Pause/Resume** — Press SPACE to pause, SPACE again to resume
✅ **Controls** — Q or ESC to quit

---

## Usage Examples

### Basic Usage
```powershell
python vidterm.py "https://www.youtube.com/watch?v=video_id"
```

### Specify Quality
```powershell
python vidterm.py "https://www.youtube.com/watch?v=video_id" --quality 720p
```

Available qualities: `360p`, `480p` (default), `720p`, `1080p`, `best`

### Pure @ Mode (No Grayscale)
```powershell
python vidterm.py "https://www.youtube.com/watch?v=video_id" --pure-at
```

### Play Local Video File
```powershell
python vidterm.py "https://www.youtube.com/watch?v=video_id" --no-download "C:\path\to\video.mp4"
```

Or just the URL without downloading:
```powershell
python vidterm.py --no-download "C:\path\to\video.mp4"
```

---

## Keyboard Controls

| Key | Action |
|-----|--------|
| **SPACE** | Pause / Resume |
| **Q** or **ESC** | Quit |

---

## Troubleshooting

### "Missing required packages"
Install them:
```powershell
pip install yt-dlp opencv-python Pillow colorama
```

### "Download failed" for X (Twitter) videos
Some X videos may require authentication. Test with:
```powershell
yt-dlp --cookies-from-browser chrome "https://x.com/user/status/..."
```

Then run the tool normally.

### Video plays too slowly
Use a lower quality:
```powershell
python vidterm.py "URL" --quality 360p
```

### Terminal looks garbled
Make sure your terminal supports ANSI escape codes (Windows 10+, modern PowerShell, or Terminal).

---

## Requirements

- **Windows 10 or later** (for ANSI support)
- **Python 3.7+**
- **FFmpeg** (optional but recommended for quality downloads)

---

## How It Works

1. **Download** — Uses `yt-dlp` to download video from any supported platform
2. **Process** — Reads frames using OpenCV
3. **Convert** — Maps pixel brightness to ASCII characters
4. **Render** — Displays each frame in the terminal
5. **Playback** — Syncs to video FPS with pause/resume support

---

## Performance Tips

- Use `--quality 360p` for slower machines
- Close other resource-heavy applications
- Use a faster internet connection for downloads
- Modern GPU helps with frame resizing (OpenCV on CUDA)

Enjoy your terminal video player! 🎬
