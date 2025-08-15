from datetime import datetime

#-----------------------------
# Add Parcel Function
#-----------------------------
def addParcel(parcels_data):
    """Adds a new parcel to the database"""
    while True:
        try:
            print("\n=== ADD NEW PARCEL ===\n")
            
            # Get tracking number
            tracking_number = input("Enter Tracking Number:\n> ").strip()
            if not tracking_number:
                print("\n"+"="*80)
                print("❌ Error: Tracking Number cannot be empty")
                print("="*80+"\n\n")
                continue
            
            # Check for duplicate tracking numbers
            for parcel in parcels_data:
                if parcel["tracking_number"] == tracking_number:
                    print("\n"+"="*80)
                    print("❌ Error: Tracking Number already exists")
                    print("="*80+"\n\n")
                    break
            else:
                # No duplicate found, continue with input
                pass
            
            if any(parcel["tracking_number"] == tracking_number for parcel in parcels_data):
                continue
            
            # Get sender info
            sender = input("Enter Sender:\n> ").strip()
            if not sender:
                print("\n"+"="*80)
                print("❌ Error: Sender cannot be empty")
                print("="*80+"\n\n")
                continue
            
            # Get receiver info
            receiver = input("Enter Receiver:\n> ").strip()
            if not receiver:
                print("\n"+"="*80)
                print("❌ Error: Receiver cannot be empty")
                print("="*80+"\n\n")
                continue
            
            # Get origin location
            origin = input("Enter Origin:\n> ").strip()
            if not origin:
                print("\n"+"="*80)
                print("❌ Error: Origin cannot be empty")
                print("="*80+"\n\n")
                continue
            
            # Get destination location
            destination = input("Enter Destination:\n> ").strip()
            if not destination:
                print("\n"+"="*80)
                print("❌ Error: Destination cannot be empty")
                print("="*80+"\n\n")
                continue
            
            # Get parcel cost
            cost = float(input("Enter Cost (₪):\n> "))
            if cost < 0:
                print("\n"+"="*80)
                print("❌ Error: Cost cannot be negative")
                print("="*80+"\n\n")
                continue
            
            # Get parcel weight
            weight = float(input("Enter Weight (kg):\n> "))
            if weight <= 0:
                print("\n"+"="*80)
                print("❌ Error: Weight must be greater than 0")
                print("="*80+"\n\n")
                continue
            
            # Get dispatch date
            dispatch_date = input("Enter Dispatch Date (YYYY-MM-DD):\n> ").strip()
            if not dispatch_date:
                print("\n"+"="*80)
                print("❌ Error: Dispatch Date cannot be empty")
                print("="*80+"\n\n")
                continue
            
            # Check if date format is correct
            try:
                datetime.strptime(dispatch_date, "%Y-%m-%d")
            except ValueError:
                print("\n"+"="*80)
                print("❌ Error: Invalid date format. Use YYYY-MM-DD")
                print("="*80+"\n\n")
                continue
            
            # Create new parcel ID
            if parcels_data:
                new_id = str(max(int(parcel["id"]) for parcel in parcels_data) + 1)
            else:
                new_id = "1"
            
            # Build new parcel record
            new_parcel = {
                "id": new_id,
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
            
            # Add to database
            parcels_data.append(new_parcel)
            
            # Show success message
            print("\n"+"="*80)
            print(f"✅ SUCCESS: Parcel '{tracking_number}' added successfully!")
            print("="*80+"\n\n")
            
            # Post-operation menu
            print("\n(1) - ADD another Parcel")
            print("(2) - Go Back")
            print("(3) - Quit")
            
            action = int(input("> "))
            if action == 1:
                continue
            elif action == 2:
                return True
            elif action == 3:
                print("Exiting program. Goodbye!")
                return False
            else:
                print("Invalid choice. Returning to main menu")
                return True
                
        except ValueError:
            print("\n"+"="*80)
            print("❌ Error: Please enter valid values.")
            print("="*80+"\n\n")
            
            # Error recovery menu
            try:
                print("\n(1) - Try Again")
                print("(2) - Go Back")
                print("(3) - Quit")
                action = int(input("> "))
                if action == 1:
                    continue
                elif action == 2:
                    return True
                elif action == 3:
                    print("Exiting program. Goodbye!")
                    return False
                else:
                    print("Invalid choice. Returning to main menu")
                    return True
            except ValueError:
                print("Invalid input. Returning to main menu.")
                return True


#-----------------------------
# Edit Parcel Function
#-----------------------------
def editParcel(parcels_data):
    """Edit an existing parcel"""
    if not parcels_data:
        print("\n❌ No parcels in the database.")
        return True
    
    while True:
        try:
            print("\n=== EDIT PARCEL ===\n")
            
            # Show available parcels
            print("Available Parcels:")
            for parcel in parcels_data:
                print(f"ID: {parcel['id']} | Tracking: {parcel['tracking_number']} | Status: {parcel['status']}")
            
            parcel_id = input("\nEnter Parcel ID to edit:\n> ").strip()
            
            # Look for the parcel
            selected_parcel = None
            for parcel in parcels_data:
                if parcel["id"] == parcel_id:
                    selected_parcel = parcel
                    break
            
            if not selected_parcel:
                print("\n❌ Error: Parcel not found")
                continue
            
            print(f"\nEditing Parcel: {selected_parcel['tracking_number']}")
            print("\nWhat would you like to edit?")
            print("1. Status")
            print("2. Delivery Date")
            print("3. Cost")
            print("4. Weight")
            print("5. Go Back")
            
            choice = int(input("> "))
            
            if choice == 1:
                # Edit status
                print("\nSelect new status:")
                print("1. pending")
                print("2. delivered")
                status_choice = int(input("> "))
                if status_choice == 1:
                    selected_parcel["status"] = "pending"
                    selected_parcel["delivery_date"] = None
                elif status_choice == 2:
                    selected_parcel["status"] = "delivered"
                    delivery_date = input("Enter Delivery Date (YYYY-MM-DD):\n> ").strip()
                    try:
                        datetime.strptime(delivery_date, "%Y-%m-%d")
                        selected_parcel["delivery_date"] = delivery_date
                    except ValueError:
                        print("❌ Error: Invalid date format")
                        continue
                else:
                    print("❌ Invalid choice")
                    continue
                    
            elif choice == 2:
                # Edit delivery date
                delivery_date = input("Enter Delivery Date (YYYY-MM-DD) or 'none' to clear:\n> ").strip()
                if delivery_date.lower() == 'none':
                    selected_parcel["delivery_date"] = None
                    selected_parcel["status"] = "pending"
                else:
                    try:
                        datetime.strptime(delivery_date, "%Y-%m-%d")
                        selected_parcel["delivery_date"] = delivery_date
                        selected_parcel["status"] = "delivered"
                    except ValueError:
                        print("❌ Error: Invalid date format")
                        continue
                        
            elif choice == 3:
                # Edit cost
                new_cost = float(input("Enter new cost:\n> "))
                if new_cost < 0:
                    print("❌ Error: Cost cannot be negative")
                    continue
                selected_parcel["cost"] = new_cost
                
            elif choice == 4:
                # Edit weight
                new_weight = float(input("Enter new weight:\n> "))
                if new_weight <= 0:
                    print("❌ Error: Weight must be greater than 0")
                    continue
                selected_parcel["weight"] = new_weight
                
            elif choice == 5:
                return True
                
            else:
                print("❌ Invalid choice")
                continue
            
            print("\n✅ Parcel updated successfully!")
            
            # Post-edit menu
            print("\n(1) - Edit another Parcel")
            print("(2) - Go Back")
            print("(3) - Quit")
            
            action = int(input("> "))
            if action == 1:
                continue
            elif action == 2:
                return True
            elif action == 3:
                return False
            else:
                return True
                
        except ValueError:
            print("❌ Error: Invalid input")
            continue


#-----------------------------
# List Parcels Function
#-----------------------------
def listParcels(parcels_data):
    """Display all parcels in the database"""
    if not parcels_data:
        print("\n❌ No parcels in the database.")
    else:
        print("\n=== PARCEL LIST ===\n")
        
        # Calculate how wide each column should be
        id_width = max(len("ID"), max(len(p["id"]) for p in parcels_data)) + 2
        tracking_width = max(len("Tracking"), max(len(p["tracking_number"]) for p in parcels_data)) + 2
        sender_width = max(len("Sender"), max(len(p["sender"]) for p in parcels_data)) + 2
        receiver_width = max(len("Receiver"), max(len(p["receiver"]) for p in parcels_data)) + 2
        status_width = max(len("Status"), max(len(p["status"]) for p in parcels_data)) + 2
        cost_width = max(len("Cost"), max(len(f"₪{p['cost']:.2f}") for p in parcels_data)) + 2
        
        # Create table header
        header = f"{'ID':<{id_width}}{'Tracking':<{tracking_width}}{'Sender':<{sender_width}}{'Receiver':<{receiver_width}}{'Status':<{status_width}}{'Cost':<{cost_width}}"
        print(header)
        print("-" * len(header))
        
        # Print each parcel
        for parcel in parcels_data:
            row = f"{parcel['id']:<{id_width}}{parcel['tracking_number']:<{tracking_width}}{parcel['sender']:<{sender_width}}{parcel['receiver']:<{receiver_width}}{parcel['status']:<{status_width}}₪{parcel['cost']:.2f}"
            print(row)
    
    # User options after viewing
    while True:
        try:
            print("\n(2) - Go Back")
            print("(3) - Quit")
            action = int(input("> "))
            if action == 3:
                print("Exiting program. Goodbye!")
                return False
            elif action == 2:
                return True
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


#-----------------------------
# Remove Parcel Function
#-----------------------------
def removeParcel(parcels_data):
    """Remove a parcel from the database"""
    if not parcels_data:
        print("\n❌ No parcels in the database.")
        return True
    
    while True:
        try:
            print("\n=== REMOVE PARCEL ===\n")
            
            # Show parcels to choose from
            print("Available Parcels:")
            for parcel in parcels_data:
                print(f"ID: {parcel['id']} | Tracking: {parcel['tracking_number']} | Receiver: {parcel['receiver']}")
            
            parcel_id = input("\nEnter Parcel ID to remove:\n> ").strip()
            
            # Search and remove the parcel
            for i, parcel in enumerate(parcels_data):
                if parcel["id"] == parcel_id:
                    removed_parcel = parcels_data.pop(i)
                    print(f"\n✅ SUCCESS: Parcel '{removed_parcel['tracking_number']}' removed successfully!")
                    break
            else:
                print("\n❌ Error: Parcel not found")
                continue
            
            # Post-removal menu
            print("\n(1) - Remove another Parcel")
            print("(2) - Go Back")
            print("(3) - Quit")
            
            action = int(input("> "))
            if action == 1:
                if not parcels_data:
                    print("\n❌ No more parcels in the database.")
                    return True
                continue
            elif action == 2:
                return True
            elif action == 3:
                return False
            else:
                return True
                
        except ValueError:
            print("❌ Error: Invalid input")
            continue


#-----------------------------
# Parcel Statistics Function
#-----------------------------
def parcelStatistics(parcels_data):
    """Display parcel statistics"""
    if not parcels_data:
        print("\n❌ No parcels in the database.")
    else:
        print("\n=== PARCEL STATISTICS ===\n")
        
        # Do the math
        total_parcels = len(parcels_data)
        delivered_count = 0
        pending_count = 0
        total_cost = 0
        total_weight = 0
        
        for parcel in parcels_data:
            if parcel["status"] == "delivered":
                delivered_count += 1
            elif parcel["status"] == "pending":
                pending_count += 1
            total_cost += parcel["cost"]
            total_weight += parcel["weight"]
        
        # Calculate averages
        avg_cost = total_cost / total_parcels if total_parcels > 0 else 0
        avg_weight = total_weight / total_parcels if total_parcels > 0 else 0
        
        # Prepare data for the table
        stats_info = [
            ("Total Parcels", str(total_parcels)),
            ("Delivered", str(delivered_count)),
            ("Pending", str(pending_count)),
            ("Total Cost", f"₪{total_cost:.2f}"),
            ("Total Weight", f"{total_weight:.2f} kg"),
            ("Average Cost", f"₪{avg_cost:.2f}"),
            ("Average Weight", f"{avg_weight:.2f} kg")
        ]
        
        # Add delivery rate if we have delivered parcels
        if delivered_count > 0:
            delivery_rate = (delivered_count / total_parcels) * 100
            stats_info.append(("Delivery Rate", f"{delivery_rate:.1f}%"))
        
        # Figure out column widths
        label_width = max(len(stat[0]) for stat in stats_info) + 2
        value_width = max(len(stat[1]) for stat in stats_info) + 2
        
        # Make the table header
        header = f"{'Metric':<{label_width}}{'Value':<{value_width}}"
        print(header)
        print("-" * len(header))
        
        # Print all the stats
        for label, value in stats_info:
            print(f"{label:<{label_width}}{value:<{value_width}}")
    
    # User menu after stats
    while True:
        try:
            print("\n(2) - Go Back")
            print("(3) - Quit")
            action = int(input("> "))
            if action == 3:
                print("Exiting program. Goodbye!")
                return False
            elif action == 2:
                return True
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")