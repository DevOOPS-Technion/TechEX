# TechEX - Parcel Tracking System

A beautiful, modern web-based parcel tracking system built with Flask, Vite, Tailwind CSS, and DaisyUI.

> Looking for deployment? See the root `README.md` and `aws/README.md` for Docker + AWS details. This file stays focused on the app itself.

## Features

- 📦 **Add New Parcels**: Register packages with detailed information
- 📋 **List All Parcels**: View and filter your shipments with a beautiful interface
- ✏️ **Edit Parcels**: Update parcel status, delivery dates, costs, and weights
- 🗑️ **Remove Parcels**: Delete parcels from the system
- 📊 **Statistics Dashboard**: View comprehensive analytics and insights
- 🌙 **Dark Mode Toggle**: Switch between light and dark themes
- 📱 **Responsive Design**: Works perfectly on mobile, tablet, and desktop
- ✨ **Modern UI**: Vite + Tailwind CSS + DaisyUI for optimal performance

## Installation

1. **Install Python dependencies:**
   ```bash
   cd web && pip install -r requirements.txt
   ```
2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```
3. **Build CSS assets:**
   ```bash
   npm run build
   ```
4. **Run the application:**
   ```bash
   python build.py
   # open http://localhost:5000
   ```

Small note: data is in-memory by design (demo-friendly). Bring your own DB if you want it to remember things after a reboot.

---
TechEX v1.0 — built with ❤️ and just enough caffeine.
