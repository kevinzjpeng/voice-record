# 🎯 Quick Start Guide - Remote Colab Transcription

This guide will help you set up **automated Cantonese transcription** triggered by GitHub, executed on Google Colab with GPU.

## 📦 What You Have

Your repository now includes:

1. **`transcribe_cantonese.ipynb`** - Manual Colab notebook
2. **`transcribe_colab_automated.ipynb`** - Semi-automated notebook (loads from GitHub)
3. **`colab_webhook_server.ipynb`** - Webhook server for full automation
4. **GitHub Actions workflows** - Automation triggers

## 🚀 Choose Your Setup

### Option A: Quick & Easy (Recommended for most users)

**Manual Colab - No setup required!**

1. Open [transcribe_cantonese.ipynb](transcribe_cantonese.ipynb) in Google Colab
2. Enable GPU (Runtime → Change runtime type → GPU)
3. Run all cells
4. Upload your audio files
5. Download transcripts

**Time: 2-5 minutes per file**

---

### Option B: Semi-Automated (Best balance)

**Colab loads files from GitHub automatically**

#### Setup (One-time, 5 minutes):

1. **Open the automated notebook:**
   - Upload [transcribe_colab_automated.ipynb](transcribe_colab_automated.ipynb) to Colab
   - Or use: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kevinzjpeng/voice-record/blob/main/transcribe_colab_automated.ipynb)

2. **Configure the notebook:**
   ```python
   GITHUB_REPO = "kevinzjpeng/voice-record"  # Your repo
   USE_MANUAL_UPLOAD = False  # Important!
   AUTO_COMMIT = True  # To push results back
   ```

3. **Add GitHub token (optional, for auto-commit):**
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Generate token with `repo` scope
   - Add to notebook: `GITHUB_TOKEN = "your_token_here"`

#### Usage:

```bash
# Add audio file
cp recording.mp3 voice-record/
git add voice-record/recording.mp3
git commit -m "Add recording"
git push

# Open Colab notebook → Run all cells
# Files are already loaded!
# Transcripts auto-commit back to GitHub
```

**Time: 5 minutes setup, then 2-3 minutes per transcription**

---

### Option C: Fully Automated (Advanced)

**GitHub triggers Colab automatically**

#### Setup (One-time, 10 minutes):

1. **Start the webhook server:**
   - Open [colab_webhook_server.ipynb](colab_webhook_server.ipynb) in Colab
   - Enable GPU
   - Configure your repo details
   - Run all cells
   - **Copy the webhook URL** that appears

2. **Add GitHub Secrets:**
   - Go to your repo → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Add:
     - Name: `COLAB_WEBHOOK_URL`
     - Value: Your webhook URL from step 1
   - (Optional) Add security:
     - Name: `WEBHOOK_SECRET`
     - Value: Create a random secret key

3. **Keep Colab running:**
   - Don't close the Colab tab
   - Server will run for ~12 hours

#### Usage:

```bash
# Just push audio files!
cp recording.mp3 voice-record/
git add voice-record/recording.mp3
git commit -m "Add recording"
git push

# GitHub Actions → Triggers Colab
# Colab transcribes with GPU
# Results auto-commit back
# Done! 🎉
```

**Time: 10 minutes setup, then fully automatic!**

**⚠️ Limitations:**
- Colab session expires after 12 hours
- Must keep browser tab open
- Free tier has usage limits

---

## 📊 Comparison

| Option | Speed | Setup | Automation | Best For |
|--------|-------|-------|------------|----------|
| A: Manual | ⚡⚡⚡ | None | ❌ | Occasional use |
| B: Semi-Auto | ⚡⚡⚡ | 5 min | ⚡ | Regular use |
| C: Full-Auto | ⚡⚡⚡ | 10 min | ⚡⚡⚡ | Power users |

## 🎓 Next Steps

1. **Start with Option A** to test it out
2. **Upgrade to Option B** if you use it regularly
3. **Try Option C** if you want full automation

## 📚 Need Help?

- **Detailed setup:** See [COLAB_SETUP.md](COLAB_SETUP.md)
- **Workflow diagrams:** See [WORKFLOW.md](WORKFLOW.md)
- **Troubleshooting:** Check GitHub Actions logs

## 🎉 You're Ready!

Pick an option above and start transcribing your Cantonese recordings with GPU acceleration!

