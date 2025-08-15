from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Debug static files
static_path = os.path.join(os.getcwd(), 'static')
print(f"Current working directory: {os.getcwd()}")
print(f"Static folder absolute path: {static_path}")
print(f"Static files exist: {os.path.exists(static_path)}")
if os.path.exists(static_path):
    print(f"Static directory contents: {os.listdir(static_path)}")
print(f"Flask static folder: {app.static_folder}")
print(f"Flask static url path: {app.static_url_path}")

# Version of the program
version = "1.0"

# Health check endpoint for Elastic Beanstalk
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'version': version,
        'timestamp': datetime.now().isoformat()
    }), 200

# In-memory parcel data storage
parcels_data = [
    {
        "id": "1",
        "tracking_number": "LP000123456CN",
        "sender": "Cainiao Warehouse",
        "receiver": "Yossi Levi",
        "origin": "Cainiao, China",
        "destination": "Tel Aviv, Israel",
        "status": "delivered",
        "cost": 18.5,
        "weight": 1.2,
        "dispatch_date": "2025-07-20",
        "delivery_date": "2025-08-01"
    },
    {
        "id": "2",
        "tracking_number": "YT123456789CN",
        "sender": "Shenzhen Logistics",
        "receiver": "Noa Cohen",
        "origin": "Shenzhen, China",
        "destination": "Haifa, Israel",
        "status": "delivered",
        "cost": 22.0,
        "weight": 2.0,
        "dispatch_date": "2025-07-18",
        "delivery_date": "2025-07-29"
    },
    {
        "id": "3",
        "tracking_number": "LP987654321CN",
        "sender": "Cainiao Hub",
        "receiver": "Avi Mizrahi",
        "origin": "Guangzhou, China",
        "destination": "Jerusalem, Israel",
        "status": "pending",
        "cost": 19.75,
        "weight": 1.7,
        "dispatch_date": "2025-08-03",
        "delivery_date": None
    },
    {
        "id": "4",
        "tracking_number": "UB123987456CN",
        "sender": "Cainiao Dispatch",
        "receiver": "Maya Shalom",
        "origin": "Hangzhou, China",
        "destination": "Ramat Gan, Israel",
        "status": "delivered",
        "cost": 21.3,
        "weight": 0.8,
        "dispatch_date": "2025-07-15",
        "delivery_date": "2025-07-27"
    },
    {
        "id": "5",
        "tracking_number": "YT987321654CN",
        "sender": "Yiwu Cainiao",
        "receiver": "Daniel Ben-David",
        "origin": "Yiwu, China",
        "destination": "Be'er Sheva, Israel",
        "status": "pending",
        "cost": 20.0,
        "weight": 3.2,
        "dispatch_date": "2025-08-04",
        "delivery_date": None
    },
    {
        "id": "6",
        "tracking_number": "LP456789123CN",
        "sender": "Cainiao Logistics",
        "receiver": "Tamar Azulay",
        "origin": "Shanghai, China",
        "destination": "Netanya, Israel",
        "status": "delivered",
        "cost": 25.6,
        "weight": 2.5,
        "dispatch_date": "2025-07-22",
        "delivery_date": "2025-08-02"
    }
]

def get_next_id():
    """Generate the next available ID"""
    if parcels_data:
        return str(max(int(parcel["id"]) for parcel in parcels_data) + 1)
    return "1"

def find_parcel_by_id(parcel_id):
    """Find a parcel by its ID"""
    for parcel in parcels_data:
        if parcel["id"] == parcel_id:
            return parcel
    return None

def validate_date(date_string):
    """Validate date format YYYY-MM-DD"""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_tracking_number_unique(tracking_number, exclude_id=None):
    """Check if tracking number is unique"""
    for parcel in parcels_data:
        if parcel["tracking_number"] == tracking_number and parcel["id"] != exclude_id:
            return False
    return True

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', version=version, parcels=parcels_data)

@app.route('/parcels')
def list_parcels():
    """List all parcels"""
    return render_template('list_parcels.html', parcels=parcels_data)

@app.route('/add_parcel', methods=['GET', 'POST'])
def add_parcel():
    """Add a new parcel"""
    if request.method == 'POST':
        # Get form data
        tracking_number = request.form.get('tracking_number', '').strip()
        sender = request.form.get('sender', '').strip()
        receiver = request.form.get('receiver', '').strip()
        origin = request.form.get('origin', '').strip()
        destination = request.form.get('destination', '').strip()
        
        try:
            cost = float(request.form.get('cost', 0))
            weight = float(request.form.get('weight', 0))
        except ValueError:
            flash('Invalid cost or weight value', 'error')
            return render_template('add_parcel.html')
        
        dispatch_date = request.form.get('dispatch_date', '').strip()
        
        # Validation
        errors = []
        
        if not tracking_number:
            errors.append('Tracking Number is required')
        elif not is_tracking_number_unique(tracking_number):
            errors.append('Tracking Number already exists')
            
        if not sender:
            errors.append('Sender is required')
        if not receiver:
            errors.append('Receiver is required')
        if not origin:
            errors.append('Origin is required')
        if not destination:
            errors.append('Destination is required')
        if cost < 0:
            errors.append('Cost cannot be negative')
        if weight <= 0:
            errors.append('Weight must be greater than 0')
        if not dispatch_date:
            errors.append('Dispatch Date is required')
        elif not validate_date(dispatch_date):
            errors.append('Invalid date format. Use YYYY-MM-DD')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('add_parcel.html')
        
        # Create new parcel
        new_parcel = {
            "id": get_next_id(),
            "tracking_number": tracking_number,
            "sender": sender,
            "receiver": receiver,
            "origin": origin,
            "destination": destination,
            "status": "pending",
            "cost": cost,
            "weight": weight,
            "dispatch_date": dispatch_date,
            "delivery_date": None
        }
        
        parcels_data.append(new_parcel)
        flash(f'Parcel {tracking_number} added successfully!', 'success')
        return redirect(url_for('list_parcels'))
    
    return render_template('add_parcel.html')

