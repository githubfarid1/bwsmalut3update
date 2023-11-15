#!/usr/bin/env bash
# Start NGROK in background
echo "⚡️ Starting ngrok"
/home/arsip/ngrok http 80 > /dev/null &

# Wait for ngrok to be available
while ! nc -z localhost 4040; do
  sleep 1/5 # wait Ngrok to be available
done
sleep 1
# Get NGROK dynamic URL from its own exposed local API
NGROK_REMOTE_URL="$(curl http://localhost:4040/api/tunnels | jq ".tunnels[0].public_url")"
if test -z "${NGROK_REMOTE_URL}"
then
  echo "❌ ERROR: ngrok doesn't seem to return a valid URL (${NGROK_REMOTE_URL})."
  exit 1
fi

# Trim double quotes from variable
NGROK_REMOTE_URL=$(echo ${NGROK_REMOTE_URL} | tr -d '"')
# If http protocol is returned, replace by https
NGROK_REMOTE_URL=${NGROK_REMOTE_URL/http:\/\//https:\/\/}

# Get script parent folder to point to .env file and get TELEGRAM_BOT_TOKEN dynamically
PARENT_PATH=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )

# # Get TELEGRAM_BOT_TOKEN dynamically from local .env file
# TELEGRAM_BOT_TOKEN=$(grep TELEGRAM_BOT_TOKEN ${PARENT_PATH}/../.env.local | cut -d '=' -f2)
# if test -z "${TELEGRAM_BOT_TOKEN}"
# then
#   echo "❌ ERROR: I haven't been able to recover TELEGRAM_BOT_TOKEN from your local .env.local variables file."
#   exit 1
# fi

# # Set our NGROK remote url to our development
# curl -F "url=${NGROK_REMOTE_URL}/webhook/telegram/${TELEGRAM_BOT_TOKEN}/" https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook

# bold=$(tput bold)
# normal=$(tput sgr0)
echo ${NGROK_REMOTE_URL} | tr -d '\n' #| pbcopy
printf "\n\n🌍 Your ngrok remote URL is 👉 ${bold}${NGROK_REMOTE_URL} 👈\n📋 ${normal}I've just copied it to your clipboard 😉\n\n"