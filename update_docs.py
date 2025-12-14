#!/usr/bin/env python3
"""
Update cached Claude Code documentation from the official site.

This script downloads the latest documentation files and updates the cache.
Can be run locally or in Colab.
"""
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def read_manifest():
    """Read the docs manifest."""
    manifest_path = Path('src/docs_manifest.json')
    with open(manifest_path, 'r') as f:
        return json.load(f)

def write_manifest(manifest):
    """Write the docs manifest."""
    manifest_path = Path('src/docs_manifest.json')
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

def download_file(url, output_path):
    """Download a file from URL."""
    try:
        # Try curl first (more reliable)
        result = subprocess.run(
            ['curl', '-s', '-f', '-L', url],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            return True, None
        else:
            return False, f"curl failed: {result.stderr}"
    except subprocess.TimeoutExpired:
        return False, "Download timeout"
    except FileNotFoundError:
        # Fallback to Python urllib
        try:
            import urllib.request
            with urllib.request.urlopen(url, timeout=30) as response:
                content = response.read().decode('utf-8')
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True, None
        except Exception as e:
            return False, str(e)

def add_metadata_header(content, doc_info, timestamp):
    """Add metadata header to doc content."""
    header = f"""<!--
Documentation Source: {doc_info['url']}
Title: {doc_info['title']}
Description: {doc_info['description']}
Downloaded: {timestamp}
Last Updated: {timestamp}
Check for updates: {doc_info['url']}
Sitemap: https://code.claude.com/docs/llms.txt
-->

"""
    return header + content

def update_docs(force=False):
    """Update all documentation files."""
    manifest = read_manifest()
    cached_docs_dir = Path('src/cached_docs')
    cached_docs_dir.mkdir(parents=True, exist_ok=True)
    
    updated_count = 0
    failed_count = 0
    timestamp = datetime.now().isoformat()
    
    print("=" * 60)
    print("Updating Claude Code Documentation")
    print("=" * 60)
    print(f"Base URL: {manifest['base_url']}")
    print(f"Sitemap: {manifest['sitemap_url']}")
    print()
    
    for doc_info in manifest['docs']:
        filename = doc_info['filename']
        url = doc_info['url']
        output_path = cached_docs_dir / filename
        
        # Skip local files
        if url == "local":
            print(f"⏭️  Skipping {filename} (local file)")
            continue
        
        # Check if file exists and is recent (unless force)
        if not force and output_path.exists():
            # Check if we should update (for now, always update if force=False still updates)
            # Could add date checking here
            pass
        
        print(f"📥 Downloading {filename}...")
        print(f"   URL: {url}")
        
        success, error = download_file(url, output_path)
        
        if success:
            # Add or update metadata header
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove existing header if present
            if content.startswith('<!--'):
                # Find the end of the HTML comment
                end_idx = content.find('-->')
                if end_idx != -1:
                    content = content[end_idx + 4:].lstrip('\n')
            
            # Add new header
            content = add_metadata_header(content, doc_info, timestamp)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"   ✓ Saved to {output_path}")
            updated_count += 1
        else:
            print(f"   ✗ Failed: {error}")
            failed_count += 1
        print()
    
    # Update manifest timestamp
    manifest['last_updated'] = timestamp
    write_manifest(manifest)
    
    print("=" * 60)
    print(f"Update complete: {updated_count} updated, {failed_count} failed")
    print(f"Last updated: {timestamp}")
    print("=" * 60)
    
    return updated_count, failed_count

def main():
    """Entry point for the update-docs script."""
    force = '--force' in sys.argv
    update_docs(force=force)

if __name__ == '__main__':
    main()
