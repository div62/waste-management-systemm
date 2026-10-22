users = []
def add_user():
    print("\n ⬜ Add New User ")
    user_id = input("Enter User ID: ")
    for user in users:
        if user["id"] == user_id:
            print("Error: User ID already exists!")
            return
    name = input("Enter user name: ")
    phone = input("Enter phone number: ")
    city = input("Enter city: ")
    user = {
        "id": user_id,
        "name": name,
        "phone": phone,
        "city": city
    }
    users.append(user)
    print("\nUser added successfully!")
def view_users():
    print("\n  ⬜ Registered Users ")
    if not users:
        print("No users registered yet.")
        return
    for user in users:
        print("User ID:", user["id"])
        print("Name:", user["name"])
        print("Phone:", user["phone"])
        print("City:", user["city"])
def search_user():
    print("\n ⬜ Search User ")
    user_id = input("Enter User ID to search: ")
    for user in users:
        if user["id"] == user_id:
            print("\nUser Found!")
            print("Name:", user["name"])
            print("Phone:", user["phone"])
            print("City:", user["city"])
            return
    print("User not found!")
def update_user():
    print("\n ⬜  Update User ")
    user_id = input("Enter User ID to update: ")
    for user in users:
        if user["id"] == user_id:
            name = input(f"Enter new name [{user['name']}]: ")
            phone = input(f"Enter new phone [{user['phone']}]: ")
            city = input(f"Enter new city [{user['city']}]: ")
            if name:
                user["name"] = name
            if phone:
                user["phone"] = phone
            if city:
                user["city"] = city
            print("\nUser updated successfully!")
            return
    print("User not found!")
def delete_user():
    print("\n ⬜  Delete User ")
    user_id = input("Enter User ID to delete: ")
    for user in users:
        if user["id"] == user_id:
            confirm = input(f"Delete user {user['name']}? (yes/no): ")
            if confirm == "yes":
                users.remove(user)
                print("User deleted successfully!")
            else:
                print("Deletion cancelled.")
            return
    print("User not found!")
 
waste_types = []
def add_waste():
    print("\n ⬜  Add Waste Type ")
    waste_id = input("Enter Waste ID: ")
    for waste in waste_types:
        if waste["id"] == waste_id:
            print("Error: Waste ID already exists!")
            return
    name = input("Enter Waste Name: ")
    category = input("Enter Waste Category: ")
    description = input("Enter Description: ")
    waste = {
        "id": waste_id,
        "name": name,
        "category": category,
        "description": description
    }
    waste_types.append(waste)
    print("\nWaste type added successfully!")
def view_waste():
    print("\n ⬜  Registered Waste Types ")
    if not waste_types:
        print("No waste types registered yet.")
        return
    for waste in waste_types:
        print("Waste ID:", waste["id"])
        print("Waste Name:", waste["name"])
        print("Category:", waste["category"])
        print("Description:", waste["description"])
def search_waste():
        print("\n ⬜  Search Waste Type ")
        waste_id = input("Enter Waste ID to search: ")
        for waste in waste_types:
            if waste["id"] == waste_id:
                print("\nWaste Type Found!")
                print("Waste ID:", waste["id"])
                print("Waste Name:", waste["name"])
                print("Category:", waste["category"])
                print("Description:", waste["description"])
                return
        print("Waste type not found!")
def update_waste():
    print("\n ⬜  Update Waste Type ")
    waste_id = input("Enter Waste ID to update: ")
    for waste in waste_types:
        if waste["id"] == waste_id:
            print("Leave a  blank")
            name = input(f"Enter new name [{waste['name']}]: ")
            category = input(f"Enter new category [{waste['category']}]: ")
            description = input(  f"Enter new description [{waste['description']}]: ")
            if name:
                waste["name"] = name
            if category:
                waste["category"] = category
            if description:
                waste["description"] = description
            print("\nWaste type updated successfully!")
            return
    print("Waste type not found!")
def delete_waste():
    print("\n ⬜  Delete Waste Type ")
    waste_id = input("Enter Waste ID to delete: ")
    for waste in waste_types:
        if waste["id"] == waste_id:
            confirm = input( f"Delete waste type {waste['name']}? (yes/no): "  )
            if confirm.lower() == "yes":
                waste_types.remove(waste)
                print("Waste type deleted successfully!")
            else:
                print("Deletion cancelled.")
            return
    print("Waste type not found!")    

