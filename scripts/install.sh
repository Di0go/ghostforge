#!/bin/sh

#
# ghostforge/scripts/install.sh
#
# Script to install all containers, dependecies and installations.
# <diogopinto> 2025+
#

cd "$(dirname "$0")"

# Load .env variables
if [ -f ../.env ]; then
  export $(grep -v '^#' ../.env | xargs)
else
  echo ".env not found"
  exit 1
fi

sudo docker compose up -d --build

sleep 5
MODEL=${OLLAMA_MODEL:-llama3}
sudo docker exec ghostforge-llm ollama pull $MODEL

echo ""
sudo docker compose ps