# voice-record

Cantonese voice transcription using OpenAI Whisper Large model.

🚀 **New!** [Quick Start Guide](QUICKSTART.md) - Get started in 5 minutes!

## 🎯 Overview

This repository provides multiple ways to transcribe voice recordings to Cantonese text and YouTube videos using OpenAI's Whisper Large model with GPU acceleration. Now with AI-powered summarization!

## 🚀 Transcription Options:

### 🎬 YouTube Video Transcription (NEW!)

Transcribe any YouTube video with optional AI summary - perfect for lectures, tutorials, podcasts!

1. **Open the notebook in Google Colab:**
   - Upload `transcribe_youtube.ipynb` to Google Colab, or
   - Click: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kevinzjpeng/voice-record/blob/main/transcribe_youtube.ipynb)

2. **Enable GPU** (optional) → Runtime → Change runtime type → GPU

3. **Run the cell** → Paste YouTube URL when prompted

4. **Optional AI Summary:**
   - Get a free API key from [Groq](https://console.groq.com/keys)
   - Paste when prompted for intelligent summary
   - Or press Enter to skip and just get transcript

5. **Download** transcript (+ summary) automatically

**Features:**
- ✨ AI-powered summary (optional, using Llama 3.3 70B)
- 🎯 Auto-detects language
- ⏱️ Timestamped segments
- 📥 Instant download
- 🧹 Auto-cleanup

---

## 🎙️ Audio File Transcription:

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

- **`transcribe_youtube.ipynb`** - 🎬 NEW! YouTube video transcription with AI summary
- **`transcribe_cantonese.ipynb`** - Manual Colab notebook for audio files
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

**For audio files:**
- MP3 (`.mp3`)
- WAV (`.wav`)
- M4A (`.m4a`)
- FLAC (`.flac`)
- OGG (`.ogg`)

**For YouTube:**
- Any valid YouTube URL
- Auto-extracts audio in best quality
- Works with videos of any length

## 📝 Output Format

Each transcript file includes:
- Full transcript text
- Auto-detected language
- Detailed segments with timestamps
- **NEW:** Optional AI summary (overview, key points, takeaways)
- Format: `[HH:MM:SS -> HH:MM:SS] transcript text`

**Example with AI Summary:**
```
YouTube Transcript
URL: https://youtube.com/watch?v=...
Language: English
==============================

🧠 AI SUMMARY
==============================
This video discusses... [AI-generated overview]

Key Points:
• Point 1
• Point 2
• Point 3

Main Takeaways:
...

==============================

📝 FULL TRANSCRIPT
==============================
Hello everyone, today we're going to...

==============================
⏱️ DETAILED SEGMENTS
==============================
[00:00:00 → 00:00:05] Hello everyone, today we're going to...
[00:00:05 → 00:00:12] First, let's talk about...
```

**Example for audio files:**
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
- **Language**: Auto-detect (or specify Cantonese/Chinese)
- **AI Summary**: Groq API with Llama 3.3 70B (optional, free)
- **Platform**: Google Colab (GPU) or GitHub Actions (CPU)
- **Python Version**: 3.10+

## 🤖 AI Summary Features

The YouTube transcription notebook includes optional AI-powered summarization:

- **Provider:** Groq (free API)
- **Model:** Llama 3.3 70B Versatile
- **Speed:** ~30 seconds per summary
- **Output:** 
  - Brief overview (2-3 sentences)
  - Key points (bullet format)
  - Main takeaways
- **Setup:** Get free API key at [console.groq.com/keys](https://console.groq.com/keys)

## 📋 Requirements

No local setup required! Everything runs on Google Colab or GitHub Actions. 

However, if you want to run locally:

```bash
# Install dependencies
pip install openai-whisper torch yt-dlp groq

# Install ffmpeg (required by Whisper)
# macOS:
brew install ffmpeg

# Ubuntu/Debian:
sudo apt-get install ffmpeg

# Transcribe audio file
python scripts/transcribe.py

# For YouTube videos with AI summary, see transcribe_youtube.ipynb
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

