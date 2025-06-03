#!/usr/bin/env python
"""
File Organization Script

This script helps organize loose files into appropriate folders
based on file type and purpose.
"""

import os
import shutil
import re
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Define organization rules
ORGANIZATION_RULES = {
    # Pattern: (target_directory, description)
    r'.*_log_\d+.*\.txt$': ('logs', 'Log files'),
    r'test_.*\.py$': ('tests', 'Test files'),
    r'.*test\.py$': ('tests', 'Test files with suffix naming'),
    r'.*\.html$': ('html_debug', 'HTML debug files'),
    r'.*_summary\.md$': ('summaries', 'Summary documentation'),
    r'.*SUMMARY\.md$': ('summaries', 'Feature summary documentation'),
    r'.*\.bat$': ('batch_files', 'Batch execution files'),
    r'Custodians.*\.xlsx$': ('data', 'Excel data files'),
    r'.*\.pdf$': ('docs', 'Documentation PDF files'),
}

# Define files to keep in the root directory
ROOT_FILES = [
    'excel_stock_updater.py',
    'outstanding_shares_updater.py',
    'requirements.txt',
    'README.md',
    'WORKSPACE_ORGANIZATION.md',
    'organize_files.py',
    '.gitignore',
    'LICENSE',
    'generate_log.py',
    'fix_keywords.py',
]

def ensure_directories_exist():
    """Ensure all target directories exist."""
    directories = set(directory for directory, _ in ORGANIZATION_RULES.values())
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Created directory: {directory}")

def should_organize_file(filename):
    """Check if file should be organized or kept in root."""
    # Skip directories
    if os.path.isdir(filename):
        return False
    
    # Skip files that should stay in root
    if filename in ROOT_FILES:
        return False
    
    # Skip hidden files
    if filename.startswith('.'):
        return False
    
    return True

def get_target_directory(filename):
    """Determine the target directory for a file based on patterns."""
    for pattern, (directory, description) in ORGANIZATION_RULES.items():
        if re.match(pattern, filename):
            return directory, description
    
    # Default handling for source files
    if filename.endswith('.py'):
        return 'src', 'Python source files'
    
    return None, None

def organize_files():
    """Organize files according to rules."""
    ensure_directories_exist()
    
    organized_count = 0
    skipped_count = 0
    
    for filename in os.listdir('.'):
        if not should_organize_file(filename):
            skipped_count += 1
            continue
        
        target_dir, description = get_target_directory(filename)
        
        if target_dir:
            # Create target directory if it doesn't exist
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            
            source_path = os.path.join('.', filename)
            target_path = os.path.join(target_dir, filename)
            
            # Check if file already exists in target
            if os.path.exists(target_path):
                # Compare modification times
                source_mtime = os.path.getmtime(source_path)
                target_mtime = os.path.getmtime(target_path)
                
                if source_mtime > target_mtime:
                    # Source is newer, backup the target file first
                    backup_dir = os.path.join('backups', target_dir)
                    if not os.path.exists(backup_dir):
                        os.makedirs(backup_dir)
                    
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    backup_filename = f"{os.path.splitext(filename)[0]}_{timestamp}{os.path.splitext(filename)[1]}"
                    backup_path = os.path.join(backup_dir, backup_filename)
                    
                    shutil.copy2(target_path, backup_path)
                    logging.info(f"Backed up existing file: {target_path} -> {backup_path}")
                    
                    # Now copy the source file
                    shutil.copy2(source_path, target_path)
                    logging.info(f"Updated file: {filename} -> {target_dir}/ (newer version)")
                else:
                    logging.info(f"Skipped: {filename} (older than target)")
            else:
                # Target doesn't exist, just copy
                shutil.copy2(source_path, target_path)
                logging.info(f"Organized: {filename} -> {target_dir}/ ({description})")
            
            organized_count += 1
    
    logging.info(f"Organization complete: {organized_count} files organized, {skipped_count} files kept in root")

if __name__ == "__main__":
    logging.info("Starting file organization process...")
    organize_files() 