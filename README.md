# Terminal ASCII Video Player

Version: 2.0.0

A Windows-focused Python CLI that plays local videos or downloaded videos as real-time ASCII art in your terminal.

It supports local `.mp4` playback, plus URL downloads through `yt-dlp` (YouTube, X/Twitter, Twitch, and many other supported sites).

## What It Does

- Scans the current folder for local `.mp4` files.
- Lets you choose a video using an interactive arrow-key menu.
- Lets you tune playback settings before starting.
- Downloads and plays URL videos through `yt-dlp`.
- Renders frames as ASCII in real time with pause/resume controls.

## Requirements

- Windows 10 or newer.
- Python 3.7+.
- Python packages:

  - `yt-dlp`
  - `opencv-python`
  - `Pillow`
  - `colorama`

- Optional but recommended:

  - FFmpeg (improves format handling and quality selection for downloads)

## Install

```powershell
pip install yt-dlp opencv-python Pillow colorama
```

Optional FFmpeg install (Chocolatey):

```powershell
choco install ffmpeg
```

## Run

```powershell
python vidterm.py
```

No arguments are required.

## Interactive Flow

1. Video selector opens.
2. Choose a local `.mp4` file or select download-from-URL.
3. Settings menu opens.
4. Configure quality, aspect ratio, and pure `@` mode.
5. Start playback.

## Controls

### Video Selector

- Up/Down: move selection.
- Enter: select item.
- D: download from URL.
- Q or Esc: exit.

### Settings Menu

- Up/Down: navigate settings.
- Enter: edit selected setting.
- Q or Esc: back.

### During Playback

- Space: pause/resume.
- Q or Esc: stop and return to menu.

## Settings

- Quality: `360p`, `480p`, `720p`, `1080p`, `best`.
- Aspect ratio: adjustable (default: `0.45`).
- Pure `@` mode: toggles between grayscale ramp and only `@` characters.

## Troubleshooting

### Missing package error

Install dependencies:

```powershell
pip install yt-dlp opencv-python Pillow colorama
```

### FFmpeg warning or lower quality downloads

Install FFmpeg:

```powershell
choco install ffmpeg
```

### No local videos listed

Put `.mp4` files in the same folder as `vidterm.py`.

### Slow playback

- Lower quality to `360p`.
- Reduce terminal size.
- Close heavy background apps.

## Project Files

- `vidterm.py`: main application.
- `vidterm.bat`: batch launcher.
- `install.ps1`: setup helper script.
- `SETUP.md`: setup guide.
- `INTERACTIVE_GUIDE.md`: menu walkthrough.
- `QUICKSTART.txt` / `QUICK_REFERENCE.txt`: quick usage notes.

## License

MIT
