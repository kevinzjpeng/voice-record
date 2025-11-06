# Remote Colab Execution Setup

This guide explains how to set up remote Colab execution triggered by GitHub Actions.

## 🎯 Solution Overview

Since Google Colab doesn't have a public API for remote execution, we offer three approaches:

### Approach 1: Manual Colab Execution (Simplest) ⭐ Recommended

1. When GitHub Actions detects new audio files, it creates an issue/comment
2. You click the Colab badge to open the notebook
3. Notebook automatically loads files from the repository
4. Results are pushed back automatically

### Approach 2: Self-Hosted Colab with ngrok (Advanced)

Keep a Colab session running with a webhook endpoint that GitHub Actions can call.

### Approach 3: Local Execution Fallback (Automatic)

If Colab isn't available, GitHub Actions runs Whisper locally (slower, no GPU).

---

## 🚀 Quick Setup (Approach 1 - Recommended)

### Step 1: Enable GitHub Actions

The workflow is already configured in `.github/workflows/trigger-colab.yml`

### Step 2: Add Audio Files

```bash
cp your-audio.mp3 voice-record/
git add voice-record/your-audio.mp3
git commit -m "Add new recording"
git push
```

### Step 3: Check Notifications

- GitHub Actions will create an issue with a link to transcribe
- Click the Colab badge in the issue
- The notebook will automatically load your audio files
- Run all cells to transcribe

### Step 4: Results Auto-Commit

The notebook will push transcripts back to your repository automatically.

---

## 🔧 Setup for Approach 2 (Advanced - ngrok webhook)

If you want fully automated Colab execution:

### 1. In Google Colab, run the webhook server:

```python
# Cell 1: Install dependencies
!pip install flask pyngrok

# Cell 2: Setup webhook
from flask import Flask, request
from pyngrok import ngrok
import os

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    data = request.json
    # Trigger transcription
    return {"status": "success"}

# Start ngrok tunnel
port = 5000
public_url = ngrok.connect(port)
print(f"Webhook URL: {public_url}/transcribe")

# Run Flask
app.run(port=port)
```

### 2. Add webhook URL to GitHub Secrets:

- Go to your repository Settings → Secrets and variables → Actions
- Add new secret: `COLAB_WEBHOOK_URL` = your ngrok URL

### 3. The GitHub Action will automatically call this webhook

---

## 📝 How It Works

1. **Audio file pushed** → Triggers GitHub Actions
2. **GitHub Actions**:
   - Detects new audio files
   - Tries to trigger Colab (if webhook configured)
   - Falls back to local execution if needed
3. **Colab/Local** → Transcribes audio
4. **Results** → Committed back to repository

---

## 🔐 Required Secrets (Optional)

Add these in GitHub Settings → Secrets and variables → Actions:

- `COLAB_WEBHOOK_URL`: Your ngrok webhook URL (for Approach 2)
- `GITHUB_TOKEN`: Automatically provided (no setup needed)

---

## 💡 Tips

- **Approach 1** is recommended for occasional use
- **Approach 2** requires keeping Colab session alive (12-hour limit)
- **Local fallback** is slower but always works

---

## 🐛 Troubleshooting

**Q: Colab session expires?**  
A: Colab free sessions last ~12 hours. You'll need to restart the webhook.

**Q: Want fully automated?**  
A: Consider using GitHub Actions with local Whisper (free, but slower)

**Q: Need faster than GitHub Actions?**  
A: Use Approach 2 with Colab Pro for longer sessions

