#!/usr/bin/env python3
"""
TechEX - Parcel Tracking System
Flask web application with DaisyUI 5
"""

import os
import shutil
import glob
from main import app

def copy_assets():
    """Copy assets to static directory if they're missing"""
    if os.path.exists("assets"):
        for png_file in glob.glob("assets/*.png"):
            filename = os.path.basename(png_file)
            static_path = os.path.join("static", filename)
            if not os.path.exists(static_path):
                shutil.copy2(png_file, static_path)
                print(f"📷 Copied {filename} to static/")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 TechEX Parcel Tracking System - DaisyUI 5")
    print("="*60)
    print("📱 Main Interface:  http://localhost:5000")
    print("🧪 DaisyUI Test:    http://localhost:5000/test")
    print("🌙 Dark Mode:       Toggle available in navbar")
    print("📦 Features:        Responsive, modern UI")
    print("="*60 + "\n")
    
    # Ensure assets are copied
    copy_assets()
    
    try:
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n👋 Application stopped.")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("📋 Check the requirements are installed: pip install -r requirements.txt")
