#!/bin/bash

# duplicate_tracked_files.sh
# Purpose: Copy all files tracked by Git into a new destination directory, 
# preserving the original directory structure.
# This script is READ-ONLY for your git repository and will not change any files or git state.

set -e

# Output usage information if no destination is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <destination_directory>"
    echo "Example: $0 ~/backup_project"
    exit 1
fi

DEST_DIR="$1"

# Check if the current directory is a git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "❌ Error: $(pwd) is not a Git repository."
    exit 1
fi

# Create the destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Convert destination to absolute path
DEST_DIR=$(realpath "$DEST_DIR")

echo "📂 Source: $(pwd)"
echo "🚀 Destination: $DEST_DIR"
echo "⏳ Duplicating tracked files..."

# Get list of all tracked files and copy them to the destination
# We use git ls-files -z to handle filenames with spaces
# We use rsync with --null --files-from to preserve the directory structure efficiently
git ls-files -z | rsync -a --from0 --files-from=- . "$DEST_DIR"

if [ $? -eq 0 ]; then
    echo "✅ Success! All git-tracked files have been duplicated to: $DEST_DIR"
    echo "   Note: Ignored files (like .env, venv/, etc.) were not copied."
else
    echo "❌ An error occurred during the copying process."
    exit 1
fi
