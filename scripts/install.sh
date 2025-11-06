#!/bin/sh

#
# ghostforge/scripts/install.sh
#
# Script to install all containers, dependecies and installations.
# <diogopinto> 2025+
#

cd "$(dirname "$0")"

sudo docker compose up -d --build

echo ""
sudo docker compose ps