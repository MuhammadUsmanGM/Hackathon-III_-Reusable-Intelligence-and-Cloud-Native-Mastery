#!/bin/bash
echo "Checking prerequisites..."
echo "Docker version:"
docker --version
if [ $? -eq 0 ]; then
    echo "✓ Docker OK"
else
    echo "✗ Docker NOT OK - Please ensure Docker Desktop is running"
fi

echo "Minikube status:"
minikube status
if [ $? -eq 0 ]; then
    echo "✓ Minikube OK"
else
    echo "✗ Minikube NOT OK - Please ensure Docker is running and run: minikube start --cpus=4 --memory=8192 --driver=docker"
fi

echo "Kubectl cluster info:"
kubectl cluster-info
if [ $? -eq 0 ]; then
    echo "✓ Kubectl OK"
else
    echo "✗ Kubectl NOT OK - Minikube cluster may not be running"
fi

echo "Helm version:"
helm version
if [ $? -eq 0 ]; then
    echo "✓ Helm OK"
else
    echo "✗ Helm NOT OK"
fi

echo "Claude Code version:"
claude --version
if [ $? -eq 0 ]; then
    echo "✓ Claude Code OK"
else
    echo "✗ Claude Code NOT OK"
fi

echo "Goose version:"
~/goose/goose.exe --version
if [ $? -eq 0 ]; then
    echo "✓ Goose OK"
else
    echo "✗ Goose NOT OK"
fi

echo "Environment verification complete!"