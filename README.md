# voice-record

Cantonese voice transcription using OpenAI Whisper Large model.

🚀 **New!** [Quick Start Guide](QUICKSTART.md) - Get started in 5 minutes!

## 🎯 Overview

This repository provides multiple ways to transcribe voice recordings to Cantonese text using OpenAI's Whisper Large model with GPU acceleration.

## 🚀 Three Ways to Transcribe:

### Option 1: Google Colab - Manual (Recommended ⭐)

Perfect for on-demand transcription with GPU acceleration.

1. **Open the notebook in Google Colab:**
   - Upload `transcribe_cantonese.ipynb` to Google Colab, or
   - Click: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kevinzjpeng/voice-record/blob/main/transcribe_cantonese.ipynb)

2. **Enable GPU** → Runtime → Change runtime type → GPU

3. **Run all cells** → Upload files when prompted

4. **Download transcripts** automatically

**Advantages:**
- ⚡ Fast with free GPU
-  Interactive and immediate
- 📱 Works from any device

### Option 2: Google Colab - Semi-Automated 🚀

GitHub Actions notifies you, Colab does the transcription automatically.

1. **Setup** (one-time):
   - Push audio files to `voice-record/`
   - GitHub Actions triggers workflow
   - Opens notebook with files pre-loaded

2. **Usage:**
   ```bash
   git add voice-record/your-audio.mp3
   git commit -m "Add recording"
   git push
   ```

3. **Transcribe:**
   - Click Colab link from GitHub Actions
   - Files are already loaded from your repo
   - Run cells, transcripts auto-commit back

**Use the automated notebook:** `transcribe_colab_automated.ipynb`

**Advantages:**
- 🔄 Semi-automated workflow
- 🎯 Files pre-loaded from repo
- ⚡ GPU acceleration
- 📤 Auto-commit results

📖 **Detailed setup:** See [COLAB_SETUP.md](COLAB_SETUP.md)

---

## 📂 Repository Files

- **`transcribe_cantonese.ipynb`** - Manual Colab notebook
- **`transcribe_colab_automated.ipynb`** - GitHub-integrated notebook  
- **`colab_webhook_server.ipynb`** - Webhook server for full automation
- **`QUICKSTART.md`** - Quick setup guide
- **`COLAB_SETUP.md`** - Detailed setup instructions
- **`WORKFLOW.md`** - Architecture and workflow diagrams

---### Option 3: GitHub Actions (Fully Automatic)

Automatically transcribe when you push files (no GPU, slower).

#### Steps:

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

