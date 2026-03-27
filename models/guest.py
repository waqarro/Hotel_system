"""
models/guest.py
Hotel Room Booking System - SEGi University Final Assessment

OOP Principles used in this file:
- Encapsulation : All attributes are private with getters and setters
- Polymorphism  : __str__ overrides default object string representation
"""


class Guest:
    """
    Represents a hotel guest.
    Uses encapsulation to protect personal data.
    """

    _id_counter = 1000  # class variable for auto ID generation

    def __init__(self, name, ic_number, phone, email=""):
        Guest._id_counter += 1

        # Private attributes - Encapsulation
        self.__guest_id  = f"G{Guest._id_counter}"
        self.__name      = name.strip().title()
        self.__ic_number = ic_number.strip()
        self.__phone     = phone.strip()
        self.__email     = email.strip()
        self.__bookings  = []   # private list of bookings

    # --- Getters ---
    def get_guest_id(self):
        return self.__guest_id

    def get_name(self):
        return self.__name

    def get_ic_number(self):
        # Mask IC number for privacy - only show last 4 digits
        if len(self.__ic_number) > 4:
            return "*" * (len(self.__ic_number) - 4) + self.__ic_number[-4:]
        return self.__ic_number

    def get_ic_full(self):
        return self.__ic_number

    def get_phone(self):
        return self.__phone

    def get_email(self):
        return self.__email

    def get_bookings(self):
        return list(self.__bookings)    # return copy to protect private list

    # --- Setters with validation ---
    def set_name(self, name):
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        self.__name = name.strip().title()

    def set_phone(self, phone):
        if not phone.strip():
            raise ValueError("Phone number cannot be empty.")
        self.__phone = phone.strip()

    def set_email(self, email):
        if email and "@" not in email:
            raise ValueError("Invalid email format.")
        self.__email = email.strip()

    # --- Methods for managing bookings ---
    def add_booking(self, booking):
        self.__bookings.append(booking)

    def remove_booking(self, booking_id):
        for b in self.__bookings:
            if b.get_booking_id() == booking_id:
                self.__bookings.remove(b)
                return True
        return False

    # --- Serialization ---
    def to_dict(self):
        return {
            "guest_id": self.__guest_id,
            "name": self.__name,
            "ic_number": self.get_ic_full(),
            "phone": self.__phone,
            "email": self.__email
        }
        
    @classmethod
    def from_dict(cls, data):
        g = cls(data["name"], data["ic_number"], data["phone"], data.get("email", ""))
        g._Guest__guest_id = data["guest_id"]
        
        # Advance the class counter safely
        id_num = int(data["guest_id"].replace("G", ""))
        if id_num > cls._id_counter:
            cls._id_counter = id_num
            
        return g

    # --- Polymorphism: overrides default __str__ ---
    def __str__(self):
        return (f"[{self.__guest_id}] {self.__name} | "
                f"IC: {self.get_ic_number()} | Phone: {self.__phone}")
