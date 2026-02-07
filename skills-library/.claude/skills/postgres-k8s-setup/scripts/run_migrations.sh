#!/bin/bash
# Skill: postgres-k8s-setup
# Script: scripts/run_migrations.sh
# Purpose: Run Alembic migrations on the Kubernetes database pod

DB_POD=$(kubectl get pods -l app=postgres -o jsonpath="{.items[0].metadata.name}")

if [ -z "$DB_POD" ]; then
    echo "✗ Error: Postgres pod not found."
    exit 1
fi

echo "✓ Found database pod: $DB_POD"
echo "Running migrations..."

# Copy alembic folder and config (simplified for demo)
# In a real environment, this would run within the backend container or a migration job
kubectl exec $DB_POD -- bash -c "alembic upgrade head"

if [ $? -eq 0 ]; then
    echo "✓ Migrations completed successfully."
else
    echo "✗ Migration failed."
    exit 1
fi
