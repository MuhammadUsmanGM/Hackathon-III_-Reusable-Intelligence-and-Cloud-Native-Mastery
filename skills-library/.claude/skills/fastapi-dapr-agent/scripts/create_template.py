#!/usr/bin/env python3
"""
Create a FastAPI service template with Dapr integration
"""
import os
import sys
import argparse
from pathlib import Path

def create_fastapi_dapr_template(service_name, output_dir):
    """Create a FastAPI service template with Dapr integration"""

    # Create the service directory
    service_dir = Path(output_dir) / service_name
    service_dir.mkdir(parents=True, exist_ok=True)

    # Create main.py
    main_content = f'''from fastapi import FastAPI, HTTPException
import logging
import uvicorn
from dapr.ext.grpc import App
from dapr.clients import DaprClient

app = FastAPI(title="{service_name}", description="FastAPI service with Dapr integration")

@app.get("/")
async def root():
    return {{"message": "{service_name} service is running with Dapr"}}

@app.get("/health")
async def health_check():
    return {{"status": "healthy", "service": "{service_name}"}}

# Example Dapr integration
@app.get("/state/{{key}}")
async def get_state(key: str):
    with DaprClient() as client:
        response = client.get_state(store_name="statestore", key=key)
        return {{"key": key, "value": response.data.decode() if response.data else None}}

@app.post("/state/{{key}}")
async def save_state(key: str, value: dict):
    with DaprClient() as client:
        client.save_state(store_name="statestore", key=key, value=str(value))
        return {{"key": key, "saved": True}}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

    with open(service_dir / "main.py", 'w') as f:
        f.write(main_content)

    # Create requirements.txt
    requirements_content = '''fastapi==0.104.1
uvicorn==0.24.0
dapr-ext-grpc==1.12.0
dapr-client==1.12.0
pydantic==2.5.0
python-dotenv==1.0.0
'''

    with open(service_dir / "requirements.txt", 'w') as f:
        f.write(requirements_content)

    # Create Dockerfile
    dockerfile_content = f'''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
'''

    with open(service_dir / "Dockerfile", 'w') as f:
        f.write(dockerfile_content)

    # Create dapr component configuration
    dapr_config = service_dir / "components"
    dapr_config.mkdir(exist_ok=True)

    statestore_content = '''apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
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

    with open(dapr_config / "statestore.yaml", 'w') as f:
        f.write(statestore_content)

    pubsub_content = '''apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
'''

    with open(dapr_config / "pubsub.yaml", 'w') as f:
        f.write(pubsub_content)

    print(f"✓ FastAPI Dapr template created at {service_dir}")

def main():
    parser = argparse.ArgumentParser(description='Create FastAPI service with Dapr integration template')
    parser.add_argument('service_name', help='Name of the service')
    parser.add_argument('--output', '-o', default='.', help='Output directory (default: current directory)')

    args = parser.parse_args()

    create_fastapi_dapr_template(args.service_name, args.output)

if __name__ == "__main__":
    main()