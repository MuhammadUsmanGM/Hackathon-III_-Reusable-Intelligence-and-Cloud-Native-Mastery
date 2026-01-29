#!/usr/bin/env python3
"""
Test the MCP server integration
"""
import asyncio
import aiohttp
import json
import argparse
import sys
from typing import Dict, Any, List

async def test_mcp_server_connection(server_url: str) -> bool:
    """
    Test if the MCP server is reachable

    Args:
        server_url: URL of the MCP server to test

    Returns:
        True if connection successful, False otherwise
    """
    try:
        async with aiohttp.ClientSession() as session:
            # Send a simple test request
            test_tools = [
                {
                    "id": "test1",
                    "name": "execute_bash_command",
                    "arguments": {"command": "echo 'Connection test'"}
                }
            ]

            async with session.post(server_url, json={"tools": test_tools}) as response:
                if response.status == 200:
                    return True
                else:
                    print(f"Server responded with status: {response.status}")
                    return False
    except aiohttp.ClientConnectorError:
        print(f"Cannot connect to server: {server_url}")
        return False
    except Exception as e:
        print(f"Error testing server connection: {e}")
        return False

async def run_comprehensive_tests(server_url: str) -> Dict[str, Any]:
    """
    Run comprehensive tests on the MCP server

    Args:
        server_url: URL of the MCP server to test

    Returns:
        Dictionary with test results
    """
    results = {
        "connection": False,
        "bash_execution": False,
        "file_operations": False,
        "directory_listing": False,
        "error_handling": False
    }

    # Test 1: Connection
    print("Test 1: Testing server connection...")
    results["connection"] = await test_mcp_server_connection(server_url)
    print(f"  Result: {'✓ PASS' if results['connection'] else '✗ FAIL'}")

    if not results["connection"]:
        return results

    # Test 2: Bash command execution
    print("\\nTest 2: Testing bash command execution...")
    try:
        async with aiohttp.ClientSession() as session:
            tools = [
                {
                    "id": "bash1",
                    "name": "execute_bash_command",
                    "arguments": {"command": "echo 'hello world'"}
                }
            ]

            async with session.post(server_url, json={"tools": tools}) as response:
                result = await response.json()

                if isinstance(result, list) and len(result) > 0:
                    content = result[0].get("content", "")
                    if "hello world" in str(content).lower():
                        results["bash_execution"] = True
                        print("  Result: ✓ PASS")
                    else:
                        print(f"  Result: ✗ FAIL - Unexpected output: {content}")
                else:
                    print(f"  Result: ✗ FAIL - Invalid response format: {result}")
    except Exception as e:
        print(f"  Result: ✗ FAIL - Error: {e}")

    # Test 3: Directory listing
    print("\\nTest 3: Testing directory listing...")
    try:
        async with aiohttp.ClientSession() as session:
            tools = [
                {
                    "id": "dir1",
                    "name": "list_directory",
                    "arguments": {"dirpath": "."}
                }
            ]

            async with session.post(server_url, json={"tools": tools}) as response:
                result = await response.json()

                if isinstance(result, list) and len(result) > 0:
                    content = result[0].get("content", "")
                    # Check if it's a valid JSON list of directory items
                    try:
                        dir_items = json.loads(content)
                        if isinstance(dir_items, list):
                            results["directory_listing"] = True
                            print("  Result: ✓ PASS")
                        else:
                            print(f"  Result: ✗ FAIL - Not a list: {type(dir_items)}")
                    except json.JSONDecodeError:
                        print(f"  Result: ✗ FAIL - Invalid JSON: {content}")
                else:
                    print(f"  Result: ✗ FAIL - Invalid response format: {result}")
    except Exception as e:
        print(f"  Result: ✗ FAIL - Error: {e}")

    # Test 4: Error handling
    print("\\nTest 4: Testing error handling...")
    try:
        async with aiohttp.ClientSession() as session:
            tools = [
                {
                    "id": "error1",
                    "name": "execute_bash_command",
                    "arguments": {"command": "nonexistent_command_that_does_not_exist"}
                }
            ]

            async with session.post(server_url, json={"tools": tools}) as response:
                result = await response.json()

                if isinstance(result, list) and len(result) > 0:
                    content = result[0].get("content", "")
                    # Check if the error was handled properly (contains error info)
                    if '"error"' in str(content) or 'not found' in str(content).lower():
                        results["error_handling"] = True
                        print("  Result: ✓ PASS")
                    else:
                        print(f"  Result: ✗ FAIL - Error not properly handled: {content}")
                else:
                    print(f"  Result: ✗ FAIL - Invalid response format: {result}")
    except Exception as e:
        print(f"  Result: ✗ FAIL - Error: {e}")

    return results

def calculate_score(results: Dict[str, Any]) -> float:
    """
    Calculate a score based on test results

    Args:
        results: Dictionary of test results

    Returns:
        Score as percentage (0-100)
    """
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    return (passed / total) * 100 if total > 0 else 0

async def main():
    parser = argparse.ArgumentParser(description='Test MCP server integration')
    parser.add_argument('--server-url', default='http://localhost:8080/execute',
                       help='URL of the MCP server to test (default: http://localhost:8080/execute)')

    args = parser.parse_args()

    print(f"MCP Server Integration Test")
    print(f"Target Server: {args.server_url}")
    print("="*50)

    results = await run_comprehensive_tests(args.server_url)

    print("\\n" + "="*50)
    print("TEST SUMMARY:")
    print(f"  Connection: {'✓ PASS' if results['connection'] else '✗ FAIL'}")
    print(f"  Bash Execution: {'✓ PASS' if results['bash_execution'] else '✗ FAIL'}")
    print(f"  File Operations: {'✓ PASS' if results['file_operations'] else '✗ FAIL'}")
    print(f"  Directory Listing: {'✓ PASS' if results['directory_listing'] else '✗ FAIL'}")
    print(f"  Error Handling: {'✓ PASS' if results['error_handling'] else '✗ FAIL'}")

    score = calculate_score(results)
    print(f"\\nOverall Score: {score:.1f}%")

    if score >= 80:
        print("✓ Integration test PASSED - MCP server is functioning properly")
        sys.exit(0)
    else:
        print("✗ Integration test FAILED - MCP server needs attention")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())