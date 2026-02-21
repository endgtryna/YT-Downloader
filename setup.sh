#!/usr/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Installing YT-Downloader..."

if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not installed"
    exit 1
fi

if ! python3 -m venv --help &> /dev/null; then
    echo "Error: python3-venv is missing"
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip -q

echo "Installing dependencies..."
pip install -r requirements.txt -q

if ! command -v node &> /dev/null; then
    echo "Setup nodeenv..."
    nodeenv -p --node=lts -q
fi

INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"

cat > "$INSTALL_DIR/yt-downloader" << 'EOF'
#!/usr/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && cd ../.. && pwd)/Code/YT-Downloader"
source "$SCRIPT_DIR/.venv/bin/activate"
exec python3 "$SCRIPT_DIR/yt-downloader" "$@"
EOF

chmod +x "$INSTALL_DIR/yt-downloader"

SHELL_NAME=$(basename "$SHELL")
if [ "$SHELL_NAME" = "zsh" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ "$SHELL_NAME" = "bash" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
else
    SHELL_CONFIG="$HOME/.bashrc"
fi

if ! grep -q '.local/bin' "$SHELL_CONFIG" 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_CONFIG"
    echo "Added $HOME/.local/bin to PATH in $SHELL_CONFIG"
    echo "Run 'source $SHELL_CONFIG' or restart terminal"
fi

echo "YT-Downloader installed successfully"
echo "Run with: yt-downloader"
