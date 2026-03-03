#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Terminal ASCII Video Player - Interactive CLI

Run with: python vidterm.py
- Select videos from folder using arrow keys
- Adjust settings interactively
- Play videos as ASCII art

Supports: YouTube, X (Twitter), Twitch, local MP4 files
"""

__version__ = "2.0.0"

import os
import sys
import time
import threading
import tempfile
import shutil
import pathlib
from typing import Optional, List, Tuple

# Third-party imports
try:
    import cv2
    import numpy as np
    from PIL import Image
    import colorama
except ImportError as e:
    sys.stderr.write(f"Missing required package: {e.name}\n")
    sys.stderr.write("Install with: pip install yt-dlp opencv-python Pillow colorama\n")
    sys.exit(1)

try:
    import yt_dlp
except ImportError:
    sys.stderr.write("Missing required package: yt-dlp\n")
    sys.stderr.write("Install with: pip install yt-dlp\n")
    sys.exit(1)

if os.name != 'nt':
    sys.stderr.write("This tool is designed for Windows. Exiting.\n")
    sys.exit(1)

import msvcrt

# === CONSTANTS ===

ASCII_RAMP_SIMPLE = "@"
ASCII_RAMP_GRAD = " .:-=+*#%@"
CHAR_ASPECT_CORRECTION = 0.45

CURSOR_HOME = "\033[H"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CLEAR_SCREEN = "\033[2J"
RESET_COLOR = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"


# === UI UTILITIES ===

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    WHITE = "\033[97m"
    RESET = "\033[0m"
    DIM = "\033[2m"
    BOLD = "\033[1m"


def clear():
    sys.stdout.write(CLEAR_SCREEN)
    sys.stdout.flush()


def print_centered(text: str, width: Optional[int] = None) -> None:
    """Print text centered in the terminal."""
    if width is None:
        width = shutil.get_terminal_size().columns
    padding = max(0, (width - len(text)) // 2)
    print(" " * padding + text)


def print_header(title: str) -> None:
    """Print a formatted header."""
    width = shutil.get_terminal_size().columns
    print(f"{Colors.CYAN}{'═' * width}{Colors.RESET}")
    print_centered(f"{Colors.CYAN}{BOLD}{title}{Colors.RESET}")
    print(f"{Colors.CYAN}{'═' * width}{Colors.RESET}")
    print()


def getch_no_echo() -> str:
    """Get a character without echoing it."""
    return msvcrt.getch().decode('utf-8', errors='ignore')


def get_arrow_input() -> Optional[str]:
    """Get arrow key input. Returns 'up', 'down', 'enter', or None."""
    if msvcrt.kbhit():
        key = msvcrt.getch()

        # Handle extended keys
        if key == b'\xe0' or key == b'\x00':
            key2 = msvcrt.getch()
            if key2 == b'H':  # Up arrow
                return 'up'
            elif key2 == b'P':  # Down arrow
                return 'down'
        elif key == b'\r':  # Enter
            return 'enter'
        elif key == b'q' or key == b'Q' or key == b'\x1b':  # Q or Escape
            return 'quit'
        elif key == b' ':  # Space
            return 'space'

    return None


# === VIDEO UTILITIES ===

def find_mp4_files(folder: str = ".") -> List[pathlib.Path]:
    """Find all MP4 files in a folder."""
    path = pathlib.Path(folder)
    if not path.exists():
        return []

    mp4s = sorted(path.glob("*.mp4"))
    return mp4s


class VideoDownloadError(Exception):
    pass


class VideoDownloader:
    """Downloads video from YouTube, X, Twitch, etc."""

    def __init__(self, quality: str = "480p"):
        self.quality = quality
        self._has_ffmpeg = self._check_ffmpeg()

    def download(self, url: str) -> pathlib.Path:
        """Download video to temp file and return path."""
        tmp_dir = pathlib.Path(tempfile.mkdtemp(prefix="vidterm_"))
        out_tmpl = str(tmp_dir / "video.%(ext)s")

        # Try to determine format based on FFmpeg availability
        if self._has_ffmpeg:
            fmt = self._get_quality_format_with_ffmpeg()
        else:
            fmt = self._get_quality_format_no_ffmpeg()

        ydl_opts = {
            "format": fmt,
            "outtmpl": out_tmpl,
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
        }

        # Only set merge_output_format if FFmpeg is available
        if self._has_ffmpeg:
            ydl_opts["merge_output_format"] = "mp4"

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(url, download=True)
                actual = self._find_output_file(tmp_dir)
                return actual
        except Exception as e:
            self.cleanup(tmp_dir)
            raise VideoDownloadError(f"Download failed: {e}") from e

    def _check_ffmpeg(self) -> bool:
        """Check if FFmpeg is installed."""
        try:
            import subprocess
            subprocess.run(["ffmpeg", "-version"], capture_output=True, timeout=2)
            return True
        except Exception:
            return False

    def _get_quality_format_with_ffmpeg(self) -> str:
        """Get format string when FFmpeg is available (best quality)."""
        quality_map = {
            "360p": "bestvideo[height<=360][ext=mp4]+bestaudio/best[height<=360]",
            "480p": "bestvideo[height<=480][ext=mp4]+bestaudio/best[height<=480]",
            "720p": "bestvideo[height<=720][ext=mp4]+bestaudio/best[height<=720]",
            "1080p": "bestvideo[height<=1080][ext=mp4]+bestaudio/best[height<=1080]",
            "best": "bestvideo[ext=mp4]+bestaudio/best",
        }
        return quality_map.get(self.quality, quality_map["480p"])

    def _get_quality_format_no_ffmpeg(self) -> str:
        """Get format string when FFmpeg is NOT available (fallback to single file)."""
        quality_map = {
            "360p": "best[height<=360][ext=mp4]",
            "480p": "best[height<=480][ext=mp4]",
            "720p": "best[height<=720][ext=mp4]",
            "1080p": "best[height<=1080][ext=mp4]",
            "best": "best[ext=mp4]",
        }
        return quality_map.get(self.quality, quality_map["480p"])

    @staticmethod
    def _find_output_file(tmp_dir: pathlib.Path) -> pathlib.Path:
        video_extensions = {".mp4", ".mkv", ".webm", ".avi", ".mov"}
        for f in tmp_dir.iterdir():
            if f.suffix.lower() in video_extensions:
                return f
        raise VideoDownloadError("No video file found after download.")

    @staticmethod
    def cleanup(tmp_dir: pathlib.Path):
        shutil.rmtree(str(tmp_dir), ignore_errors=True)


# === PLAYBACK STATE ===

class PlaybackState:
    """Thread-safe playback state."""

    def __init__(self):
        self._paused = threading.Event()
        self._quit = threading.Event()
        self.fps = 30.0
        self.width = 80
        self.height = 24
        self._lock = threading.Lock()

    def toggle_pause(self):
        if self._paused.is_set():
            self._paused.clear()
        else:
            self._paused.set()

    def request_quit(self):
        self._quit.set()

    @property
    def is_paused(self) -> bool:
        return self._paused.is_set()

    @property
    def should_quit(self) -> bool:
        return self._quit.is_set()


# === FRAME CONVERTER ===

class FrameConverter:
    """Converts frames to ASCII."""

    def __init__(self, ramp: str = ASCII_RAMP_GRAD, aspect_correction: float = CHAR_ASPECT_CORRECTION):
        self.ramp = ramp
        self.ramp_len = len(ramp)
        self.aspect_correction = aspect_correction

    def convert(self, frame_bgr: np.ndarray, term_cols: int, term_rows: int) -> str:
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

        display_rows = term_rows - 1
        target_cols = term_cols
        target_rows = max(1, int(display_rows * self.aspect_correction))

        pil_img = Image.fromarray(gray)
        resized = pil_img.resize((target_cols, target_rows), resample=Image.LANCZOS)
        pixels = list(resized.getdata())

        ascii_chars = [self._brightness_to_char(p) for p in pixels]

        rows = []
        for r in range(target_rows):
            row_chars = ascii_chars[r * target_cols : (r + 1) * target_cols]
            row_str = "".join(row_chars)
            rows.append(row_str)

        padding = display_rows - target_rows
        frame_str = "\n".join(rows) + "\n" * (padding + 1)

        return frame_str

    def _brightness_to_char(self, value: int) -> str:
        idx = int((255 - value) / 255 * (self.ramp_len - 1))
        idx = min(idx, self.ramp_len - 1)
        return self.ramp[idx]


# === TERMINAL RENDERER ===

class TerminalRenderer:
    """Renders frames to terminal."""

    def __init__(self, state: PlaybackState):
        self.state = state
        colorama.init()

    def setup(self):
        sys.stdout.write(CLEAR_SCREEN + HIDE_CURSOR)
        sys.stdout.flush()

    def render_frame(self, frame_str: str, frame_num: int, total_frames: int) -> None:
        elapsed_sec = frame_num / self.state.fps if self.state.fps > 0 else 0
        status = self._build_status(frame_num, total_frames, elapsed_sec, paused=False)

        out = CURSOR_HOME + frame_str + status
        sys.stdout.write(out)
        sys.stdout.flush()

    def render_paused_overlay(self, frame_str: str, frame_num: int, total_frames: int) -> None:
        elapsed_sec = frame_num / self.state.fps if self.state.fps > 0 else 0
        status = self._build_status(frame_num, total_frames, elapsed_sec, paused=True)

        out = CURSOR_HOME + frame_str + status
        sys.stdout.write(out)
        sys.stdout.flush()

    def _build_status(self, frame_num: int, total_frames: int, elapsed: float, paused: bool = False) -> str:
        term_cols = self.state.width
        pause_str = " [PAUSED]" if paused else ""

        elapsed_min = int(elapsed // 60)
        elapsed_sec = int(elapsed % 60)
        total_sec = total_frames / self.state.fps if self.state.fps > 0 else 0
        total_min = int(total_sec // 60)
        total_secs = int(total_sec % 60)

        elapsed_fmt = f"{elapsed_min:02d}:{elapsed_sec:02d}"
        total_fmt = f"{total_min:02d}:{total_secs:02d}"

        status = f" {elapsed_fmt}/{total_fmt}  Frame {frame_num}/{total_frames}{pause_str}  [SPACE=pause Q=quit]"

        return status[: term_cols].ljust(term_cols)

    def teardown(self):
        sys.stdout.write(SHOW_CURSOR + RESET_COLOR + "\n")
        sys.stdout.flush()
        colorama.deinit()


# === KEYBOARD LISTENER ===

def keyboard_listener(state: PlaybackState) -> None:
    """Background thread for keyboard input."""
    while not state.should_quit:
        if msvcrt.kbhit():
            key = msvcrt.getch()

            if key in (b"\x00", b"\xe0"):
                msvcrt.getch()
                continue

            if key == b" ":
                state.toggle_pause()
            elif key in (b"q", b"Q", b"\x1b"):
                state.request_quit()

        time.sleep(0.01)


# === PLAYER ===

class Player:
    """Main video player."""

    def __init__(self, video_path: pathlib.Path, quality: str = "480p", pure_at: bool = False, aspect_ratio: float = CHAR_ASPECT_CORRECTION):
        self.video_path = video_path
        self.quality = quality
        self.pure_at = pure_at
        self.aspect_ratio = aspect_ratio

        self.state = PlaybackState()
        self.renderer = TerminalRenderer(self.state)
        self.converter = FrameConverter(
            ramp=ASCII_RAMP_SIMPLE if pure_at else ASCII_RAMP_GRAD,
            aspect_correction=aspect_ratio
        )
        self._cap: Optional[cv2.VideoCapture] = None
        self._tmp_dir: Optional[pathlib.Path] = None
        self._last_frame_str = ""

    def play_url(self, url: str) -> bool:
        """Download and play a URL."""
        print(f"\n{Colors.YELLOW}Downloading: {url}{Colors.RESET}")
        print("(This may take a moment...)")

        downloader = VideoDownloader(quality=self.quality)

        # Notify about FFmpeg status
        if not downloader._has_ffmpeg:
            print(f"{Colors.YELLOW}Note: FFmpeg not found. Using fallback quality.{Colors.RESET}")
            print(f"      Install with: choco install ffmpeg")
            print()

        try:
            video_path = downloader.download(url)
            self._tmp_dir = video_path.parent
            print(f"{Colors.GREEN}Downloaded!{Colors.RESET}")
            time.sleep(1)
            return self._play_phase(video_path)
        except VideoDownloadError as e:
            print(f"{Colors.RED}Error: {e}{Colors.RESET}")
            print(f"{Colors.YELLOW}If this is a merge error, try installing FFmpeg:{Colors.RESET}")
            print(f"  choco install ffmpeg")
            return False

    def play_local(self) -> bool:
        """Play local MP4 file."""
        return self._play_phase(self.video_path)

    def _play_phase(self, video_path: pathlib.Path) -> bool:
        """Play video from file."""
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            print(f"{Colors.RED}Cannot open video file{Colors.RESET}")
            return False

        self._cap = cap
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 30.0
        self.state.fps = fps

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames <= 0:
            total_frames = 1

        # Start keyboard listener
        kb_thread = threading.Thread(target=keyboard_listener, args=(self.state,), daemon=True)
        kb_thread.start()

        self.renderer.setup()
        self._update_terminal_size()

        frame_duration = 1.0 / fps
        frame_num = 0

        try:
            while not self.state.should_quit:
                self._update_terminal_size()

                if self.state.is_paused:
                    self.renderer.render_paused_overlay(self._last_frame_str, frame_num, total_frames)
                    time.sleep(0.05)
                    continue

                frame_start = time.perf_counter()

                ret, frame_bgr = cap.read()
                if not ret:
                    break

                frame_num += 1
                frame_str = self.converter.convert(frame_bgr, self.state.width, self.state.height)
                self._last_frame_str = frame_str

                self.renderer.render_frame(frame_str, frame_num, total_frames)

                elapsed = time.perf_counter() - frame_start
                sleep_needed = frame_duration - elapsed
                if sleep_needed > 0:
                    time.sleep(sleep_needed)

        finally:
            self._cleanup()

        return True

    def _update_terminal_size(self):
        size = shutil.get_terminal_size(fallback=(80, 24))
        self.state.width = size.columns
        self.state.height = size.lines

    def _cleanup(self):
        if self._cap:
            self._cap.release()
            self._cap = None
        self.renderer.teardown()
        if self._tmp_dir:
            VideoDownloader.cleanup(self._tmp_dir)
            self._tmp_dir = None


# === INTERACTIVE MENUS ===

class VideoSelector:
    """Interactive video selection menu."""

    def __init__(self):
        self.mp4_files = find_mp4_files()
        self.selected = 0

    def show(self) -> Optional[pathlib.Path]:
        """Show selection menu. Returns selected file or None."""
        needs_redraw = True
        while True:
            if needs_redraw:
                clear()
                print_header("TERMINAL ASCII VIDEO PLAYER")

                if not self.mp4_files:
                    print(f"{Colors.RED}No MP4 files found in current folder.{Colors.RESET}\n")
                    print("Options:")
                    print("  1. Download from URL")
                    print("  2. Exit")
                    print()
                    choice = getch_no_echo()
                    if choice == '1':
                        return self._download_from_url()
                    else:
                        return None

                print(f"{Colors.CYAN}Local MP4 Files:{Colors.RESET}\n")

                for i, f in enumerate(self.mp4_files):
                    prefix = f"{Colors.GREEN}▶ {Colors.RESET}" if i == self.selected else "  "
                    size_mb = f.stat().st_size / (1024 * 1024)
                    print(f"{prefix}{i+1}. {f.name} ({size_mb:.1f} MB)")

                print()
                print(f"{Colors.CYAN}Options:{Colors.RESET}")
                print("  ↑/↓  Navigate")
                print("  Enter  Play selected")
                print("  D  Download from URL")
                print("  Q  Exit")
                print()
                needs_redraw = False

            if msvcrt.kbhit():
                key_byte = msvcrt.getch()

                # Handle extended keys (arrows)
                if key_byte == b'\xe0' or key_byte == b'\x00':
                    if msvcrt.kbhit():
                        arrow = msvcrt.getch()
                        if arrow == b'H':  # Up arrow
                            self.selected = (self.selected - 1) % len(self.mp4_files)
                            needs_redraw = True
                        elif arrow == b'P':  # Down arrow
                            self.selected = (self.selected + 1) % len(self.mp4_files)
                            needs_redraw = True

                elif key_byte == b'\r':  # Enter
                    return self.mp4_files[self.selected]
                elif key_byte in (b'q', b'Q', b'\x1b'):  # Q or Escape
                    return None
                elif key_byte in (b'd', b'D'):  # D for download
                    return self._download_from_url()

            time.sleep(0.1)

    def _download_from_url(self) -> Optional[pathlib.Path]:
        """Prompt user for URL to download."""
        clear()
        print_header("DOWNLOAD FROM URL")
        print("Supported: YouTube, X (Twitter), Twitch, Instagram, TikTok, etc.\n")
        url = input(f"{Colors.CYAN}Paste video URL:{Colors.RESET}\n> ").strip()

        if not url:
            return None

        return ("url", url)  # Return tuple to indicate URL mode


class SettingsMenu:
    """Interactive settings menu with edit mode."""

    def __init__(self):
        self.quality = "480p"
        self.aspect_ratio = 0.45
        self.pure_at = False
        self.selected = 0

    def show(self) -> Tuple[str, float, bool]:
        """Show settings menu. Returns (quality, aspect_ratio, pure_at)."""
        needs_redraw = True
        while True:
            if needs_redraw:
                self._draw_menu()
                needs_redraw = False

            if msvcrt.kbhit():
                key_byte = msvcrt.getch()

                # Handle extended keys (arrows)
                if key_byte == b'\xe0' or key_byte == b'\x00':
                    if msvcrt.kbhit():
                        arrow = msvcrt.getch()

                        if arrow == b'H':  # Up arrow
                            self.selected = (self.selected - 1) % 4
                            needs_redraw = True
                        elif arrow == b'P':  # Down arrow
                            self.selected = (self.selected + 1) % 4
                            needs_redraw = True

                elif key_byte == b'\r':  # Enter
                    if self.selected == 0:
                        self._edit_quality()
                        needs_redraw = True
                    elif self.selected == 1:
                        self._edit_aspect_ratio()
                        needs_redraw = True
                    elif self.selected == 2:
                        self._edit_pure_at()
                        needs_redraw = True
                    elif self.selected == 3:  # PLAY button
                        return (self.quality, self.aspect_ratio, self.pure_at)

                elif key_byte in (b'q', b'Q', b'\x1b'):  # Q or Escape
                    return None

            time.sleep(0.15)

    def _draw_menu(self):
        """Draw the settings menu."""
        clear()
        print_header("VIDEO SETTINGS")
        print()

        # Quality setting
        prefix = f"{Colors.GREEN}▶ {Colors.RESET}" if self.selected == 0 else "  "
        print(f"{prefix}1. Quality: {Colors.YELLOW}{self.quality}{Colors.RESET}")

        # Aspect Ratio setting
        prefix = f"{Colors.GREEN}▶ {Colors.RESET}" if self.selected == 1 else "  "
        print(f"{prefix}2. Aspect Ratio: {Colors.YELLOW}{self.aspect_ratio:.2f}{Colors.RESET}")

        # Pure @ Mode setting
        prefix = f"{Colors.GREEN}▶ {Colors.RESET}" if self.selected == 2 else "  "
        status = f"{Colors.GREEN}ON{Colors.RESET}" if self.pure_at else f"{Colors.RED}OFF{Colors.RESET}"
        print(f"{prefix}3. Pure @ Mode: {status}")

        # PLAY button
        prefix = f"{Colors.GREEN}▶ {Colors.RESET}" if self.selected == 3 else "  "
        print(f"{prefix}{Colors.GREEN}{Colors.BOLD}4. ▶ PLAY VIDEO{Colors.RESET}")

        print()
        print(f"{Colors.CYAN}How to use:{Colors.RESET}")
        print("  ↑/↓        Select a setting or button")
        print("  Enter      Edit setting OR play video")
        print("  Q / ESC    Back to videos")
        print()
        print(f"{Colors.DIM}(Use arrow keys to navigate, press Enter to select){Colors.RESET}")

    def _edit_quality(self):
        """Edit quality setting."""
        qualities = ["360p", "480p", "720p", "1080p", "best"]
        idx = qualities.index(self.quality)

        while True:
            clear()
            print_header("EDIT QUALITY")
            print()

            for i, q in enumerate(qualities):
                prefix = f"{Colors.GREEN}▶ {Colors.RESET}" if i == idx else "  "
                print(f"{prefix}{q}")

            print()
            print(f"{Colors.CYAN}Use arrow keys to select, Enter to confirm, ESC to cancel{Colors.RESET}")
            print()

            if msvcrt.kbhit():
                key_byte = msvcrt.getch()

                if key_byte == b'\xe0' or key_byte == b'\x00':
                    if msvcrt.kbhit():
                        arrow = msvcrt.getch()
                        if arrow == b'H':  # Up
                            idx = (idx - 1) % len(qualities)
                        elif arrow == b'P':  # Down
                            idx = (idx + 1) % len(qualities)

                elif key_byte == b'\r':  # Enter
                    self.quality = qualities[idx]
                    return

                elif key_byte in (b'\x1b', b'q', b'Q'):  # Escape or Q
                    return

            time.sleep(0.1)

    def _edit_aspect_ratio(self):
        """Edit aspect ratio setting."""
        value = self.aspect_ratio

        while True:
            clear()
            print_header("EDIT ASPECT RATIO")
            print()
            print(f"Current: {Colors.YELLOW}{value:.2f}{Colors.RESET}")
            print()
            print(f"{Colors.CYAN}Aspect Ratio Guide:{Colors.RESET}")
            print("  0.30 - 0.40  = Wide (many columns)")
            print("  0.45         = Default (balanced)")
            print("  0.55 - 0.65  = ⭐ FULLSCREEN FOR 1440P")
            print("  0.70 - 0.90  = Very tall (maximize rows)")
            print("  0.95+        = MAXIMUM HEIGHT (try if still not full)")
            print()
            print(f"{Colors.CYAN}Controls:{Colors.RESET}")
            print("  ↑            Increase (+0.02)")
            print("  ↓            Decrease (-0.02)")
            print("  Enter        Confirm")
            print("  ESC / Q      Cancel")
            print()
            print(f"{Colors.DIM}Tip: For 1440p fullscreen, try 0.70-0.95{Colors.RESET}")
            print()

            if msvcrt.kbhit():
                key_byte = msvcrt.getch()

                if key_byte == b'\xe0' or key_byte == b'\x00':
                    if msvcrt.kbhit():
                        arrow = msvcrt.getch()
                        if arrow == b'H':  # Up
                            value = min(1.5, value + 0.02)
                        elif arrow == b'P':  # Down
                            value = max(0.2, value - 0.02)

                elif key_byte == b'\r':  # Enter
                    self.aspect_ratio = value
                    return

                elif key_byte in (b'\x1b', b'q', b'Q'):  # Escape or Q
                    return

            time.sleep(0.1)

    def _edit_pure_at(self):
        """Edit Pure @ mode setting."""
        value = self.pure_at

        while True:
            clear()
            print_header("EDIT PURE @ MODE")
            print()

            off_prefix = f"{Colors.GREEN}▶ {Colors.RESET}" if not value else "  "
            on_prefix = f"{Colors.GREEN}▶ {Colors.RESET}" if value else "  "

            print(f"{off_prefix}OFF - Grayscale ramp (more detail)")
            print(f"{on_prefix}ON  - Pure @ characters only (artistic)")
            print()
            print(f"{Colors.CYAN}Controls:{Colors.RESET}")
            print("  ↑/↓          Toggle")
            print("  Space        Toggle")
            print("  Enter        Confirm")
            print("  ESC / Q      Cancel")
            print()

            if msvcrt.kbhit():
                key_byte = msvcrt.getch()

                if key_byte == b'\xe0' or key_byte == b'\x00':
                    if msvcrt.kbhit():
                        arrow = msvcrt.getch()
                        if arrow in (b'H', b'P'):  # Up or Down
                            value = not value

                elif key_byte == b' ':  # Space
                    value = not value

                elif key_byte == b'\r':  # Enter
                    self.pure_at = value
                    return

                elif key_byte in (b'\x1b', b'q', b'Q'):  # Escape or Q
                    return

            time.sleep(0.1)


# === MAIN ===

def main():
    """Main entry point."""
    colorama.init()

    try:
        while True:
            # Video selection
            selector = VideoSelector()
            video_info = selector.show()

            if video_info is None:
                break

            # Settings
            settings_menu = SettingsMenu()
            result = settings_menu.show()

            if result is None:
                continue

            quality, aspect_ratio, pure_at = result

            # Play video
            try:
                if isinstance(video_info, tuple) and video_info[0] == "url":
                    # Download from URL
                    _, url = video_info
                    player = Player(None, quality=quality, pure_at=pure_at, aspect_ratio=aspect_ratio)
                    player.play_url(url)
                else:
                    # Play local file
                    player = Player(video_info, quality=quality, pure_at=pure_at, aspect_ratio=aspect_ratio)
                    player.play_local()
            except Exception as e:
                print(f"\n{Colors.RED}Error playing video: {e}{Colors.RESET}")
                time.sleep(2)

            print(f"\n{Colors.GREEN}Video finished. Press any key to continue...{Colors.RESET}")
            getch_no_echo()

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
    finally:
        colorama.deinit()


if __name__ == "__main__":
    main()
