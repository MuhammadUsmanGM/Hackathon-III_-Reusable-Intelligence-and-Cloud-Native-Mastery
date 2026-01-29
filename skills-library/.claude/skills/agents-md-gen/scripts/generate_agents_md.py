#!/usr/bin/env python3
"""
AGENTS.md Generator Script
Creates or updates AGENTS.md files for repositories
"""
import os
import sys
import argparse
from pathlib import Path

def analyze_repository(repo_path):
    """Analyze repository structure and content"""
    repo = Path(repo_path)
    structure = {}

    # Identify key directories and files
    for item in repo.iterdir():
        if item.is_dir():
            structure[item.name] = {
                'type': 'directory',
                'contents': [subitem.name for subitem in item.iterdir() if subitem.is_file()]
            }
        elif item.is_file():
            structure[item.name] = {
                'type': 'file',
                'extension': item.suffix
            }

    return structure

def generate_agents_md(structure, repo_path):
    """Generate AGENTS.md content based on repository structure"""
    content = f"""# AGENTS.md for {os.path.basename(repo_path)}

This file describes the repository structure and guidelines to help AI agents work effectively with this codebase.

## Repository Structure

"""

    for name, info in structure.items():
        if info['type'] == 'directory':
            content += f"- **{name}/**: Directory containing {len(info['contents'])} files\n"
        else:
            content += f"- **{name}**: {info['extension']} file\n"

    content += """

## Key Conventions

## Architecture Patterns

## Testing Guidelines

## Deployment Process

## Troubleshooting

"""
    return content

def main():
    parser = argparse.ArgumentParser(description='Generate AGENTS.md for a repository')
    parser.add_argument('repo_path', help='Path to the repository')
    parser.add_argument('--output', '-o', help='Output file (default: repo_path/AGENTS.md)')

    args = parser.parse_args()

    repo_path = args.repo_path
    if not os.path.exists(repo_path):
        print(f"Error: Repository path does not exist: {repo_path}")
        sys.exit(1)

    structure = analyze_repository(repo_path)
    agents_content = generate_agents_md(structure, repo_path)

    output_file = args.output or os.path.join(repo_path, "AGENTS.md")
    with open(output_file, 'w') as f:
        f.write(agents_content)

    print(f"✓ AGENTS.md generated successfully: {output_file}")

if __name__ == "__main__":
    main()