#!/bin/sh

# ------------------------------------------------------------
# scripts/install.sh
# This script sets up a container infrastructure for a project
# 
# <diogopinto> 2025+
# ------------------------------------------------------------

# EN: Stops the script if any command fails
set -e

# 0: Configurations
PROJECT_NAME="ghostforge"
STORAGE_POOL_NAME="ghostforge-storage"
STORAGE_POOL_BACKEND="dir" 
NETWORK_NAME="ghostforge-net"
BASE_IMAGE="images:ubuntu/24.04"
DB_IP="10.100.100.10"
LLM_IP="10.100.100.11"
APP_IP="10.100.100.12"
GATEWAY="10.100.100.1"
DNS="1.1.1.1"

assign_ip() 
{
  container="$1"
  ip="$2"
  echo "Configuring IP $ip for $container..."

  sudo incus exec "$container" --project "$PROJECT_NAME" -- bash -c "cat >/etc/netplan/01-netcfg.yaml <<'EOF'
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: no
      addresses: [$ip/24]
      nameservers:
        addresses: [$DNS]
      routes:
        - to: 0.0.0.0/0
          via: $GATEWAY
          on-link: true
EOF
chmod 600 /etc/netplan/01-netcfg.yaml
netplan apply
"
}


# 1: Project creation
incus project create "$PROJECT_NAME"

# 2: Storage pool creation
incus storage create "$STORAGE_POOL_NAME" "$STORAGE_POOL_BACKEND" --project "$PROJECT_NAME"
incus profile device add default root disk path=/ pool="$STORAGE_POOL_NAME" --project "$PROJECT_NAME"

# 3: Network Setup
incus network create "$NETWORK_NAME" ipv4.address="$GATEWAY/24" ipv4.nat=true ipv4.dhcp=true ipv6.address=none --project "$PROJECT_NAME"
incus profile device add default eth0 nic name=eth0 network="$NETWORK_NAME" --project "$PROJECT_NAME"

# 4: Setup the containers for this project
# 4.1: ghostforge-db (PostgreSQL)
incus launch "$BASE_IMAGE" ghostforge-db --project "$PROJECT_NAME" -c limits.memory=1GB -c limits.cpu=1

# 4.2: ghostforge-llm (Ollama) - TODO: Setup GPU passtrough
incus launch "$BASE_IMAGE" ghostforge-llm --project "$PROJECT_NAME" -c limits.memory=8GB -c limits.cpu=4

# 4.3: ghostforge-app (Django/LangChain)
incus launch "$BASE_IMAGE" ghostforge-app --project "$PROJECT_NAME" -c limits.memory=4GB -c limits.cpu=2

# 4.4: Assign IPs
assign_ip "ghostforge-db" "$DB_IP"
assign_ip "ghostforge-llm" "$LLM_IP"
assign_ip "ghostforge-app" "$APP_IP"

# 4.5: Proxy for the web app (Host:8000 -> ghostforge-app:8000)
incus config device add ghostforge-app proxy-http proxy listen=tcp:0.0.0.0:8000 connect=tcp:127.0.0.1:8000 --project "$PROJECT_NAME"

sleep 5