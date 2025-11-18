#!/bin/bash

# Build script for Hakki Text Editor AppImage
set -e

echo "Building Hakki Text Editor AppImage..."

# Check if appimagetool is available
if ! command -v appimagetool &> /dev/null; then
    echo "appimagetool not found. Downloading..."
    wget -c "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage" -O appimagetool
    chmod +x appimagetool
    APPIMAGETOOL=./appimagetool
else
    APPIMAGETOOL=appimagetool
fi

# Clean previous build
rm -rf AppDir
rm -f Hakki-Text-Editor-*.AppImage

# Create AppDir structure
echo "Creating AppDir structure..."
mkdir -p AppDir/usr/bin
mkdir -p AppDir/usr/share/applications
mkdir -p AppDir/usr/share/icons/hicolor/scalable/apps
mkdir -p AppDir/usr/share/locale
mkdir -p AppDir/usr/lib/python3/dist-packages/hakkitor

# Copy application files
echo "Copying application files..."
cp src/*.py AppDir/usr/lib/python3/dist-packages/hakkitor/

# Copy translations if they exist
if [ -d "po" ] && [ -f "po/tr.mo" ]; then
    echo "Copying translations..."
    mkdir -p AppDir/usr/share/locale/tr/LC_MESSAGES
    cp po/tr.mo AppDir/usr/share/locale/tr/LC_MESSAGES/hakkitor.mo
fi

# Create launcher script
echo "Creating launcher script..."
cat > AppDir/usr/bin/hakkitor << 'EOF'
#!/bin/bash
# Get the AppImage mount point (APPDIR is set by AppImage runtime)
if [ -z "$APPDIR" ]; then
    # Fallback if not running as AppImage
    SELF=$(readlink -f "$0")
    HERE=$(dirname "$SELF")
    APPDIR=$(dirname "$HERE")
fi

export PYTHONPATH="$APPDIR/usr/lib/python3/dist-packages:$PYTHONPATH"
export GI_TYPELIB_PATH="$APPDIR/usr/lib/girepository-1.0:$GI_TYPELIB_PATH"
export LD_LIBRARY_PATH="$APPDIR/usr/lib:$LD_LIBRARY_PATH"
export XDG_DATA_DIRS="$APPDIR/usr/share:${XDG_DATA_DIRS:-/usr/local/share:/usr/share}"

# Set translations path
export TEXTDOMAINDIR="$APPDIR/usr/share/locale"

# Run the application
exec python3 "$APPDIR/usr/lib/python3/dist-packages/hakkitor/main.py" "$@"
EOF
chmod +x AppDir/usr/bin/hakkitor

# Copy desktop file
echo "Copying desktop file..."
cp hakki-text-editor.desktop AppDir/usr/share/applications/
cp hakki-text-editor.desktop AppDir/

# Create/copy icon (using a symbolic icon as placeholder)
echo "Setting up icon..."
# For now, create a symlink to system icon
ln -sf /usr/share/icons/hicolor/scalable/apps/text-editor-symbolic.svg AppDir/usr/share/icons/hicolor/scalable/apps/text-editor.svg || true
# Try to use system icon
if [ -f "/usr/share/icons/hicolor/scalable/apps/text-editor.svg" ]; then
    cp /usr/share/icons/hicolor/scalable/apps/text-editor.svg AppDir/text-editor.svg
elif [ -f "/usr/share/icons/hicolor/48x48/apps/text-editor.png" ]; then
    cp /usr/share/icons/hicolor/48x48/apps/text-editor.png AppDir/text-editor.png
else
    # Create a simple SVG icon if no system icon is found
    cat > AppDir/text-editor.svg << 'SVGEOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg width="48" height="48" version="1.1" xmlns="http://www.w3.org/2000/svg">
    <rect x="8" y="8" width="32" height="32" fill="#3584e4" rx="4"/>
    <rect x="12" y="16" width="24" height="2" fill="#ffffff"/>
    <rect x="12" y="22" width="24" height="2" fill="#ffffff"/>
    <rect x="12" y="28" width="16" height="2" fill="#ffffff"/>
</svg>
SVGEOF
fi

# Create AppRun
echo "Creating AppRun..."
cat > AppDir/AppRun << 'EOF'
#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
exec "$APPDIR/usr/bin/hakkitor" "$@"
EOF
chmod +x AppDir/AppRun

# Build AppImage
echo "Building AppImage..."
ARCH=x86_64 $APPIMAGETOOL AppDir Hakki-Text-Editor-x86_64.AppImage

echo "Done! AppImage created: Hakki-Text-Editor-x86_64.AppImage"
echo "You can run it with: ./Hakki-Text-Editor-x86_64.AppImage"
