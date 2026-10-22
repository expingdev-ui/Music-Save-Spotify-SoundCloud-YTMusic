# 🎵 Music Save | Spotify, SoundCloud, YTMusic

**Music Save** is a user-friendly Telegram bot designed to download music and save it in **MP3** format directly via a URL link.

## 🚀 Features

* 🟢 **Spotify**: Automatically recognizes tracks via web link (extracting HTML metadata) and locates the audio version.
* 🟠 **SoundCloud**: Direct high-quality track downloads.
* 🔴 **YouTube Music**: Fast audio extraction and conversion.
* ⚡ **MP3 Conversion**: Automatic file audio conversion using `FFmpeg` (192 kbps).
* 🧹 **Auto-cleanup**: Instant removal of temporary files from the server right after sending them to the user.
* 💬 **Interactive Menu**: Clean interface powered by inline keyboards.

## 🛠 Tech Stack

* **Language**: Python 3.11+
* **Bot Framework**: [aiogram 3.x](https://github.com/aiogram/aiogram)
* **Audio Downloader**: [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* **Media Processing**: [FFmpeg](https://ffmpeg.org/)

## 📋 Prerequisites

Before running the bot, make sure you have the following installed on your system:

1. **Python 3.11** or higher.
2. **FFmpeg** (required by `yt-dlp` to convert downloaded audio to MP3).

### Installing FFmpeg via Terminal:

* **Windows**:
  * Via **Winget** (built-in on Windows 10/11):
    ```bash
    winget install ffmpeg
    ```
  * Via **Chocolatey**:
    ```bash
    choco install ffmpeg
    ```
  * Via **Scoop**:
    ```bash
    scoop install ffmpeg
    ```

* **Ubuntu/Debian**:
  ```bash
  sudo apt update && sudo apt install ffmpeg
  ```

* **macOS**:
  ```bash
  brew install ffmpeg
  ```

> ⚠️ **Note:** Installing via package managers automatically adds `FFmpeg` to your system `PATH`. Restart your terminal after installation.

## 📦 Installation & Setup

1. **Clone the repository or download the source code:**
   ```bash
   git clone https://github.com/your-username/music-save-bot.git
   cd music-save-bot
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   # On Linux/macOS:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install aiogram yt-dlp
   ```

4. **Configure application settings:**
   Replace the `TOKEN` variable in `musicsave.py` with your Telegram Bot token obtained from BotFather:
   ```python
   TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
   ADMIN_USERNAME = "your_username"
   ```

5. **Run the bot:**
   ```bash
   python musicsave.py
   ```

## 📱 How to Use

1. Open a chat with your bot in Telegram and send the `/start` command.
2. Copy a track link from **Spotify**, **SoundCloud**, or **YouTube Music**.
3. Send the link to the bot.
4. Wait for processing and receive your **MP3** file!

## ⚠️ Disclaimer

This project is created strictly for educational and informational purposes. The author is not responsible for any misuse of the application that violates copyright laws or third-party service Terms of Service.