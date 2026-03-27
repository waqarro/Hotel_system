"""
models/booking.py
Hotel Room Booking System - SEGi University Final Assessment

OOP Principles used in this file:
- Encapsulation     : Private attributes with getters
- Object Interaction: Booking connects Guest and Room objects together
"""

from datetime import date, timedelta, datetime


class Booking:
    """
    Represents a room booking.
    Demonstrates object interaction - links a Guest to a Room.
    """

    _id_counter = 5000

    # Status constants
    CONFIRMED   = "Confirmed"
    CHECKED_IN  = "Checked In"
    CHECKED_OUT = "Checked Out"
    CANCELLED   = "Cancelled"

    def __init__(self, guest, room, check_in_date, nights):
        if room.is_booked():
            raise ValueError(f"Room {room.get_room_number()} is already booked.")
        if nights < 1:
            raise ValueError("Must book for at least 1 night.")

        Booking._id_counter += 1

        # Private attributes - Encapsulation
        self.__booking_id   = f"BK{Booking._id_counter}"
        self.__guest        = guest                          # Object Interaction
        self.__room         = room                          # Object Interaction
        self.__check_in     = check_in_date
        self.__nights       = nights
        self.__check_out    = check_in_date + timedelta(days=nights)
        self.__total_price  = room.calculate_price(nights)  # Polymorphism called here
        self.__status       = self.CONFIRMED
        self.__created_at   = datetime.now()

        # Object Interaction: update the room and guest
        room.set_booked(True)
        guest.add_booking(self)

    # --- Getters ---
    def get_booking_id(self):
        return self.__booking_id

    def get_guest(self):
        return self.__guest

    def get_room(self):
        return self.__room

    def get_check_in(self):
        return self.__check_in

    def get_check_out(self):
        return self.__check_out

    def get_nights(self):
        return self.__nights

    def get_total_price(self):
        return self.__total_price

    def get_status(self):
        return self.__status

    def get_created_at(self):
        return self.__created_at

    # --- Status change methods ---
    def do_check_in(self):
        if self.__status != self.CONFIRMED:
            raise ValueError("Only confirmed bookings can be checked in.")
        self.__status = self.CHECKED_IN

    def do_check_out(self):
        if self.__status != self.CHECKED_IN:
            raise ValueError("Guest must be checked in before checking out.")
        self.__status = self.CHECKED_OUT
        self.__room.set_booked(False)   # Object Interaction: free the room

    def do_cancel(self):
        if self.__status in (self.CHECKED_OUT, self.CANCELLED):
            raise ValueError("This booking cannot be cancelled.")
        self.__status = self.CANCELLED
        self.__room.set_booked(False)   # Object Interaction: free the room
        self.__guest.remove_booking(self.__booking_id)

    def get_receipt_text(self):
        line = "=" * 44
        thin = "-" * 44
        return (
            f"{line}\n"
            f"       GRAND AZURE HOTEL\n"
            f"         BOOKING RECEIPT\n"
            f"{line}\n"
            f"Booking ID   : {self.__booking_id}\n"
            f"Date Booked  : {self.__created_at.strftime('%d %b %Y  %H:%M')}\n"
            f"{thin}\n"
            f"Guest Name   : {self.__guest.get_name()}\n"
            f"IC Number    : {self.__guest.get_ic_number()}\n"
            f"Phone        : {self.__guest.get_phone()}\n"
            f"{thin}\n"
            f"Room No.     : {self.__room.get_room_number()}\n"
            f"Room Type    : {self.__room.get_room_type()}\n"
            f"Floor        : {self.__room.get_floor()}\n"
            f"Check-In     : {self.__check_in.strftime('%d %b %Y')}\n"
            f"Check-Out    : {self.__check_out.strftime('%d %b %Y')}\n"
            f"Nights       : {self.__nights}\n"
            f"Rate/Night   : RM {self.__room.get_price_per_night():.2f}\n"
            f"{thin}\n"
            f"TOTAL        : RM {self.__total_price:.2f}\n"
            f"Status       : {self.__status}\n"
            f"{line}\n"
        )

    # --- Serialization ---
    def to_dict(self):
        return {
            "booking_id": self.__booking_id,
            "guest_id": self.__guest.get_guest_id(),
            "room_number": self.__room.get_room_number(),
            "check_in": self.__check_in.strftime("%Y-%m-%d"),
            "nights": self.__nights,
            "status": self.__status,
            "created_at": self.__created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data, guest, room):
        b = cls.__new__(cls) # Bypass __init__ to avoid raising validation errors for historic bookings
        b._Booking__booking_id   = data["booking_id"]
        b._Booking__guest        = guest
        b._Booking__room         = room
        b._Booking__check_in     = datetime.strptime(data["check_in"], "%Y-%m-%d").date()
        b._Booking__nights       = data["nights"]
        b._Booking__check_out    = b._Booking__check_in + timedelta(days=data["nights"])
        b._Booking__total_price  = room.calculate_price(data["nights"])
        b._Booking__status       = data["status"]
        b._Booking__created_at   = datetime.fromisoformat(data["created_at"])
        
        id_num = int(data["booking_id"].replace("BK", ""))
        if id_num > cls._id_counter:
            cls._id_counter = id_num
            
        return b

    def __str__(self):
        return (f"[{self.__booking_id}] {self.__guest.get_name()} | "
                f"Room {self.__room.get_room_number()} ({self.__room.get_room_type()}) | "
                f"{self.__check_in} to {self.__check_out} | "
                f"RM {self.__total_price:.2f} | {self.__status}")