@app.route('/edit_parcel/<parcel_id>', methods=['GET', 'POST'])
def edit_parcel(parcel_id):
    """Edit an existing parcel"""
    parcel = find_parcel_by_id(parcel_id)
    if not parcel:
        flash('Parcel not found', 'error')
        return redirect(url_for('list_parcels'))
    
    if request.method == 'POST':
        # Get form data
        field = request.form.get('field')
        value = request.form.get('value', '').strip()
        
        if field == 'status':
            if value in ['pending', 'delivered']:
                parcel['status'] = value
                if value == 'pending':
                    parcel['delivery_date'] = None
                flash('Status updated successfully!', 'success')
            else:
                flash('Invalid status value', 'error')
                
        elif field == 'delivery_date':
            if value.lower() == 'none' or value == '':
                parcel['delivery_date'] = None
                parcel['status'] = 'pending'
                flash('Delivery date cleared successfully!', 'success')
            elif validate_date(value):
                parcel['delivery_date'] = value
                parcel['status'] = 'delivered'
                flash('Delivery date updated successfully!', 'success')
            else:
                flash('Invalid date format. Use YYYY-MM-DD', 'error')
                
        elif field == 'cost':
            try:
                new_cost = float(value)
                if new_cost < 0:
                    flash('Cost cannot be negative', 'error')
                else:
                    parcel['cost'] = new_cost
                    flash('Cost updated successfully!', 'success')
            except ValueError:
                flash('Invalid cost value', 'error')
                
        elif field == 'weight':
            try:
                new_weight = float(value)
                if new_weight <= 0:
                    flash('Weight must be greater than 0', 'error')
                else:
                    parcel['weight'] = new_weight
                    flash('Weight updated successfully!', 'success')
            except ValueError:
                flash('Invalid weight value', 'error')
        
        return redirect(url_for('edit_parcel', parcel_id=parcel_id))
    
    return render_template('edit_parcel.html', parcel=parcel)

@app.route('/remove_parcel/<parcel_id>', methods=['POST'])
def remove_parcel(parcel_id):
    """Remove a parcel"""
    for i, parcel in enumerate(parcels_data):
        if parcel["id"] == parcel_id:
            removed_parcel = parcels_data.pop(i)
            flash(f'Parcel {removed_parcel["tracking_number"]} removed successfully!', 'success')
            break
    else:
        flash('Parcel not found', 'error')
    
    return redirect(url_for('list_parcels'))

@app.route('/statistics')
def statistics():
    """Display parcel statistics"""
    if not parcels_data:
        stats = {
            'total_parcels': 0,
            'delivered_count': 0,
            'pending_count': 0,
            'total_cost': 0,
            'total_weight': 0,
            'avg_cost': 0,
            'avg_weight': 0,
            'delivery_rate': 0
        }
    else:
        total_parcels = len(parcels_data)
        delivered_count = sum(1 for p in parcels_data if p["status"] == "delivered")
        pending_count = sum(1 for p in parcels_data if p["status"] == "pending")
        total_cost = sum(p["cost"] for p in parcels_data)
        total_weight = sum(p["weight"] for p in parcels_data)
        
        stats = {
            'total_parcels': total_parcels,
            'delivered_count': delivered_count,
            'pending_count': pending_count,
            'total_cost': total_cost,
            'total_weight': total_weight,
            'avg_cost': total_cost / total_parcels,
            'avg_weight': total_weight / total_parcels,
            'delivery_rate': (delivered_count / total_parcels) * 100 if total_parcels > 0 else 0
        }
    
    return render_template('statistics.html', stats=stats)

@app.route('/api/parcels')
def api_parcels():
    """API endpoint to get parcels data"""
    return jsonify(parcels_data)

@app.route('/test')
def test_daisyui():
    """Test page for DaisyUI components"""
    from flask import send_from_directory
    return send_from_directory('.', 'test_daisyui.html')

@app.route('/test-images')
def test_images():
    """Test page for logo images"""
    import os
    static_files = os.listdir('static')
    return f'''
    <html>
    <head><title>Image Test</title></head>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h1>Testing Logo Images</h1>
        <h2>Light Logo:</h2>
        <img src="/static/TechEX_light.png" alt="Light Logo" style="border: 1px solid black; max-width: 200px;">
        <h2>Dark Logo:</h2>
        <img src="/static/TechEX_dark.png" alt="Dark Logo" style="border: 1px solid black; max-width: 200px;">
        <h2>Direct Links:</h2>
        <a href="/static/TechEX_light.png" target="_blank">Light Logo Direct</a><br>
        <a href="/static/TechEX_dark.png" target="_blank">Dark Logo Direct</a><br>
        <h2>Static Directory Contents:</h2>
        <pre>{static_files}</pre>
    </body>
    </html>
    '''



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
