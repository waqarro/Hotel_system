======================================================
  GRAND AZURE HOTEL — ROOM BOOKING SYSTEM
  SEGi University Final Assessment (JAN 2026)
  DIT2133 / DCS2133 / PRG4064
======================================================

HOW TO RUN
----------
  Windows:   python main.py
  macOS:     python3 main.py
  Linux:     python3 main.py

If tkinter is missing on Linux:
  sudo apt install python3-tk

No other libraries needed — only Python 3.8+ is required.


PROJECT STRUCTURE
-----------------
hotel_gui/
│
├── main.py                  ← Entry point (run this)
│
├── models/
│   ├── room.py              ← Abstract Room + StandardRoom, DeluxeRoom, SuiteRoom
│   ├── guest.py             ← Guest class
│   ├── booking.py           ← Booking class
│   └── hotel.py             ← Hotel (manages everything)
│
└── gui/
    └── app.py               ← Full tkinter GUI (all screens)


OOP PRINCIPLES
--------------
[1] ENCAPSULATION
    All model classes use private attributes (double underscore)
    with getters and setters. Example: Room.__room_number,
    Guest.__ic_number, Booking.__total_price.

[2] INHERITANCE
    Room is the parent class. StandardRoom, DeluxeRoom, and
    SuiteRoom all inherit from Room using super().__init__().

[3] POLYMORPHISM
    get_description() and calculate_price() are defined in Room
    but behave differently in each subclass:
      - StandardRoom: flat rate
      - DeluxeRoom:   +10% weekend surcharge
      - SuiteRoom:    -15% loyalty discount for 5+ nights

[4] ABSTRACTION
    Room extends ABC (Abstract Base Class). It cannot be created
    directly. Subclasses MUST implement get_description() and
    calculate_price() or Python will raise a TypeError.


FEATURES
--------
  • Dashboard — occupancy rate, revenue, room breakdown
  • Room viewer — filter by type, double-click for details
  • Guest registration and listing
  • Booking form — live price preview, available rooms panel
  • Booking management — check in, check out, cancel, receipt
  • Printable booking receipts in popup window
