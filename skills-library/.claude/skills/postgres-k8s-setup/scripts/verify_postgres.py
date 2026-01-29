#!/usr/bin/env python3
"""
PostgreSQL verification script
Checks if PostgreSQL is properly deployed and running
"""
import subprocess
import json
import sys

def check_postgres_pod():
    """Check if PostgreSQL pod is running"""
    try:
        result = subprocess.run(
            ["kubectl", "get", "pods", "-n", "postgresql", "-o", "json"],
            capture_output=True, text=True
        )

        if result.returncode != 0:
            print("✗ Could not get PostgreSQL pods status")
            print(result.stderr)
            return False

        pods_data = json.loads(result.stdout)
        pods = pods_data.get("items", [])

        if not pods:
            print("✗ No PostgreSQL pods found")
            return False

        running_count = 0
        for pod in pods:
            status = pod["status"]["phase"]
            pod_name = pod["metadata"]["name"]
            print(f"  Pod {pod_name}: {status}")

            if status == "Running":
                running_count += 1

        total_count = len(pods)

        if running_count == total_count:
            print(f"✓ All {total_count} PostgreSQL pods running")
            return True
        else:
            print(f"✗ {running_count}/{total_count} PostgreSQL pods running")
            return False

    except Exception as e:
        print(f"✗ Error checking PostgreSQL pods: {str(e)}")
        return False

def main():
    print("Verifying PostgreSQL deployment...")

    if check_postgres_pod():
        print("✓ PostgreSQL verification successful")
        sys.exit(0)
    else:
        print("✗ PostgreSQL verification failed")
        sys.exit(1)

if __name__ == "__main__":
    main()