cities = []
def add_city():
    print("\n ⬜ Add City ")
    city_id = input("Enter City ID: ")
    for city in cities:
        if city["id"] == city_id:
            print("Error: City ID already exists!")
            return
    name = input("Enter City Name: ")
    state = input("Enter State Name: ")
    city = {
        "id": city_id,
        "name": name,
        "state": state
    }
    cities.append(city)
    print("\nCity added successfully!")
def view_cities():
    print("\n ⬜  Registered Cities ")
    if not cities:
        print("No cities registered yet.")
        return
    for city in cities:
        print("City ID:", city["id"])
        print("City Name:", city["name"])
        print("State:", city["state"])  
def search_cities():
    print("\n ⬜ Search City ")
    city_id = input("Enter City ID to search: ")
    for city in cities:
        if str(city["id"]) == city_id:
            print("\nCity Found!")
            print("City ID:", city["id"])
            print("City Name:", city["name"])
            print("State:", city["state"])
            return
    print("City not found!")
def update_city():
    print("\n ⬜ Update City ")

    city_id = input("Enter City ID to update: ")
    for city in cities:
        if str(city["id"]) == city_id:
            name = input(f"Enter new city name [{city['name']}]: ")
            state = input(f"Enter new state name [{city['state']}]: ")
            if name:
                city["name"] = name

            if state:
                city["state"] = state

            print("\nCity updated successfully!")
            return
    print("City not found!")
def delete_city():
    print("\n ⬜ Delete City ")
    city_id = input("Enter City ID to delete: ")
    for city in cities:
        if str(city["id"]) == city_id:
            confirm = input( f"Delete city {city['name']}? (yes/no): " ).lower()
            if confirm == "yes":
                cities.remove(city)
                print("\nCity deleted successfully!")
            else:
                print("Deletion cancelled.")
            return
    print("City not found!")


collections=[]
def add_collection():
    print("\n ⬜ Add Waste Collection ")
    collection_id = input("Enter Collection ID: ")
    for collection in collections:
        if collection["id"] == collection_id:
           print("Collection ID already exists!")
           return
    waste_type = input("Enter Waste Type: ")
    quantity = input("Enter Quantity (kg): ")
    city_id = input("Enter City ID: ")
    area_id = input("Enter Area ID: ")
    provider_id = input("Enter Service Provider ID: ")
    collection_date = input("Enter Collection Date (DD/MM/YYYY): ")
    status = input("Enter Collection Status: ")
    collection = {
        "id": collection_id,
        "waste_type": waste_type,
        "quantity": quantity,
        "city_id": city_id,
        "area_id": area_id,
        "provider_id": provider_id,
        "collection_date": collection_date,
        "status": status
    }
    collections.append(collection)
    print("\nWaste Collection added successfully!")
def view_collections():
    print("\n  ⬜  Registered Waste Collections  ")
    if not collections:
        print("No waste collections registered yet.")
        return
    for collection in collections:
        print("\nCollection ID:", collection["id"])
        print("Waste Type:", collection["waste_type"])
        print("Quantity:", collection["quantity"], "kg")
        print("City ID:", collection["city_id"])
        print("Area ID:", collection["area_id"])
        print("Service Provider ID:", collection["provider_id"])
        print("Collection Date:", collection["collection_date"])
        print("Status:", collection["status"])
def search_collection():
    print("\n ⬜  Search Waste Collection  ")
    collection_id = input("Enter Collection ID to search: ")
    for collection in collections:
        if collection["id"] == collection_id:
            print("\nCollection Found!")
            print("Collection ID:", collection["id"])
            print("Waste Type:", collection["waste_type"])
            print("Quantity:", collection["quantity"], "kg")
            print("City ID:", collection["city_id"])
            print("Area ID:", collection["area_id"])
            print("Service Provider ID:", collection["provider_id"])
            print("Collection Date:", collection["collection_date"])
            print("Status:", collection["status"])
            return
    print("Collection not found!")           
