# voice-record

Automatic Cantonese voice transcription using GitHub Actions and OpenAI Whisper Large.

## 🎯 Overview

This repository automatically transcribes voice recordings to Cantonese text using OpenAI's Whisper Large model. Simply upload your audio files, and GitHub Actions will handle the transcription for you!

## 🚀 How to Use

1. **Add your voice recording** to the `voice-record/` directory:
   ```bash
   # Copy your audio file to the voice-record directory
   cp your-audio-file.mp3 voice-record/
   ```

2. **Commit and push** to GitHub:
   ```bash
   git add voice-record/your-audio-file.mp3
   git commit -m "Add new voice recording"
   git push
   ```

3. **Wait for GitHub Actions** to process your file (this may take 5-10 minutes)
   - Go to the "Actions" tab in your GitHub repository
   - Watch the transcription workflow run

4. **Get your transcript** - the workflow will automatically:
   - Transcribe your audio to Cantonese text
   - Create a `.txt` file with the same name as your audio file
   - Commit the transcript back to the repository

## 📁 Supported Audio Formats

- MP3 (`.mp3`)
- WAV (`.wav`)
- M4A (`.m4a`)
- FLAC (`.flac`)
- OGG (`.ogg`)

## 📝 Output Format

Each transcript file includes:
- Full transcript text
- Detailed segments with timestamps
- Format: `[HH:MM:SS -> HH:MM:SS] transcript text`

Example:
```
Transcript of: recording.mp3
Language: Cantonese/Chinese
============================================================

你好，今天天氣真好。

============================================================
Detailed segments:

[00:00:00 -> 00:00:03] 你好，今天天氣真好。
```

## 🔧 Technical Details

- **Model**: OpenAI Whisper Large
- **Language**: Chinese (Cantonese)
- **Platform**: GitHub Actions (Ubuntu)
- **Python Version**: 3.10

## 📋 Requirements

No local setup required! Everything runs on GitHub Actions. However, if you want to run locally:

```bash
# Install dependencies
pip install openai-whisper torch

# Install ffmpeg (required by Whisper)
# macOS:
brew install ffmpeg

# Ubuntu/Debian:
sudo apt-get install ffmpeg

# Run transcription
python scripts/transcribe.py
```

## ⚙️ Workflow Configuration

The workflow is triggered when audio files are pushed to the `voice-record/` directory. It:
1. Checks out the repository
2. Sets up Python 3.10
3. Installs ffmpeg and Whisper
4. Transcribes new/modified audio files
5. Commits transcripts back to the repository

## 📄 License

Feel free to use and modify as needed!

