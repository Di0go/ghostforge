#!/bin/sh

#
# ghostforge/scripts/clean.sh
#
# Script to clean all containers, dependecies and installations using Docker Compose.
# <diogopinto> 2025+
#

# "$0" Saves the path of the executed script
cd "$(dirname "$0")"

sudo docker compose down -v
