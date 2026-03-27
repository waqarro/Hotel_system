import sys

def run():
    try:
        import tkinter as tk
    except ImportError:
        print("Tkinter not installed.", file=sys.stderr)
        sys.exit(1)
        
    from models.hotel import Hotel
    from gui.app import HotelApp
    
    hotel = Hotel("WAKA Hotel")
    app = HotelApp(hotel)
    app.mainloop()

if __name__ == "__main__":
    run()