def update_collection():
    print("\n  ⬜ Update Waste Collection  ")
    collection_id = input("Enter Collection ID to update: ")
    for collection in collections:
        if collection["id"] == collection_id:
            waste_type = input("Enter new Waste Type: ")
            quantity = input("Enter new Quantity (kg): ")
            city_id = input("Enter new City ID: ")
            area_id = input("Enter new Area ID: ")
            provider_id = input("Enter new Service Provider ID: ")
            collection_date = input("Enter new Collection Date: ")
            status = input("Enter new Collection Status: ")
            if waste_type:
                collection["waste_type"] = waste_type
            if quantity:
                collection["quantity"] = quantity
            if city_id:
                collection["city_id"] = city_id
            if area_id:
                collection["area_id"] = area_id
            if provider_id:
                collection["provider_id"] = provider_id
            if collection_date:
                collection["collection_date"] = collection_date
            if status:
                collection["status"] = status
            print("Collection updated successfully!")
            return
    print("Collection not found!")     
def delete_collection():
    print("\n ⬜  Delete Waste Collection  ")
    collection_id = input("Enter Collection ID to delete: ")
    for collection in collections:
        if collection["id"] == collection_id:
            confirm = input("Are you sure you want to delete it? (yes/no): ")
            if confirm.lower() == "yes":
                collections.remove(collection)
                print("Collection deleted successfully!")
            else:
                print("Deletion cancelled.")
            return
    print("Collection not found!")  

providers = []
def add_provider():
    print("\n  ADD SERVICE PROVIDER  ")
    provider_id = input("Enter Provider ID: ")
    for provider in providers:
        if provider["id"] == provider_id:
            print("Error: Provider ID already exists!")
            return
    name = input("Enter Provider Name: ")
    service_type = input("Enter Service Type: ")
    city_id = input("Enter City ID: ")
    provider = {
        "id": provider_id,
        "name": name,
        "service_type": service_type,
        "city_id": city_id
    }
    providers.append(provider)
    print("\nService Provider added successfully!")
def view_providers():
    print("\n  REGISTERED SERVICE PROVIDERS  ")
    if not providers:
        print("No service providers registered yet.")
        return
    for provider in providers:
        print("Provider ID:", provider["id"])
        print("Provider Name:", provider["name"])
        print("Service Type:", provider["service_type"])
        print("City ID:", provider["city_id"])
def search_provider():
    print("\n  SEARCH SERVICE PROVIDER  ")
    provider_id = input("Enter Provider ID to search: ")
    for provider in providers:
        if provider["id"] == provider_id:
            print("\nService Provider Found!")
            print("Provider ID:", provider["id"])
            print("Provider Name:", provider["name"])
            print("Service Type:", provider["service_type"])
            print("City ID:", provider["city_id"])
            return
    print("Service Provider not found!")
def update_provider():
    print("\n  UPDATE SERVICE PROVIDER  ")
    provider_id = input("Enter Provider ID to update: ")
    for provider in providers:
        if provider["id"] == provider_id:
            name = input("Enter new Provider Name: ")
            service_type = input("Enter new Service Type: ")
            city_id = input("Enter new City ID: ")
            if name:
                provider["name"] = name
            if service_type:
                provider["service_type"] = service_type
            if city_id:
                provider["city_id"] = city_id
            print("\nService Provider updated successfully!")
            return
    print("Service Provider not found!")
def delete_provider():
    print("\n  DELETE SERVICE PROVIDER  ")
    provider_id = input("Enter Provider ID to delete: ")
    for provider in providers:
        if provider["id"] == provider_id:
            confirm = input( f"Delete service provider {provider['name']}? (yes/no): " ).lower()
            if confirm == "yes":
                providers.remove(provider)
                print("\nService Provider deleted successfully!")
            else:
                print("Deletion cancelled.")
            return
    print("Service Provider not found!")
schedules = []
def add_schedule():
    print("\n ⬜  Add Waste Collection Schedule ")
    schedule_id = f"SCH{len(schedules) + 1:03d}"
    collection_id = input("Enter Collection ID: ")
    date = input("Enter Schedule Date (DD/MM/YYYY): ")
    time = input("Enter Schedule Time: ")
    provider_id = input("Enter Service Provider ID: ")
    schedule = {
        "id": schedule_id,
        "collection_id": collection_id,
        "date": date,
        "time": time,
        "provider_id": provider_id,
        "status": "Scheduled"
    }
    schedules.append(schedule)
    print("\nSchedule added successfully!")
    print("Generated Schedule ID:", schedule_id)
