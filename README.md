# Terminal ASCII Video Player 🎬

A Python CLI tool that downloads videos from **YouTube, X (Twitter), Twitch**, and any **yt-dlp**-supported site, then plays them as **ASCII art** directly in your terminal with auto-detected terminal size, pause/resume, and real-time playback.

Every video pixel is converted to `@` characters (or a grayscale ASCII ramp) and rendered frame-by-frame in the terminal.

---

## Features

✨ **Multi-Platform Download**
- YouTube, X (Twitter), Twitch, Instagram, TikTok, Reddit, and 1000+ other sites (via yt-dlp)
- Automatic quality selection (360p, 480p, 720p, 1080p, best)
- Automatic temp file cleanup on exit

📺 **ASCII Art Rendering**
- Every pixel converted to `@` characters or grayscale ramp
- Aspect-ratio corrected (terminal chars are ~2x taller than wide)
- No flicker—uses ANSI cursor-home for smooth playback
- Auto-detects and adapts to terminal size changes

🎮 **Playback Controls**
- **SPACE** — Pause/Resume
- **Q** or **ESC** — Quit
- Real-time FPS sync (no frame skipping needed)
- Status bar with current time, frame count, and controls

🪟 **Windows Optimized**
- Installs via Chocolatey (`choco install python`)
- Colorama integration for ANSI support on Windows Console
- Non-blocking keyboard input with daemon thread
- Clean terminal restoration on exit

---

## Quick Start (5 Minutes)

### 1. Install Python (Windows)

Open **PowerShell as Administrator**:

```powershell
choco install python
```

Or install Chocolatey first if needed:
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### 2. Install Python Packages

```powershell
pip install yt-dlp opencv-python Pillow colorama
```

### 3. Run the Tool

```powershell
python vidterm.py "https://www.youtube.com/watch?v=XXXXXXXXXXX"
```

Replace the URL with a real video link.

---

## Usage

### Basic Command
```bash
python vidterm.py "VIDEO_URL"
```

### With Options
```bash
python vidterm.py "VIDEO_URL" --quality 480p --pure-at
```

### Full Help
```bash
python vidterm.py --help
```

---

## Examples

### YouTube Video
```powershell
python vidterm.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### X (Twitter) Video
```powershell
python vidterm.py "https://x.com/user/status/1234567890"
```

### Twitch VOD
```powershell
python vidterm.py "https://www.twitch.tv/videos/1234567890"
```

### High Quality
```powershell
python vidterm.py "URL" --quality 720p
```

### Pure @ Characters Only (No Grayscale)
```powershell
python vidterm.py "URL" --pure-at
```

### Play Local Video File
```powershell
python vidterm.py --no-download "C:\path\to\video.mp4"
```

---

## Command-Line Options

```
positional arguments:
  url                   Video URL (YouTube, X/Twitter, Twitch, or any
                        yt-dlp supported site)

optional arguments:
  -h, --help            show this help message and exit
  -q {360p,480p,720p,1080p,best}, --quality {360p,480p,720p,1080p,best}
                        Video quality to download (default: 480p)
  --pure-at             Use only '@' characters (no grayscale ramp)
  --no-download FILE    Skip download; play a local video file instead
