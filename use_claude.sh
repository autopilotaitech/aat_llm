#!/usr/bin/env bash
# Run this inside any project folder to start Claude Code
# Usage:  ./use_claude.sh
# Or:     ./use_claude.sh "fix the bug in server.py"

if [ -z "$1" ]; then
  echo ""
  echo "Starting Claude Code in interactive mode..."
  echo "Type your task or question, then press Enter."
  echo ""
  claude
else
  echo ""
  echo "Running Claude Code with task: $1"
  echo ""
  claude "$1"
fi
