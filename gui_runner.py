import sys

def run():
    try:
        import tkinter as tk
    except ImportError:
        print("Tkinter not installed.", file=sys.stderr)
        sys.exit(1)
        
    from gui.app import HotelApp
    
    app = HotelApp()
    app.mainloop()

if __name__ == "__main__":
    run()