```

---

## Keyboard Controls

| Key | Action |
|:---:|--------|
| **SPACE** | Pause / Resume playback |
| **Q** | Quit |
| **ESC** | Quit |

---

## Requirements

- **Windows 10 or later** (for ANSI escape code support)
- **Python 3.7+**
- **Internet connection** (to download videos)
- **~50 MB** free disk space (for dependencies and temp videos)

### Optional
- **FFmpeg** (for better video quality downloads) — `choco install ffmpeg`

---

## Installation Details

### Dependencies

| Package | Purpose |
|---------|---------|
| `yt-dlp` | Download videos from 1000+ sites |
| `opencv-python` (cv2) | Frame extraction and resizing |
| `Pillow` (PIL) | High-quality image downscaling |
| `colorama` | ANSI escape code support on Windows |
| `msvcrt` | Windows keyboard input (built-in) |

### Install All at Once
```powershell
pip install yt-dlp opencv-python Pillow colorama
```

---

## How It Works

1. **Download Phase**
   - Uses `yt-dlp` to download video from URL
   - Automatically selects best available quality
   - Saves to temp directory with auto-cleanup

2. **Decode Phase**
   - Opens video with OpenCV (`cv2.VideoCapture`)
   - Extracts frames at video's native FPS
   - Gets total frame count and video duration

3. **Render Phase**
   - Converts each frame to grayscale
   - Resizes to terminal dimensions (aspect-ratio corrected)
   - Maps pixel brightness to ASCII character
   - Writes to terminal using CURSOR_HOME (no flicker)

4. **Playback Phase**
   - Syncs frame timing to video FPS
   - Handles pause/resume with spacebar
   - Renders status bar with time, frame count, controls
   - Cleans up temp files on exit

---

## Performance Tips

### If Video Plays Slowly

1. **Lower the quality** — Use `--quality 360p` instead of 720p
2. **Disable other apps** — Close browser, IDE, heavy apps
3. **Smaller terminal** — Use a narrower terminal window
4. **Check GPU** — OpenCV uses CPU by default; modern GPU would help

### Example for Slow Machines
```powershell
python vidterm.py "URL" --quality 360p
```

---

## Troubleshooting

### "Missing required packages"
```powershell
pip install yt-dlp opencv-python Pillow colorama
```

### "Cannot open video file"
- Make sure ffmpeg is installed: `choco install ffmpeg`
- Or try a different quality: `python vidterm.py "URL" --quality 360p`

### X (Twitter) Video Won't Download
Some X videos require authentication:
```powershell
yt-dlp --cookies-from-browser chrome "https://x.com/user/status/..."
```
Test with the above command first to diagnose.

### "Python was not found"
Install Python via Chocolatey (admin PowerShell):
```powershell
choco install python
```

### Terminal Output Looks Garbled
- Make sure you're using Windows 10+ Terminal or PowerShell
- Very old console versions don't support ANSI escape codes
- Try Windows Terminal from the Microsoft Store

### Video Pauses During Playback
- Your machine may be too slow to decode frames in real-time
- Try lower quality: `--quality 360p`
- Close other resource-heavy applications

---

## Advanced Usage

### Batch Processing Multiple Videos

Create a batch file `play_videos.bat`:
```batch
@echo off
python vidterm.py "https://www.youtube.com/watch?v=video1"
python vidterm.py "https://www.youtube.com/watch?v=video2"
python vidterm.py "https://www.youtube.com/watch?v=video3"
```

Then run:
```powershell
.\play_videos.bat
```

### Scripted Playback

```python
import subprocess
urls = [
    "https://www.youtube.com/watch?v=video1",
    "https://www.youtube.com/watch?v=video2",
]
for url in urls:
    subprocess.run(["python", "vidterm.py", url, "--quality", "480p"])
```

---

## File Structure

```
C:\Users\IJXP\why\
├── vidterm.py          # Main application (single file, ~700 lines)
├── vidterm.bat         # Windows batch launcher
├── README.md           # This file
└── SETUP.md            # Detailed setup guide
```

---

## Architecture

### Classes

- **`PlaybackState`** — Thread-safe pause/quit flags using `threading.Event`
- **`FrameConverter`** — Converts OpenCV BGR frames to ASCII strings
- **`TerminalRenderer`** — Outputs to terminal using ANSI codes (colorama-wrapped)
- **`VideoDownloader`** — Wraps yt-dlp for video downloads
- **`Player`** — Main orchestrator (download → play → cleanup)

### Threading

- **Main thread** — Frame render loop (tight FPS sync)
- **Keyboard thread** — Daemon that polls `msvcrt.kbhit()` for pause/quit (non-blocking)

### Key Techniques

- **No-flicker rendering** — Uses ANSI CURSOR_HOME instead of cls
- **Aspect ratio correction** — Terminal chars are ~2.2× taller; multiply rows by 0.45
- **High-precision timing** — `time.perf_counter()` for frame budget calculation
- **Non-blocking I/O** — msvcrt polling prevents input lag

---

## Limitations & Known Issues

| Issue | Workaround |
|-------|-----------|
| Very slow machines | Use `--quality 360p` |
| X videos requiring auth | Use `yt-dlp --cookies-from-browser chrome URL` first |
| Twitch live streams | Only works with VODs (archived videos), not live streams |
| Terminal too small | Output will be truncated; enlarge terminal window |
| Old Windows (pre-Win10) | No ANSI support; upgrade or use Windows Terminal |

---

## License

MIT License — Use, modify, and distribute freely.

---

## Contributing

Found a bug or have a suggestion? Great!
- Check the [GitHub Issues](https://github.com/anthropics/claude-code/issues) for Claude Code feedback
- For yt-dlp issues, see [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)

---

## Made With

- **Python 3.7+** — Core language
- **yt-dlp** — Video downloading
- **OpenCV** — Frame processing
- **Pillow** — Image resizing
- **colorama** — ANSI support on Windows
- **Windows Terminal** — Best viewing experience

Enjoy watching videos in your terminal! 🎬✨
#   v i d e o c o n v e r t e r  
 