#!/usr/bin/env python3
"""
Build script for TechEX - Builds CSS and starts Flask server
"""

import subprocess
import sys
import os

def run_command(command):
    """Run a command and handle errors"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {command}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running: {command}")
        print(f"Error: {e.stderr}")
        return None

def main():
    print("🚀 TechEX Build & Start Script")
    print("="*40)
    
    # Build CSS with Vite
    print("📦 Building CSS with Vite...")
    result = run_command("npm run build")
    
    if result is None:
        print("❌ CSS build failed. Make sure to run 'npm install' first.")
        return 1
    
    print("✅ CSS built successfully!")
    
    # Copy assets (images) to static directory after build
    print("🖼️  Copying assets to static directory...")
    import shutil
    import glob
    
    # Copy PNG files from assets to static
    for png_file in glob.glob("assets/*.png"):
        filename = os.path.basename(png_file)
        shutil.copy2(png_file, os.path.join("static", filename))
        print(f"   📷 Copied {filename}")
    
    print("✅ Assets copied successfully!")
    
    # Display server info
    print("\n" + "="*50)
    print("🎉 TechEX Parcel Tracking System")
    print("="*50)
    print("📱 Interface:       http://localhost:5000")
    print("="*50)
    
    # Start Flask server
    try:
        from main import app
        print("\n🚀 Starting Flask server...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped.")
    except Exception as e:
        print(f"\n❌ Error starting Flask: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
