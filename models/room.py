"""
models/room.py
Hotel Room Booking System - SEGi University Final Assessment

OOP Principles used in this file:
- Abstraction    : Room is an abstract base class (cannot be created directly)
- Encapsulation  : Private attributes (__room_number, __price) with getters/setters
- Inheritance    : StandardRoom, DeluxeRoom, SuiteRoom all extend Room
- Polymorphism   : get_description() and calculate_price() behave differently per subclass
"""

from abc import ABC, abstractmethod
from datetime import datetime


# -------------------------------------------------------
# Abstract Base Class  (Abstraction + Encapsulation)
# -------------------------------------------------------
class Room(ABC):
    """
    Abstract class representing a hotel room.
    Cannot be instantiated directly - must use a subclass.
    """

    _id_counter = 100   # class variable to auto-number rooms

    def __init__(self, room_type, floor, capacity, price_per_night):
        Room._id_counter += 1

        # Private attributes - Encapsulation
        self.__room_number     = Room._id_counter
        self.__price_per_night = price_per_night

        # Protected attributes (accessible to child classes)
        self._room_type = room_type
        self._floor     = floor
        self._capacity  = capacity
        self._is_booked = False

    # --- Getters (Encapsulation) ---
    def get_room_number(self):
        return self.__room_number

    def get_price_per_night(self):
        return self.__price_per_night

    def get_room_type(self):
        return self._room_type

    def get_floor(self):
        return self._floor

    def get_capacity(self):
        return self._capacity

    def is_booked(self):
        return self._is_booked

    # --- Setters with validation (Encapsulation) ---
    def set_price_per_night(self, price):
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        self.__price_per_night = price

    def set_booked(self, status):
        self._is_booked = status

    # --- Abstract methods (must be overridden by child classes) ---
    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def calculate_price(self, nights):
        pass

    def __str__(self):
        status = "Booked" if self._is_booked else "Available"
        return (f"Room {self.__room_number} | {self._room_type} | "
                f"Floor {self._floor} | RM{self.__price_per_night:.2f}/night | {status}")


# -------------------------------------------------------
# StandardRoom  (Inheritance + Polymorphism)
# -------------------------------------------------------
class StandardRoom(Room):
    """
    Basic room. Inherits from Room.
    Overrides get_description() and calculate_price() - Polymorphism.
    """

    def __init__(self, floor):
        super().__init__(
            room_type="Standard",
            floor=floor,
            capacity=2,
            price_per_night=150.00
        )

    def get_description(self):
        # Polymorphism: different description from other room types
        return "Cozy room for 2. Includes TV, Wi-Fi, and air-conditioning."

    def calculate_price(self, nights):
        # Polymorphism: standard flat rate
        return self.get_price_per_night() * nights


# -------------------------------------------------------
# DeluxeRoom  (Inheritance + Polymorphism)
# -------------------------------------------------------
class DeluxeRoom(Room):
    """
    Upgraded room with a 10% weekend surcharge.
    Inherits from Room. Overrides calculate_price() - Polymorphism.
    """

    WEEKEND_SURCHARGE = 0.10

    def __init__(self, floor):
        super().__init__(
            room_type="Deluxe",
            floor=floor,
            capacity=3,
            price_per_night=280.00
        )

    def get_description(self):
        # Polymorphism: different description
        return "Spacious room for 3. Includes smart TV, mini-bar, balcony, and Wi-Fi. Weekend +10%."

    def calculate_price(self, nights):
        # Polymorphism: adds weekend surcharge for Fri/Sat nights
        base  = self.get_price_per_night()
        today = datetime.today()
        total = 0.0
        for i in range(nights):
            day = (today.weekday() + i) % 7
            if day in (4, 5):   # 4=Friday, 5=Saturday
                total += base * (1 + self.WEEKEND_SURCHARGE)
            else:
                total += base
        return round(total, 2)


# -------------------------------------------------------
# SuiteRoom  (Inheritance + Polymorphism)
# -------------------------------------------------------
class SuiteRoom(Room):
    """
    Luxury suite with 15% discount for 5+ nights.
    Inherits from Room. Overrides calculate_price() - Polymorphism.
    """

    LOYALTY_DISCOUNT = 0.15

    def __init__(self, floor):
        super().__init__(
            room_type="Suite",
            floor=floor,
            capacity=4,
            price_per_night=550.00
        )

    def get_description(self):
        # Polymorphism: different description
        return "Luxury suite for 4. Private pool, butler service, panoramic view. 15% off for 5+ nights."

    def calculate_price(self, nights):
        # Polymorphism: loyalty discount for long stays
        total = self.get_price_per_night() * nights
        if nights >= 5:
            total *= (1 - self.LOYALTY_DISCOUNT)
        return round(total, 2)
