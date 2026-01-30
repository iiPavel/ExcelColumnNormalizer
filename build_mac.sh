#!/usr/bin/env bash
set -euo pipefail

# Builds a macOS app bundle for the project using PyInstaller.
# Run this on a macOS machine with Python 3.8+.

ROOT_DIR=$(cd "$(dirname "$0")" && pwd)
VENV_DIR="$ROOT_DIR/.venv_mac"

echo "Creating virtualenv in $VENV_DIR..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

echo "Upgrading pip and installing build dependencies..."
pip install --upgrade pip
pip install -r "$ROOT_DIR/requirements.txt"
pip install pyinstaller

echo "Running PyInstaller (this may take a while)..."
# Use the provided spec which collects PySide6 resources and includes config.json
pyinstaller --noconfirm "$ROOT_DIR/app.spec"

echo "Build finished. The app bundle is in dist/ExcelColumnNormalizer" 
echo "You can open it with: open dist/ExcelColumnNormalizer/ExcelColumnNormalizer.app"

deactivate || true
