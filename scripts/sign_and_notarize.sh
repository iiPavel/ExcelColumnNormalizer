#!/usr/bin/env bash
set -euo pipefail

# Sign and notarize the .app produced by package_app.sh
# Requires Xcode command line tools and an Apple Developer ID
# Usage:
#   export CODESIGN_IDENTITY="Developer ID Application: Your Name (TEAMID)"
#   export BUNDLE_ID="com.example.ExcelColumnNormalizer"
#   export ASC_API_KEY="/path/to/AuthKey_XXX.p8" # optional for notarytool
#   ./scripts/sign_and_notarize.sh

APP_PATH="dist/ExcelColumnNormalizer.app"
APP_NAME=${APP_NAME:-ExcelColumnNormalizer}
CODESIGN_IDENTITY=${CODESIGN_IDENTITY:-}
BUNDLE_ID=${BUNDLE_ID:-com.example.ExcelColumnNormalizer}

if [ ! -d "$APP_PATH" ]; then
  echo "App bundle not found at $APP_PATH"
  exit 1
fi

if [ -z "$CODESIGN_IDENTITY" ]; then
  echo "Please set CODESIGN_IDENTITY environment variable to your Developer ID Application identity."
  exit 1
fi

echo "Codesigning $APP_PATH with identity $CODESIGN_IDENTITY..."
# Deep sign the app; adjust --entitlements if required
codesign --verbose --deep --force --options runtime -s "$CODESIGN_IDENTITY" "$APP_PATH"

echo "Verifying codesign..."
codesign --verify --deep --strict --verbose=2 "$APP_PATH"

# Notarization (optional) using notarytool if ASC_API_KEY is provided
if [ -n "${ASC_API_KEY-}" ]; then
  echo "Submitting to notary service using notarytool..."
  xcrun notarytool submit --key "$ASC_API_KEY" --key-id "$ASC_KEY_ID" --issuer "$ASC_ISSUER" "$APP_PATH" --wait
  echo "Stapling notarization ticket..."
  xcrun stapler staple "$APP_PATH"
else
  echo "ASC_API_KEY not provided; skipping notarization. To notarize, set ASC_API_KEY, ASC_KEY_ID, ASC_ISSUER environment variables and re-run."
fi

echo "Done."