def view_schedules():
    print("\n ⬜  All Schedules  ")
    if not schedules:
        print("No schedules available.")
        return
    for schedule in schedules:
        print("\nSchedule ID:", schedule["id"])
        print("Collection ID:", schedule["collection_id"])
        print("Date:", schedule["date"])
        print("Time:", schedule["time"])
        print("Service Provider ID:", schedule["provider_id"])
        print("Status:", schedule["status"])
def search_schedule():
    print("\n ⬜  Search Schedule  ")
    schedule_id = input("Enter Schedule ID: ")
    for schedule in schedules:
        if schedule["id"] == schedule_id:
            print("\nSchedule Found!")
            print("Schedule ID:", schedule["id"])
            print("Collection ID:", schedule["collection_id"])
            print("Date:", schedule["date"])
            print("Time:", schedule["time"])
            print("Service Provider ID:", schedule["provider_id"])
            print("Status:", schedule["status"])
            return
    print("Schedule not found!")
def update_schedule():
    print("\n ⬜ Update Schedule    ")
    schedule_id = input("Enter Schedule ID to update: ")
    for schedule in schedules:
        if schedule["id"] == schedule_id:
            date = input("Enter new date: ")
            time = input("Enter new time: ")
            provider_id = input("Enter new Service Provider ID: ")
            status = input("Enter new status: ")
            if date:
                schedule["date"] = date
            if time:
                schedule["time"] = time
            if provider_id:
                schedule["provider_id"] = provider_id
            if status:
                schedule["status"] = status
            print("Schedule updated successfully!")
            return
    print("Schedule not found!")
def delete_schedule():
    print("\n ⬜   Delete Schedule   ")
    schedule_id = input("Enter Schedule ID to delete: ")
    for schedule in schedules:
        if schedule["id"] == schedule_id:
            confirm = input( "Are you sure you want to delete this schedule? (yes/no): ")
            if confirm.lower() == "yes":
                schedules.remove(schedule)
                print("Schedule deleted successfully!")
            else:
                print("Deletion cancelled.")
            return
    print("Schedule not found!")

requests = []
def add_request():
    print("\n ⬜  Submit Waste Collection Request ")
    request_id = f"REQ{len(requests) + 1:03d}"
    user_id = input("Enter User ID: ")
    waste_type = input("Enter Waste Type: ")
    quantity = input("Enter Waste Quantity (kg): ")
    city_id = input("Enter City ID: ")
    area_id = input("Enter Area ID: ")
    preferred_date = input("Enter Preferred Collection Date (DD/MM/YYYY): ")
    request = {
        "id": request_id,
        "user_id": user_id,
        "waste_type": waste_type,
        "quantity": quantity,
        "city_id": city_id,
        "area_id": area_id,
        "preferred_date": preferred_date,
        "status": "Pending"
    }
    requests.append(request)
    print("\nRequest submitted successfully!")
    print("Generated Request ID:", request_id)
    print("Request Status: Pending")
def view_requests():
    print("\n ⬜   All Waste Collection Requests   ")
    if not requests:
        print("No requests available.")
        return
    for request in requests:
        print("\nRequest ID:", request["id"])
        print("User ID:", request["user_id"])
        print("Waste Type:", request["waste_type"])
        print("Quantity:", request["quantity"], "kg")
        print("City ID:", request["city_id"])
        print("Area ID:", request["area_id"])
        print("Preferred Date:", request["preferred_date"])
        print("Status:", request["status"])
def search_request():
    print("\n ⬜  Search Request   ")
    request_id = input("Enter Request ID: ")
    for request in requests:
        if request["id"] == request_id:
            print("\nRequest Found!")
            print("Request ID:", request["id"])
            print("User ID:", request["user_id"])
            print("Waste Type:", request["waste_type"])
            print("Quantity:", request["quantity"], "kg")
            print("City ID:", request["city_id"])
            print("Area ID:", request["area_id"])
            print("Preferred Date:", request["preferred_date"])
            print("Status:", request["status"])
            return
    print("Request not found!")
