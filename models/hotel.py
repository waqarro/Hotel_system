from datetime import date
from .room    import StandardRoom, DeluxeRoom, SuiteRoom
from .guest   import Guest
from .booking import Booking
import json
import os


class Hotel:
    """
    Central class that manages all hotel operations.
    Demonstrates object interaction between Room, Guest, and Booking.
    """

    def __init__(self, name):
        # Private attributes - Encapsulation
        self.__name     = name
        self.__rooms    = []
        self.__guests   = []
        self.__bookings = []

        self._create_rooms()    # seed rooms on startup
        self.load_data()        # load persisted state

    def _create_rooms(self):
        """Create default rooms for the hotel (5 floors)."""
        for floor in range(1, 6):
            self.__rooms.append(StandardRoom(floor))
            self.__rooms.append(StandardRoom(floor))
            self.__rooms.append(DeluxeRoom(floor))
            if floor >= 3:
                self.__rooms.append(SuiteRoom(floor))

    #  Getters 
    def get_name(self):
        return self.__name

    def get_all_rooms(self):
        return list(self.__rooms)

    def get_available_rooms(self, room_type=None):
        rooms = [r for r in self.__rooms if not r.is_booked()]
        if room_type:
            rooms = [r for r in rooms if r.get_room_type() == room_type]
        return rooms

    def get_all_guests(self):
        return list(self.__guests)

    def get_all_bookings(self):
        return list(self.__bookings)

    def find_booking(self, booking_id):
        for b in self.__bookings:
            if b.get_booking_id() == booking_id:
                return b
        return None

    def find_guest(self, guest_id):
        for g in self.__guests:
            if g.get_guest_id() == guest_id:
                return g
        return None

    def find_room(self, room_number):
        for r in self.__rooms:
            if r.get_room_number() == room_number:
                return r
        return None

    #  Hotel operations (Object Interaction) 
    def register_guest(self, name, ic, phone, email=""):
        guest = Guest(name, ic, phone, email)
        self.__guests.append(guest)
        self.save_data()
        return guest

    def make_booking(self, guest, room_number, check_in, nights):
        room = self.find_room(room_number)
        if not room:
            raise ValueError(f"Room {room_number} does not exist.")
        booking = Booking(guest, room, check_in, nights)
        self.__bookings.append(booking)
        self.save_data()
        return booking

    def check_in(self, booking_id):
        booking = self.find_booking(booking_id)
        if not booking:
            raise ValueError(f"Booking {booking_id} not found.")
        booking.do_check_in()
        self.save_data()
        return booking

    def check_out(self, booking_id):
        booking = self.find_booking(booking_id)
        if not booking:
            raise ValueError(f"Booking {booking_id} not found.")
        booking.do_check_out()
        self.save_data()
        return booking

    def cancel_booking(self, booking_id):
        booking = self.find_booking(booking_id)
        if not booking:
            raise ValueError(f"Booking {booking_id} not found.")
        booking.do_cancel()
        self.save_data()
        return booking

    def get_stats(self):
        total   = len(self.__rooms)
        booked  = sum(1 for r in self.__rooms if r.is_booked())
        revenue = sum(
            b.get_total_price() for b in self.__bookings
            if b.get_status() != "Cancelled"
        )
        return {
            "total_rooms"     : total,
            "booked_rooms"    : booked,
            "available_rooms" : total - booked,
            "total_guests"    : len(self.__guests),
            "total_bookings"  : len(self.__bookings),
            "total_revenue"   : round(revenue, 2),
        }

    #  File I/O Persistence 
    def save_data(self):
        os.makedirs("data", exist_ok=True)
        with open("data/guests.json", "w") as f:
            json.dump([g.to_dict() for g in self.__guests], f, indent=4)
        with open("data/bookings.json", "w") as f:
            json.dump([b.to_dict() for b in self.__bookings], f, indent=4)

    def load_data(self):
        try:
            if os.path.exists("data/guests.json"):
                with open("data/guests.json", "r") as f:
                    self.__guests = [Guest.from_dict(d) for d in json.load(f)]
            
            if os.path.exists("data/bookings.json"):
                with open("data/bookings.json", "r") as f:
                    for d in json.load(f):
                        guest = self.find_guest(d["guest_id"])
                        room = self.find_room(d["room_number"])
                        if guest and room:
                            b = Booking.from_dict(d, guest, room)
                            self.__bookings.append(b)
                            guest.add_booking(b)
                            if b.get_status() in [Booking.CONFIRMED, Booking.CHECKED_IN]:
                                room.set_booked(True)
        except Exception as e:
            print(f"Warning: Could not fully load save data. Error: {e}")

    def __str__(self):
        return f"Hotel: {self.__name}"
