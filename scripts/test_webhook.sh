#!/bin/bash
# Test script to verify Colab webhook is working

echo "🧪 Testing Colab Webhook Connection"
echo "===================================="

# Check if webhook URL is provided
if [ -z "$1" ]; then
    echo "❌ Error: Webhook URL not provided"
    echo ""
    echo "Usage: ./test_webhook.sh <WEBHOOK_URL>"
    echo "Example: ./test_webhook.sh https://abc123.ngrok.io/transcribe"
    echo ""
    echo "Get your webhook URL from the colab_webhook_server.ipynb notebook"
    exit 1
fi

WEBHOOK_URL=$1

echo ""
echo "Testing connection to: $WEBHOOK_URL"
echo ""

# Test health endpoint first
echo "1️⃣ Testing health endpoint..."
HEALTH_URL="${WEBHOOK_URL/\/transcribe/\/health}"
HEALTH_RESPONSE=$(curl -s "$HEALTH_URL")

if [ $? -eq 0 ]; then
    echo "✅ Server is reachable!"
    echo "Response: $HEALTH_RESPONSE"
else
    echo "❌ Cannot reach server"
    echo "Make sure colab_webhook_server.ipynb is running"
    exit 1
fi

echo ""
echo "2️⃣ Testing transcribe endpoint..."

# Create test payload
PAYLOAD=$(cat <<EOF
{
  "repository_url": "https://github.com/kevinzjpeng/voice-record.git",
  "audio_files": ["voice-record/test.mp3"],
  "commit": "test",
  "pusher": "test-user"
}
EOF
)

# Send test request
RESPONSE=$(curl -s -X POST "$WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" \
    -w "\nHTTP_CODE:%{http_code}")

HTTP_CODE=$(echo "$RESPONSE" | grep HTTP_CODE | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed '/HTTP_CODE/d')

echo "HTTP Code: $HTTP_CODE"
echo "Response: $BODY"

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
    echo ""
    echo "✅ Webhook is working!"
    echo ""
    echo "Next steps:"
    echo "1. Add this URL to GitHub Secrets as COLAB_WEBHOOK_URL"
    echo "2. Push an audio file to test the full workflow"
    echo ""
    echo "GitHub Secrets setup:"
    echo "  Repository Settings → Secrets → Actions → New secret"
    echo "  Name: COLAB_WEBHOOK_URL"
    echo "  Value: $WEBHOOK_URL"
else
    echo ""
    echo "⚠️ Webhook returned HTTP $HTTP_CODE"
    echo "Check the Colab notebook output for errors"
fi

echo ""
echo "===================================="
echo "Test complete!"