def update_request():
    print("\n ⬜  Update Request   ")
    request_id = input("Enter Request ID to update: ")
    for request in requests:
        if request["id"] == request_id:
            quantity = input("Enter new quantity: ")
            preferred_date = input("Enter new preferred date: ")
            status = input("Enter status (Pending/Approved/Rejected/Completed): ")
            if quantity:
                request["quantity"] = quantity
            if preferred_date:
                request["preferred_date"] = preferred_date
            if status:
                request["status"] = status
            print("Request updated successfully!")
            return
    print("Request not found!")
def delete_request():
    print("\n  ⬜ Delete Request ")
    request_id = input("Enter Request ID to delete: ")
    for request in requests:
        if request["id"] == request_id:
            confirm = input( "Are you sure you want to delete this request? (yes/no): ")
            if confirm.lower() == "yes":
                requests.remove(request)
                print("Request deleted successfully!")
            else:
                print("Deletion cancelled.")
            return
    print("Request not found!")

bills = []
def generate_bill():
    print("\n ⬜   Generate Bill  ")
    bill_id = f"BILL{len(bills) + 1:03d}"
    user_id = input("Enter User ID: ")
    collection_id = input("Enter Collection ID: ")
    try:
        quantity = float(input("Enter Waste Quantity (kg): "))
        rate = float(input("Enter Rate per kg (₹): "))
        if quantity <= 0 or rate < 0:
            print("Quantity must be greater than 0 and rate cannot be negative.")
            return
    except ValueError:
        print("Please enter a valid number for quantity and rate.")
        return
    total_amount = quantity * rate
    bill = {
        "id": bill_id,
        "user_id": user_id,
        "collection_id": collection_id,
        "quantity": quantity,
        "rate": rate,
        "total_amount": total_amount,
        "payment_status": "Unpaid"
    }
    bills.append(bill)
    print("\nBill generated successfully!")
    print("Bill ID:", bill_id)
    print("Total Amount: ₹", format(total_amount, ".2f"))
    print("Payment Status: Unpaid")
def view_bills():
    print("\n  ⬜  All Bills  ")
    if not bills:
        print("No bills available.")
        return
    for bill in bills:
        print("\n  BinGO BILL   ")
        print("Bill ID:", bill["id"])
        print("User ID:", bill["user_id"])
        print("Collection ID:", bill["collection_id"])
        print("Waste Quantity:", bill["quantity"], "kg")
        print("Rate per kg: ₹", format(bill["rate"], ".2f"))
        print("Total Amount: ₹", format(bill["total_amount"], ".2f"))
        print("Payment Status:", bill["payment_status"])
def search_bill():
    print("\n ⬜  Search Bill  ")
    bill_id = input("Enter Bill ID: ")
    for bill in bills:
        if bill["id"] == bill_id:
            print("\nBill Found!")
            print("Bill ID:", bill["id"])
            print("User ID:", bill["user_id"])
            print("Collection ID:", bill["collection_id"])
            print("Waste Quantity:", bill["quantity"], "kg")
            print("Rate per kg: ₹", format(bill["rate"], ".2f"))
            print("Total Amount: ₹", format(bill["total_amount"], ".2f"))
            print("Payment Status:", bill["payment_status"])
            return
    print("Bill not found!")
def update_bill():
    print("\n ⬜  Update Bill   ")
    bill_id = input("Enter Bill ID to update: ")
    for bill in bills:
        if bill["id"] == bill_id:
            status = input("Enter Payment Status (Paid/Unpaid): ")
            if status:
                if status.lower() == "paid":
                    bill["payment_status"] = "Paid"
                elif status.lower() == "unpaid":
                    bill["payment_status"] = "Unpaid"
                else:
                    print("Invalid payment status.")
                    return
            print("Bill updated successfully!")
            return
    print("Bill not found!")
def delete_bill():
    print("\n ⬜  Delete Bill  ")
    bill_id = input("Enter Bill ID to delete: ")
    for bill in bills:
        if bill["id"] == bill_id:
            confirm = input(
                "Are you sure you want to delete this bill? (yes/no): "
            )
            if confirm.lower() == "yes":
                bills.remove(bill)
                print("Bill deleted successfully!")
            else:
                print("Deletion cancelled.")
            return
    print("Bill not found!")  
