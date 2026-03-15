#!/usr/bin/env bash
set -e

echo ""
echo "================================================"
echo "  Installing Claude Code (claude CLI)"
echo "================================================"
echo ""

# ── 1. Check Node.js is installed (required) ─────────────────────────────────
if ! command -v node &> /dev/null; then
  echo "❌  Node.js not found. Installing via nvm..."
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
  nvm install --lts
  nvm use --lts
  echo "✅  Node.js installed: $(node --version)"
else
  echo "✅  Node.js found: $(node --version)"
fi

# ── 2. Install Claude Code globally via npm ───────────────────────────────────
echo ""
echo "Installing @anthropic-ai/claude-code globally..."
npm install -g @anthropic-ai/claude-code

echo ""
echo "✅  Claude Code installed: $(claude --version)"

# ── 3. Verify PATH ────────────────────────────────────────────────────────────
NPM_GLOBAL=$(npm root -g)
NPM_BIN=$(npm bin -g 2>/dev/null || dirname "$NPM_GLOBAL/bin")

if ! command -v claude &> /dev/null; then
  echo ""
  echo "⚠️   'claude' not found in PATH. Adding npm global bin to PATH..."
  SHELL_RC="$HOME/.bashrc"
  [ -n "$ZSH_VERSION" ] && SHELL_RC="$HOME/.zshrc"
  echo "export PATH=\"$NPM_BIN:\$PATH\"" >> "$SHELL_RC"
  export PATH="$NPM_BIN:$PATH"
  echo "✅  PATH updated in $SHELL_RC"
fi

# ── 4. Create per-project helper script: use_claude.sh ───────────────────────
cat > use_claude.sh << 'INNER'
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
INNER
chmod +x use_claude.sh
echo ""
echo "✅  Created use_claude.sh in current directory"

# ── 5. Create global alias (optional convenience) ────────────────────────────
SHELL_RC="$HOME/.bashrc"
[ -f "$HOME/.zshrc" ] && SHELL_RC="$HOME/.zshrc"

if ! grep -q "alias cl=" "$SHELL_RC" 2>/dev/null; then
  echo "alias cl='claude'" >> "$SHELL_RC"
  echo "✅  Added alias 'cl' for 'claude' in $SHELL_RC"
else
  echo "✅  Alias 'cl' already exists in $SHELL_RC"
fi

# ── 6. Print summary ──────────────────────────────────────────────────────────
echo ""
echo "================================================"
echo "  Claude Code is ready!"
echo "================================================"
echo ""
echo "  Global commands (works anywhere):"
echo "    claude               → interactive mode"
echo "    claude \"<task>\"      → run a one-shot task"
echo "    cl                   → short alias for claude"
echo ""
echo "  In this project:"
echo "    ./use_claude.sh                    → interactive"
echo "    ./use_claude.sh \"fix server.py\"    → one-shot"
echo ""
echo "  Useful Claude Code commands once inside:"
echo "    /help                → show all commands"
echo "    /init                → create CLAUDE.md for this project"
echo "    /compact             → compress conversation context"
echo "    /clear               → clear conversation"
echo ""
echo "  First-time setup:"
echo "    Run 'claude' then follow the login prompt to"
echo "    authenticate with your Anthropic account."
echo ""
echo "  Reload your shell or run:"
echo "    source $SHELL_RC"
echo ""
