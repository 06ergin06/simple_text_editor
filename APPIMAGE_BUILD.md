# AppImage Build Instructions

## Building the AppImage

To build the Hakki Text Editor as an AppImage, follow these steps:

### Prerequisites

1. Install required system packages:
```bash
sudo apt-get install python3 python3-gi gir1.2-gtk-4.0 wget
```

2. The build script will automatically download `appimagetool` if it's not already installed.

### Build Steps

1. Navigate to the project directory:
```bash
cd /home/ergin/Projects/python_gtk
```

2. Run the build script:
```bash
./build-appimage.sh
```

3. The AppImage will be created as `Hakki-Text-Editor-x86_64.AppImage` in the current directory.

### Running the AppImage

Once built, you can run the AppImage directly:
```bash
./Hakki-Text-Editor-x86_64.AppImage
```

### Distribution

The generated AppImage is a single executable file that can be distributed to users. They only need to:
1. Download the AppImage
2. Make it executable: `chmod +x Hakki-Text-Editor-x86_64.AppImage`
3. Run it: `./Hakki-Text-Editor-x86_64.AppImage`

### Notes

- The AppImage includes all necessary Python dependencies bundled inside
- GTK4 and GObject Introspection libraries need to be available on the target system
- Translation files are automatically included if available in the `po/` directory
