from functions import *

version = "1.0" # Version of the program

#-----------------------------
# Parcel List
#-----------------------------
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



#-----------------------------
# Exit Menu
#-----------------------------
def exitMenu():
    """Exit the program"""
    print("Exiting program. Goodbye!")
    return False # Signal to exit the program


#-----------------------------
# Display Menu
#-----------------------------
def displayMenu():
    """Display the main menu options"""
    print("\n"+"="*30)
    print(r"""
  _____       _    _____  __
 |_   _|__ __| |_ | __\ \/ /
   | |/ -_) _| ' \| _| >  < 
   |_|\___\__|_||_|___/_/\_\.
    """)
    print("="*30+"\n")
    print("| 1 | Add Parcel")
    print("| 2 | Edit Parcel")
    print("| 3 | List Parcels")
    print("| 4 | Remove Parcel")
    print("| 5 | Parcel Statistics")
    print("| 6 | Exit")

#-----------------------------
# Main program loop
#-----------------------------
def mainMenuHandler():
    """Main program function that runs TechEX"""
    while True:
        displayMenu()
        
        # Check if the user input is a number
        try:
            choice = int(input("\n> "))
        except ValueError:
            print("❌ Error: Invalid input.")
            continue
        
        # Process user choice
        continue_program = True
        match choice:
            case 1:  
                continue_program = addParcel(parcels_data)
            case 2: 
                continue_program = editParcel(parcels_data)
            case 3: 
                continue_program = listParcels(parcels_data)
            case 4:  
                continue_program = removeParcel(parcels_data)
            case 5:
                continue_program = parcelStatistics(parcels_data)
            case 6:
                print("\nExiting program. Goodbye!")
                break
            case _:  # Default case for invalid choices
                print("❌ Error: Invalid input.\nPlease enter a number between 1 and 6.")
        # Check if we should exit the program
        if not continue_program:
            break


#-----------------------------
# Run the main program
#-----------------------------
if __name__ == "__main__":
    mainMenuHandler()
