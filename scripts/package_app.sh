#!/usr/bin/env bash
set -euo pipefail

# Packages the PyInstaller dist folder into a macOS .app bundle.
# Assumes the PyInstaller output directory is dist/ExcelColumnNormalizer
# and contains an executable named `ExcelColumnNormalizer`.

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
DIST_DIR="$ROOT_DIR/dist/ExcelColumnNormalizer"
APP_DIR="$ROOT_DIR/dist/ExcelColumnNormalizer.app"
APP_NAME="ExcelColumnNormalizer"
BUNDLE_ID=${BUNDLE_ID:-com.example.ExcelColumnNormalizer}
VERSION=${VERSION:-1.0}

if [ ! -d "$DIST_DIR" ]; then
  echo "Expected PyInstaller output at $DIST_DIR"
  exit 1
fi

rm -rf "$APP_DIR"
mkdir -p "$APP_DIR/Contents/MacOS"
mkdir -p "$APP_DIR/Contents/Resources"

# Move all files from dist/ExcelColumnNormalizer into Contents/MacOS
cp -R "$DIST_DIR"/* "$APP_DIR/Contents/MacOS/"

# Create a minimal Info.plist
cat > "$APP_DIR/Contents/Info.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleName</key>
  <string>${APP_NAME}</string>
  <key>CFBundleDisplayName</key>
  <string>${APP_NAME}</string>
  <key>CFBundleIdentifier</key>
  <string>${BUNDLE_ID}</string>
  <key>CFBundleVersion</key>
  <string>${VERSION}</string>
  <key>CFBundleExecutable</key>
  <string>${APP_NAME}</string>
  <key>CFBundlePackageType</key>
  <string>APPL</string>
</dict>
</plist>
EOF

# Ensure executable permission
chmod +x "$APP_DIR/Contents/MacOS/$APP_NAME"

echo "Packaged app created at: $APP_DIR"

echo "You can run it with: open \"$APP_DIR\"" 
