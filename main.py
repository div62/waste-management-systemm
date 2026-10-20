from function import (add_user, view_users, search_user, update_user, delete_user,add_waste,
    view_waste,search_waste,update_waste,delete_waste,add_city, view_cities,search_cities,update_city, delete_city ,add_collection,view_collections,search_collection,update_collection,delete_collection, add_schedule, view_schedules, search_schedule,
    update_schedule, delete_schedule,add_request, view_requests, search_request,update_request, delete_request, generate_bill, view_bills, search_bill, update_bill, delete_bill)
print("      ♻️  BinGO",       "\nSmart Waste Management System")
while True:
    print("\n1.  🚹 User Management")
    print("2.  🗑️  Waste Management")
    print("3.  🏢 City Management")
    print("4.  👥 Collection Management")
    print("5.  🕑 Scheduling")
    print("6.  🗳️  Request Management")
    print("7.  🧾 Billing")
    print("8.  🔶 Dashboard & Analytics")
    print("9.  ➡️  Exit")
    choice = input("\nEnter your choice (1-9): ")
    if choice == "1":
       while True:
        print("\n 🚹  User Management ")
        print("1. Add User")
        print("2. View Users")
        print("3. Search User")
        print("4. Update User")
        print("5. Delete User")
        print("6. Back to Main Menu")
        user_choice = input("Enter your choice: ")
        if user_choice == "1":
            add_user()
        elif user_choice == "2":
            view_users()
        elif user_choice == "3":
            search_user()
        elif user_choice == "4":
            update_user()
        elif user_choice == "5":
            delete_user()
        elif user_choice == "6":
            break
        else:
            print("Invalid choice! Try again.")
    elif choice == "2":
        while True:
            print("\n  🗑️  Waste Management ")
            print("1. Add Waste Type")
            print("2. View Waste Types")
            print("3. Search Waste Type")
            print("4. Update Waste Type")
            print("5. Delete Waste Type")
            print("6. Back to Main Menu")
            waste_choice = input("Enter your choice: ")
            if waste_choice == "1":
               add_waste()
            elif waste_choice == "2":
                view_waste()
            elif waste_choice == "3":
                search_waste()
            elif waste_choice == "4":
                update_waste() 
            elif  waste_choice == "5":
                delete_waste()     
            elif waste_choice == "6":
                break
            else:
               print("Invalid choice! Please try again.")
    elif choice == "3":
        while True:
            print("\n 🏢  City Management ")
            print("1. Add City")
            print("2. View Cities")
            print("3. Search City")
            print("4. update city")
            print("5. Delete City")
            print("6. Back to Main Menu")
            city_choice = input("Enter your choice: ")
            if city_choice == "1":
               add_city()
            elif city_choice == "2":
               view_cities()
            elif city_choice == "3":
               search_cities()
            elif city_choice == "4":
                update_city()
            elif city_choice == "5":
                delete_city()
            elif city_choice == "6":
                break
            else:
                print("Invalid choice! Please try again.")
    elif choice == "4":
        while True:
            print("\n 👥  Collection Management  ")
            print("1. Add Collection")
            print("2. View Collections")
            print("3. Search Collection")
            print("4. Update Collection")
            print("5. Delete Collection")
            print("6. Back to Main Menu")
            collection_choice = input("Enter your choice: ")
            if collection_choice == "1":
                add_collection()
            elif collection_choice == "2":
                view_collections()
            elif collection_choice == "3":
                search_collection()
            elif collection_choice == "4":
                update_collection()
            elif collection_choice == "5":
                delete_collection()
            elif collection_choice == "6":
                break
            else:
                print("Invalid choice! Please try again.")
    elif choice == "5":
        while True:
            print("\n  🕑  Scheduling Management  ")
            print("1. Add Schedule")
            print("2. View Schedules")
            print("3. Search Schedule")
            print("4. Update Schedule")
            print("5. Delete Schedule")
            print("6. Back to Main Menu")
            schedule_choice = input("Enter your choice: ")
            if schedule_choice == "1":
                add_schedule()
            elif schedule_choice == "2":
                view_schedules()
            elif schedule_choice == "3":
                search_schedule()
            elif schedule_choice == "4":
                update_schedule()
            elif schedule_choice == "5":
                delete_schedule()
            elif schedule_choice == "6":
                break
            else:
                print("Invalid choice! Please try again.")
    elif choice == "6":
        while True:
            print("\n  🗳️  Request Management ")
            print("1. Submit Request")
            print("2. View Requests")
            print("3. Search Request")
            print("4. Update Request")
            print("5. Delete Request")
            print("6. Back to Main Menu")
            request_choice = input("Enter your choice: ")

            if request_choice == "1":
                add_request()
            elif request_choice == "2":
                view_requests()
            elif request_choice == "3":
                search_request()
            elif request_choice == "4":
                update_request()
            elif request_choice == "5":
                delete_request()
            elif request_choice == "6":
                break
            else:
                print("Invalid choice! Please try again.")
    elif choice == "7":
        while True:
            print("\n 🧾  Billing Management ")
            print("1. Generate Bill")
            print("2. View Bills")
            print("3. Search Bill")
            print("4. Update Bill")
            print("5. Delete Bill")
            print("6. Back to Main Menu")
            billing_choice = input("Enter your choice: ")
            if billing_choice == "1":
                generate_bill()
            elif billing_choice == "2":
                view_bills()
            elif billing_choice == "3":
                search_bill()
            elif billing_choice == "4":
                update_bill()
            elif billing_choice == "5":
                delete_bill()
            elif billing_choice == "6":
                break
            else:
                print("Invalid choice! Please try again.")
    elif choice == "8":
        print("🔶  Dashboard & Analytics selected")
    elif choice == "9":
        print("\nThank you for using BinGO! ♻️")
        break
    else:
        print("Invalid choice! Please enter a number from 1 to 9.")