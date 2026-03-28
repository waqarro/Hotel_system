import sys
import subprocess
import time

def ensure_dependencies():
    """
    Check if required libraries are installed.
    Removed 'rich' from here since we use simple text now.
    """
    # No extra dependencies needed for simple text CLI
    pass

def try_gui():
    print("\n[System] Checking GUI requirements...")
    try:
        import tkinter
    except ImportError:
        print("\n[System] Tkinter is missing! Attempting automatic OS-level install...")
        if sys.platform == "darwin":
            if subprocess.run(["which", "brew"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                print("[Mac] Running: brew install python-tk")
                subprocess.run(["brew", "install", "python-tk"])
            else:
                print("[Error] macOS requires Homebrew to auto-install Tkinter. Please install Python from python.org.")
                return False
        elif sys.platform.startswith("linux"):
            if subprocess.run(["which", "apt-get"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                print("[Linux] Found apt. Your password may be required to install python3-tk.")
                subprocess.run(["sudo", "apt-get", "update"])
                subprocess.run(["sudo", "apt-get", "install", "-y", "python3-tk"])
            else:
                print("[Error] Auto-install only supports apt-based Linux distributions.")
                return False
        else:
            print("[Error] Windows requires Tkinter to be selected during the standard Python installation wizard.")
            return False

        try:
            import tkinter
            print("[System] Tkinter installed successfully!")
        except ImportError:
            return False

    print("\n[System] Launching Graphical User Interface (GUI)...")
    try:
        result = subprocess.run([sys.executable, "gui_runner.py"])
        if result.returncode == 0:
            return True
        return False
    except Exception:
        return False

def main():
    # 1. Start application
    print("\n" + "="*45)
    print("  Welcome to the WAKA Hotel Booking System")
    print("="*45)
    
    # 2. Ask user what they want to run
    print("\nHow would you like to launch the application?")
    print("  [1] Graphical Interface (GUI)")
    print("  [2] Terminal Console Interface")
    
    choice = input("\nEnter your choice (1): ") or "1"
    
    run_console = False
    
    if choice == "1":
        if try_gui():
            print("\nExiting GUI safely. Goodbye!")
            sys.exit(0)
        else:
            print("\n[System] GUI launch failed (missing library or macOS crash).")
            confirm = input("Would you like to run the Terminal version instead? (y/n): ")
            if confirm.lower() == 'y':
                run_console = True
            else:
                print("\nExiting system. Goodbye!")
                sys.exit(1)
    else:
        run_console = True
        
    if run_console:
        from cli import HotelCLI
        app = HotelCLI()
        
        try:
            app.run()
        except KeyboardInterrupt:
            print("\n\nExiting system safely. Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()