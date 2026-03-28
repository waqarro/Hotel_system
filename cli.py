from datetime import datetime

class HotelCLI:
    def __init__(self):
        import os, json
        from models.hotel import Hotel
        
        os.makedirs("data", exist_ok=True)
        if not os.path.exists("data/auth.json"):
            
            print("\n=== First-Time System Setup ===")
            username = input("Enter New Admin Username: ")
            password = input("Enter New Admin Password: ")
            hotel_name = input("Enter Your Hotel Name: ")
            
            with open("data/auth.json", "w") as f:
                json.dump({"username": username, "password": password, "hotel_name": hotel_name}, f)
            
            self.current_user = username
            self.hotel_name = hotel_name
            print(f"\nSetup Complete! Welcome to {hotel_name}")
            import time; time.sleep(1)
        else:
            with open("data/auth.json", "r") as f:
                data = json.load(f)
            
            self.hotel_name = data["hotel_name"]
            print(f"\nWelcome back to {self.hotel_name}, {data['username']}!")
            
            while True:
                pwd = input("Enter Password: ")
                if pwd == data["password"]:
                    self.current_user = data["username"]
                    break
                else:
                    print("Incorrect password. Try again.")
                    
        self.hotel = Hotel(self.hotel_name)

    def run(self):
        while True:
            print("\n" + "="*40)
            print(f"  {self.hotel.get_name()} Booking System")
            print("="*40)
            print(" [1] Dashboard")
            print(" [2] View All Rooms")
            print(" [3] Register Guest")
            print(" [4] View All Guests")
            print(" [5] Make New Booking")
            print(" [6] Manage Bookings")
            print(" [L] Logout")
            print(" [0] Exit")
            print("-" * 40)
            
            choice = input("Enter your choice (1): ") or "1"
            
            if choice == '1':
                self.show_dashboard()
            elif choice == '2':
                self.show_rooms()
            elif choice == '3':
                self.register_guest()
            elif choice == '4':
                self.show_guests()
            elif choice == '5':
                self.new_booking()
            elif choice == '6':
                self.manage_bookings()
            elif choice.upper() == 'L':
                print("Logging out...")
                import time; time.sleep(1)
                self.__init__() 
                continue
            elif choice == '0':
                print("\nThank you for using the Hotel Booking System. Goodbye!\n")
                break
            
            if choice != '0':
                input("\nPress Enter to return to the main menu...")

    def show_dashboard(self):
        stats = self.hotel.get_stats()
        print("\n--- Hotel Dashboard ---")
        print(f"Total Rooms     : {stats['total_rooms']}")
        print(f"Available Rooms : {stats['available_rooms']}")
        print(f"Booked Rooms    : {stats['booked_rooms']}")
        print(f"Total Guests    : {stats['total_guests']}")
        print(f"Total Bookings  : {stats['total_bookings']}")
        print(f"Total Revenue   : RM {stats['total_revenue']:,.2f}")
        print("-" * 23)

    def show_rooms(self):
        rooms = self.hotel.get_all_rooms()
        print("\n--- All Hotel Rooms ---")
        print(f"{'No':<6} {'Type':<12} {'Floor':<6} {'Cap':<6} {'Price':<12} {'Status'}")
        print("-" * 60)
        for r in rooms:
            status = "Booked" if r.is_booked() else "Available"
            print(f"{str(r.get_room_number()):<6} {r.get_room_type():<12} "
                  f"{str(r.get_floor()):<6} {str(r.get_capacity()):<6} "
                  f"RM {r.get_price_per_night():<9.2f} {status}")

    def register_guest(self):
        print("\n--- Register a New Guest ---")
        name = input("Full Name: ")
        ic = input("IC/Passport Number: ")
        phone = input("Phone Number: ")
        email = input("Email (optional): ")

        if not name or not ic or not phone:
            print("Error: Name, IC, and Phone are strongly required.")
            return

        try:
            guest = self.hotel.register_guest(name, ic, phone, email)
            print(f"\nSuccess! Guest registered with ID: {guest.get_guest_id()}")
        except Exception as e:
            print(f"\nError: {e}")

    def show_guests(self):
        guests = self.hotel.get_all_guests()
        if not guests:
            print("\nNo guests registered yet.")
            return
            
        print("\n--- Registered Guests ---")
        print(f"{'ID':<10} {'Name':<20} {'IC/Passport':<15} {'Phone'}")
        print("-" * 60)
        for g in guests:
            print(f"{g.get_guest_id():<10} {g.get_name()[:19]:<20} "
                  f"{g.get_ic_number():<15} {g.get_phone()}")

    def new_booking(self):
        print("\n--- Make a New Booking ---")
        avail_rooms = self.hotel.get_available_rooms()
        if not avail_rooms:
            print("Sorry, no rooms are currently available.")
            return
            
        room_list = ", ".join([str(r.get_room_number()) for r in avail_rooms])
        print(f"Available Rooms: {room_list}\n")
        
        guest_id = input("Enter Guest ID: ").upper()
        guest = self.hotel.find_guest(guest_id)
        if not guest:
            print("Error: Guest not found. Please register the guest first.")
            return

        try:
            room_num = int(input("Enter Room Number: "))
            checkin_str = input("Check-In Date (DD/MM/YYYY) (Leave blank for today): ")
            
            if not checkin_str:
                checkin = datetime.today().date()
            else:
                checkin = datetime.strptime(checkin_str, "%d/%m/%Y").date()
            
            nights = int(input("Number of Nights: "))
        except ValueError:
            print("Error: Invalid input format. Please check your numbers and dates.")
            return

        try:
            booking = self.hotel.make_booking(guest, room_num, checkin, nights)
            print(f"\nBooking Confirmed!")
            print(f"Booking ID  : {booking.get_booking_id()}")
            print(f"Total Price : RM {booking.get_total_price():.2f}")
            
            import os
            os.makedirs("Receipts", exist_ok=True)
            path = f"Receipts/{booking.get_booking_id()}_receipt.txt"
            with open(path, "w") as f:
                f.write(booking.get_receipt_text())
            print(f"Receipt saved to: {path}")
            
        except Exception as e:
            print(f"\nError: {e}")

    def manage_bookings(self):
        bookings = self.hotel.get_all_bookings()
        if not bookings:
            print("\nNo bookings exist yet.")
            return
            
        print("\n--- Manage Bookings ---")
        print(f"{'ID':<10} {'Guest':<15} {'Room':<6} {'In':<12} {'Out':<12} {'Status'}")
        print("-" * 65)
        for b in bookings:
            print(f"{b.get_booking_id():<10} {b.get_guest().get_name()[:14]:<15} "
                  f"{str(b.get_room().get_room_number()):<6} "
                  f"{b.get_check_in().strftime('%d/%m/%Y'):<12} "
                  f"{b.get_check_out().strftime('%d/%m/%Y'):<12} "
                  f"{b.get_status()}")
            
        print("\nActions: [1] Check-In [2] Check-Out [3] Cancel [4] View Receipt [0] Back")
        action = input("Select an action (0): ") or "0"
        if action == '0':
            return
            
        bid = input("Enter Booking ID: ").upper()
        
        try:
            if action == '1':
                self.hotel.check_in(bid)
                print(f"Successfully checked in booking {bid}!")
            elif action == '2':
                self.hotel.check_out(bid)
                print(f"Successfully checked out booking {bid}!")
            elif action == '3':
                confirm = input("Are you sure you want to cancel? (y/n): ")
                if confirm.lower() == 'y':
                    self.hotel.cancel_booking(bid)
                    print(f"Booking {bid} cancelled.")
            elif action == '4':
                b = self.hotel.find_booking(bid)
                if b:
                    print("\n--- Receipt ---")
                    print(b.get_receipt_text())
                    
                    import os
                    os.makedirs("Receipts", exist_ok=True)
                    path = f"Receipts/{b.get_booking_id()}_receipt.txt"
                    with open(path, "w") as f:
                        f.write(b.get_receipt_text())
                    print(f"Receipt downloaded to: {path}")
                else:
                    print("Error: Booking not found.")
        except Exception as e:
            print(f"Error: {e}")
