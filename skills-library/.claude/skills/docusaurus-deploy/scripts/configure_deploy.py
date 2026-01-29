#!/usr/bin/env python3
"""
Configure Docusaurus deployment settings
"""
import json
import sys
import argparse
import os
from pathlib import Path

def configure_docusaurus_deployment(config_file, base_url="/", site_title="Documentation"):
    """Configure Docusaurus deployment settings"""

    config_path = Path(config_file)

    # Check if config file exists
    if not config_path.exists():
        print(f"✗ Config file does not exist: {config_file}")
        return False

    # Read the existing config file
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the docusaurusConfig object - this could be in JS or TS format
        # We'll make a backup and modify it appropriately

        # Create backup
        backup_path = config_path.with_suffix(config_path.suffix + '.backup')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Update the configuration based on file extension
        if config_path.suffix == '.js':
            # Handle JavaScript config file
            updated_content = update_js_config(content, base_url, site_title)
        elif config_path.suffix == '.ts':
            # Handle TypeScript config file
            updated_content = update_ts_config(content, base_url, site_title)
        else:
            print(f"✗ Unsupported config file type: {config_path.suffix}")
            return False

        # Write the updated config
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print(f"✓ Docusaurus configuration updated in {config_file}")
        print(f"  - baseUrl: {base_url}")
        print(f"  - title: {site_title}")
        print(f"  - Backup saved to: {backup_path}")

        return True

    except Exception as e:
        print(f"✗ Error updating config file: {str(e)}")
        return False

def update_js_config(content, base_url, site_title):
    """Update JavaScript Docusaurus config"""

    # This is a simplified approach - in a real implementation we'd use a proper AST parser
    # For now, we'll do string replacement with some safety checks

    # Update baseUrl if it exists in the config
    if 'baseUrl:' in content:
        import re
        content = re.sub(r'baseUrl:\s*[\'"][^\'"]*[\'"]', f'baseUrl: "{base_url}"', content)
    else:
        # Add baseUrl to the config object if it doesn't exist
        # Look for the main config object start
        config_start = content.find('{')
        if config_start != -1:
            # Insert baseUrl after the opening brace
            insert_pos = content.find('\n', config_start)  # Insert after first newline
            if insert_pos == -1:
                insert_pos = config_start + 1
            content = content[:insert_pos] + f'\n  baseUrl: "{base_url}",' + content[insert_pos:]

    # Update title if it exists in the themeConfig
    if '"title":' in content or "'title':" in content:
        import re
        content = re.sub(r'"title":\s*[\'"][^\'"]*[\'"]', f'"title": "{site_title}"', content)
        content = re.sub(r"'title':\s*[\'"][^\'"]*[\'\"]", f"'title': '{site_title}'", content)
    else:
        # Try to add title to themeConfig
        if 'themeConfig:' in content:
            import re
            # Find the themeConfig object
            theme_config_match = re.search(r'(themeConfig:\s*\{)', content)
            if theme_config_match:
                pos = theme_config_match.end()
                content = content[:pos] + f'\n    title: "{site_title}",' + content[pos:]

    return content

def update_ts_config(content, base_url, site_title):
    """Update TypeScript Docusaurus config - similar to JS but with TS syntax"""
    return update_js_config(content, base_url, site_title)  # For simplicity, treat similarly

def main():
    parser = argparse.ArgumentParser(description='Configure Docusaurus deployment settings')
    parser.add_argument('config_file', help='Path to docusaurus.config.js or docusaurus.config.ts')
    parser.add_argument('--base-url', default='/', help='Base URL for the site (default: /)')
    parser.add_argument('--site-title', default='Documentation', help='Site title (default: Documentation)')

    args = parser.parse_args()

    if configure_docusaurus_deployment(args.config_file, args.base_url, args.site_title):
        print(f"✓ Docusaurus deployment configured successfully")
        sys.exit(0)
    else:
        print(f"✗ Failed to configure Docusaurus deployment")
        sys.exit(1)

if __name__ == "__main__":
    main()