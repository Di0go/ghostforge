#!/bin/sh

#
# ghostforge/scripts/stop.sh
#
# Script to stop all containers.
# <diogopinto> 2025+
#

# "$0" Saves the path of the executed script
cd "$(dirname "$0")"

sudo docker compose stop