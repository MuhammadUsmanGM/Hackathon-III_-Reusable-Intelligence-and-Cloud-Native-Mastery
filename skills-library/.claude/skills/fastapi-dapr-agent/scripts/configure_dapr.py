#!/usr/bin/env python3
"""
Configure Dapr for a FastAPI service
"""
import subprocess
import sys
import argparse
import os
from pathlib import Path

def check_dapr_installed():
    """Check if Dapr CLI is installed"""
    try:
        result = subprocess.run(["dapr", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_dapr():
    """Install Dapr CLI and runtime"""
    print("Installing Dapr...")

    # Install Dapr CLI and init runtime
    try:
        subprocess.run(["wget", "-q", "https://raw.githubusercontent.com/dapr/cli/master/install/install.sh", "-O", "-"],
                      stdout=subprocess.PIPE)
        result = subprocess.run(["bash", "-"], shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"✗ Failed to install Dapr CLI: {result.stderr}")
            return False

        # Initialize Dapr
        result = subprocess.run(["dapr", "init"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"✗ Failed to initialize Dapr: {result.stderr}")
            return False

        print("✓ Dapr installed and initialized")
        return True
    except Exception as e:
        print(f"✗ Error installing Dapr: {str(e)}")
        return False

def configure_dapr_components(service_name):
    """Configure Dapr components for the service"""
    print(f"Configuring Dapr components for {service_name}...")

    # Create Dapr components directory if it doesn't exist
    components_dir = Path.home() / ".dapr" / "components"
    components_dir.mkdir(parents=True, exist_ok=True)

    # Create state store component
    statestore_config = f'''apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore-{service_name}
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
  - name: actorStateStore
    value: "true"
'''

    with open(components_dir / f"statestore-{service_name}.yaml", 'w') as f:
        f.write(statestore_config)

    # Create pubsub component
    pubsub_config = f'''apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub-{service_name}
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
'''

    with open(components_dir / f"pubsub-{service_name}.yaml", 'w') as f:
        f.write(pubsub_config)

    print(f"✓ Dapr components configured for {service_name}")
    return True

def main():
    parser = argparse.ArgumentParser(description='Configure Dapr for a FastAPI service')
    parser.add_argument('service_name', help='Name of the service')

    args = parser.parse_args()

    # Check if Dapr is installed
    if not check_dapr_installed():
        print("Dapr not found. Installing...")
        if not install_dapr():
            print("✗ Failed to install Dapr. Exiting.")
            sys.exit(1)

    # Configure Dapr components
    if configure_dapr_components(args.service_name):
        print(f"✓ Dapr successfully configured for {args.service_name}")
        sys.exit(0)
    else:
        print(f"✗ Failed to configure Dapr for {args.service_name}")
        sys.exit(1)

if __name__ == "__main__":
    main()