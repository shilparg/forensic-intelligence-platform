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

# 2. Stage High-Level Components (ML Engine, ELT Models, Dashboard)
echo "🏗️ Staging Platform Core Logic..."
git add core_nlp_engine/
git add meltano_elt_engine/
git add streamlit_dashboard/
git add scripts/
git add documentation/
git add notebooks/

# 3. Stage Project Metadata & Utilities
echo "📂 Staging Project Utilities..."
git add README.md .gitignore requirements.txt requirements_install.txt commit_platform.sh

# 4. Final Professional Commit
echo "🚀 committing changes..."
git commit -m "$COMMIT_MSG"

# 5. Push to GitHub
echo "📡 Pushing to GitHub (origin main)..."
git push origin main

echo "🎯 MISSION COMPLETE: Platform submitted to GitHub."
