#!/usr/bin/env bash
set -euo pipefail

# Flaco AI - Professional installer
# Installs the CLI with pipx (preferred) and makes the `flaco` command globally available.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║                                       ║"
echo "║          🦙 FLACO AI                  ║"
echo "║                                       ║"
echo "║     Installing CLI (pipx)             ║"
echo "║                                       ║"
echo "╚═══════════════════════════════════════╝"
echo ""

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "❌ $1 not found."
    return 1
  fi
}

# Check Python
if ! require_cmd python3; then
  echo "📥 Please install Python 3.9+ from https://python.org"
  exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Found Python ${PYTHON_VERSION}"

# Check Ollama (warn only)
if ! command -v ollama >/dev/null 2>&1; then
  echo "⚠️  Ollama not found. Install from https://ollama.ai (required for LLM features)."
fi

install_with_pipx() {
  echo "📦 Installing with pipx..."
  pipx install --force "${REPO_ROOT}"
}

install_with_pip() {
  echo "📦 Installing with pip (fallback)..."
  python3 -m pip install --upgrade "${REPO_ROOT}"
}

ensure_global_shim() {
  # If flaco already resolves, nothing to do.
  if command -v flaco >/dev/null 2>&1; then
    return
  fi

  # Try to locate the installed binary.
  local candidate=""

  if command -v pipx >/dev/null 2>&1; then
    candidate="$(python3 -m pipx environment --value PIPX_BIN_DIR 2>/dev/null || true)/flaco"
  fi

  if [ -z "${candidate}" ] || [ ! -x "${candidate}" ]; then
    # Fall back to Python scripts dir.
    candidate="$(python3 -c 'import sysconfig; print(sysconfig.get_path("scripts"))')/flaco"
  fi

  if [ ! -x "${candidate}" ]; then
    echo "⚠️  Could not locate the flaco binary after install."
    return
  fi

  # Prefer linking into /usr/local/bin if writable.
  if [ -d "/usr/local/bin" ] && [ -w "/usr/local/bin" ]; then
    ln -sf "${candidate}" /usr/local/bin/flaco
    echo "✅ Linked flaco to /usr/local/bin/flaco"
  else
    echo "⚠️  /usr/local/bin is not writable; flaco is at:"
    echo "    ${candidate}"
  fi
}

# Install
if command -v pipx >/dev/null 2>&1; then
  install_with_pipx
else
  echo "ℹ️  pipx not found; using pip. For isolated installs, install pipx: https://pipx.pypa.io"
  install_with_pip
fi

# Ensure command is reachable without shell edits
ensure_global_shim

if command -v flaco >/dev/null 2>&1; then
  echo ""
  echo "✅ flaco command is ready."
else
  echo ""
  echo "⚠️  flaco command not on PATH. You may need to restart your terminal or add the scripts directory to PATH."
fi

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║          🎉 ALL DONE!                 ║"
echo "║    Start Flaco by typing: flaco       ║"
echo "╚═══════════════════════════════════════╝"
echo ""
echo "💡 Quick commands to try:"
echo "   flaco --help"
echo "   /help       - See all commands"
echo "   /init       - Initialize project with FLACO.md"
echo "   /scan       - Scan your project"
echo "   /stats week - View statistics"
echo ""
