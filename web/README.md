# TechEX - Parcel Tracking System

A beautiful, modern web-based parcel tracking system built with Flask, Vite, Tailwind CSS, and DaisyUI.

## Features

- 📦 **Add New Parcels**: Register packages with detailed information
- 📋 **List All Parcels**: View and filter your shipments with a beautiful interface
- ✏️ **Edit Parcels**: Update parcel status, delivery dates, costs, and weights
- 🗑️ **Remove Parcels**: Delete parcels from the system
- 📊 **Statistics Dashboard**: View comprehensive analytics and insights
- 🌙 **Dark Mode Toggle**: Switch between light and dark themes
- 📱 **Responsive Design**: Works perfectly on mobile, tablet, and desktop
- ✨ **Modern UI**: Glassmorphism pill navbar with smooth animations
- 🎨 **Modern Stack**: Vite + Tailwind CSS + DaisyUI for optimal performance

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
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
   python main.py
   ```
   
   **Or use the automated build script:**
   ```bash
   python build.py
   ```

5. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

## Usage

### Adding a Parcel
1. Click "Add New Parcel" from the home page or navigation
2. Fill in all required information:
   - Tracking number (unique identifier)
   - Sender and origin information
   - Receiver and destination information
   - Cost, weight, and dispatch date
3. Click "Add Parcel" to save

### Managing Parcels
- **View All**: Click "All Parcels" to see your complete shipment list
- **Filter**: Use status filters (All, Delivered, Pending) to find specific parcels
- **Search**: Use the search bar to find parcels by tracking number, sender, or receiver
- **Edit**: Click the edit button on any parcel to modify its details
- **Delete**: Click the delete button to remove a parcel (with confirmation)

### Viewing Statistics
- Navigate to "Statistics" to see comprehensive analytics
- View delivery rates, cost analysis, weight statistics
- Get insights and recommendations for your shipping operations

## Data Storage

This application uses **in-memory storage**, meaning:
- Data is stored in RAM while the application is running
- Data will be lost when the application is restarted
- Perfect for testing and demonstration purposes
- To persist data, you would need to integrate a database

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, JavaScript (ES6+)
- **Styling**: DaisyUI 5 + Tailwind CSS
- **Icons**: Font Awesome 6
- **Design**: Responsive, mobile-first approach

## Features Highlight

### Beautiful UI Components
- Modern card-based layout
- Smooth animations and transitions
- Interactive hover effects
- Gradient backgrounds and shadows

### Dark Mode Support
- Automatic theme persistence
- Smooth theme transitions
- System-wide dark/light mode toggle

### Responsive Design
- Mobile-optimized interface
- Tablet-friendly layouts
- Desktop-enhanced experience
- Touch-friendly controls

### Form Validation
- Real-time input validation
- Clear error messaging
- User-friendly feedback
- Accessibility features

## Development

To modify or extend the application:

1. **Templates**: HTML templates are in the `templates/` folder
2. **Routes**: Flask routes are defined in `main.py`
3. **Styling**: Custom CSS is embedded in the templates
4. **JavaScript**: Interactive features are included in each template

## Customization

### Changing Colors
The application uses DaisyUI's theming system. You can customize colors by modifying the CSS variables or changing the data-theme attribute.

### Adding New Features
1. Add new routes in `main.py`
2. Create corresponding HTML templates
3. Update navigation in `base.html`

### Integrating a Database
To add persistent storage:
1. Choose a database (SQLite, PostgreSQL, etc.)
2. Add SQLAlchemy or similar ORM
3. Replace in-memory `parcels_data` with database models
4. Update CRUD operations

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

Feel free to contribute by:
- Reporting bugs
- Suggesting new features
- Improving the UI/UX
- Adding new functionality

---

**TechEX v1.0** - Built with ❤️ using Flask & DaisyUI
