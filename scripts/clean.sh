#!/bin/sh

# ------------------------------------------------------------
# scripts/clean.sh
# This script cleans up the container infrastructure for a project
# 
# <diogopinto> 2025+
# ------------------------------------------------------------

# EN: Stops the script if any command fails
set -e

# 0: Configurations
PROJECT_NAME="ghostforge"
STORAGE_POOL_NAME="ghostforge-storage"
NETWORK_NAME="ghostforge-net"

incus project delete "$PROJECT_NAME" -f

incus storage delete "$STORAGE_POOL_NAME"

incus network delete "$NETWORK_NAME"