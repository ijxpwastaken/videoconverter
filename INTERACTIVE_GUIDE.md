# Terminal ASCII Video Player - Interactive Mode Guide

## NEW: Completely Interactive CLI!

You can now run **just one command** and control everything with arrow keys:

```powershell
python vidterm.py
```

**That's it!** No URLs, no command-line arguments needed.

---

## How It Works

### Screen 1: Video Selection

When you run `python vidterm.py`, you'll see:

```
════════════════════════════════════════════════════════════
  TERMINAL ASCII VIDEO PLAYER
════════════════════════════════════════════════════════════

Local MP4 Files:

▶ 1. my_video.mp4 (245.3 MB)
  2. another_video.mp4 (156.2 MB)
  3. trailer.mp4 (89.1 MB)

Options:
  ↑/↓  Navigate
  Enter  Play selected
  D  Download from URL
  Q  Exit
```

**Controls:**
- **↑/↓** — Move cursor up/down to select video
- **Enter** — Play the selected video
- **D** — Download video from YouTube/X/Twitch/etc
- **Q** — Quit

---

### Screen 2: Settings Menu

After selecting a video, you'll see:

```
════════════════════════════════════════════════════════════
  VIDEO SETTINGS
════════════════════════════════════════════════════════════

▶ Quality: 480p
  Aspect Ratio: 0.45 (↑/↓ to adjust, try 0.55 for fullscreen)
  Pure @ Mode: OFF

Controls:
  ↑/↓  Navigate or adjust aspect ratio
  ←/→  Change quality
  Space  Toggle Pure @ mode
  Enter  Play video
  Q  Back to video list
```

**Controls:**
- **↑/↓** —
  - When on **Quality**: navigate (left/right to change)
  - When on **Aspect Ratio**: adjust value (0.2 to 0.8)
  - When on **Pure @ Mode**: navigate
- **←/→** — Change quality (360p, 480p, 720p, 1080p, best)
- **Space** — Toggle Pure @ mode (ON/OFF)
- **Enter** — Play with current settings
- **Q** — Back to video list

---

## Aspect Ratio Tips for 1440p Screens

The aspect ratio controls how tall the ASCII characters appear:

| Value | Effect |
|-------|--------|
| **0.3** | Super wide (more columns, few rows) |
| **0.45** | Default (balanced) |
| **0.55** | Fullscreen (fills more of screen) ⭐ **Try this for 1440p** |
| **0.6+** | Very tall (many rows, thin columns) |

**Arrow Keys:** Use ↑/↓ to increment/decrement by 0.02

Example:
- Start at 0.45
- Press ↑ four times → 0.53 (closer to fullscreen)
- Press ↓ once → 0.51 (fine-tune)
- Press Enter to play

---

## Quality Settings

| Quality | Best For | Download Time |
|---------|----------|---|
| **360p** | Slow machines, quick download | 30 sec |
| **480p** | Default, good balance | 1-2 min |
| **720p** | High quality | 3-5 min |
| **1080p** | Best quality | 5-10 min |
| **best** | Absolute best available | Variable |

**Use arrow keys (←/→) to cycle through qualities!**

---

## Pure @ Mode

Toggles between:

- **OFF** (default): Grayscale ramp: `" .:-=+*#%@"`
  - More detailed, better visuals

- **ON**: Pure `@` characters only
  - Literal "every pixel is @"
  - Looks more artistic but less detail

Use **Space** to toggle while selected.

---

## Download from URL

While in the video selector:

1. Press **D** to open download prompt
2. Paste a YouTube/X/Twitch/etc URL
3. Settings menu appears
4. Adjust settings with arrow keys
5. Press **Enter** to download and play

**Supported Sites:**
- ✅ YouTube
- ✅ X (Twitter)
- ✅ Twitch
- ✅ Instagram
- ✅ TikTok
- ✅ Reddit
- ✅ And 1000+ more (yt-dlp supported)

---

## Playing a Video

Once you press **Enter** on the settings screen:

```
Loading video...
Downloading... (if URL)
Playing...

[ASCII Video Plays Here]

00:45/03:30  Frame 1350/5400 [PAUSED]  [SPACE=pause Q=quit]
```

**Controls During Playback:**
- **Space** — Pause / Resume
- **Q** — Stop and go back to menu
- **ESC** — Stop and go back to menu

---

## Loop Playback

The menu loops! After a video finishes:

```
Video finished. Press any key to continue...
```

Press any key → Back to video selector → Play another video or adjust settings

---

## Example Workflow

1. **Run it:**
   ```powershell
   python vidterm.py
   ```

2. **See your MP4 files:**
   - Use ↑/↓ to pick one

3. **Select video:**
   - Press Enter

4. **Adjust settings:**
   - Quality: Use ←/→ to change
   - Aspect Ratio: Use ↑/↓ to adjust (try 0.55 for 1440p!)
   - Pure @: Press Space to toggle

5. **Play:**
   - Press Enter

6. **During playback:**
   - Space = pause
   - Q = quit

7. **Loop:**
   - After video, press any key to play another!

---

## Troubleshooting

**Q: "No MP4 files found"**
- A: Put MP4 files in the same folder as vidterm.py
- Or press D to download from URL

**Q: "Aspect ratio not filling my 1440p screen"**
- A: In settings, go to "Aspect Ratio" and press ↑ several times
- Try 0.55 to 0.65 for fullscreen
- Use arrow keys (↑/↓) to fine-tune

**Q: "Downloaded file won't play"**
- A: Make sure ffmpeg is installed: `choco install ffmpeg`

**Q: "Download stuck"**
- A: Press Q and try again
- Or download lower quality: Select 360p or 480p

---

## Keyboard Cheat Sheet

### Video Selector
```
↑/↓     Navigate videos
Enter   Play selected
D       Download from URL
Q       Quit
```

### Settings Menu
```
↑/↓     Navigate or adjust aspect ratio
←/→     Change quality
Space   Toggle Pure @ mode
Enter   Play video
Q       Back to video list
```

### During Playback
```
Space   Pause / Resume
Q       Quit
ESC     Quit
```

---

## Tips & Tricks

1. **Slow playback?**
   - Use 360p quality
   - Close other apps

2. **Video looks squashed?**
   - Increase aspect ratio (0.5 → 0.6)

3. **Want pure @ characters?**
   - In settings, toggle "Pure @ Mode" with Space

4. **Want to play multiple videos in a row?**
   - Just keep pressing Enter!
   - The menu loops after each video

5. **Favorite settings?**
   - The app remembers your last choices within a session
   - Can be modified later for permanent defaults in code

---

Enjoy your interactive terminal video player! 🎬✨
