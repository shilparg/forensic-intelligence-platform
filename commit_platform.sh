#!/bin/bash

# --- Forensic Intelligence Platform: Professional Commit Utility ---
# Usage: ./commit_platform.sh "Your Commit Message"

COMMIT_MSG=$1

if [ -z "$COMMIT_MSG" ]; then
    echo "❌ Error: Please provide a commit message."
    echo "Example: ./commit_platform.sh \"Updated AI metrics\""
    exit 1
fi

echo "🕵️ Starting Forensic Submission Pipeline..."

# 1. Clean Environment (Stop tracking transient UI states)
echo "🧹 Cleaning Git Cache for state files..."
git rm --cached ui_state.json run_config.json 2>/dev/null

# 2. Stage Documentation Hub (Master Docs, 3D Visuals, Notebooks)
echo "📂 Staging Documentation hub..."
git add documentation/

# 3. Stage Core Technical Files
echo "🏗️ Staging Core Project Assets..."
git add README.md .gitignore requirements.txt 
git add streamlit_dashboard/app.py 
git add core_nlp_engine/analysis/sector_metadata.json

# 4. Final Professional Commit
echo "🚀 committing changes..."
git commit -m "$COMMIT_MSG"

# 5. Push to GitHub
echo "📡 Pushing to GitHub (origin main)..."
git push origin main

echo "🎯 MISSION COMPLETE: Platform submitted to GitHub."
