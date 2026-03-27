import sys
import subprocess
import time

def ensure_dependencies():
    """
    Checks if required libraries are installed. 
    If not, silently installs them to prevent the application from crashing.
    """
    try:
        import rich
    except ImportError:
        print("\n\033[93m[System Setup]\033[0m Some required console libraries are missing.")
        print("Installing them automatically now so the program runs perfectly... Please wait.")
        try:
            cmd = [sys.executable, "-m", "pip", "install", "rich"]
            try:
                subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                cmd.append("--break-system-packages")
                subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
            print("\033[92mInstallation complete!\033[0m Starting application...\n")
            time.sleep(1)
        except Exception as e:
            print(f"\n\033[91mFailed to automatically install dependencies: {e}\033[0m")
            print("Please manually run: pip install rich")
            sys.exit(1)

def try_gui():
    print("\n\033[94m[System]\033[0m Checking GUI requirements...")
    try:
        import tkinter
    except ImportError:
        print("\n\033[93m[System] Tkinter is missing! Attempting automatic OS-level install...\033[0m")
        if sys.platform == "darwin":
            if subprocess.run(["which", "brew"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                print("\033[96m[Mac] Running: brew install python-tk\033[0m")
                subprocess.run(["brew", "install", "python-tk"])
            else:
                print("\033[91m[Error] macOS requires Homebrew to auto-install Tkinter. Please install Python from python.org.\033[0m")
                return False
        elif sys.platform.startswith("linux"):
            if subprocess.run(["which", "apt-get"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                print("\033[96m[Linux] Found apt. Your password may be required to install python3-tk.\033[0m")
                subprocess.run(["sudo", "apt-get", "update"])
                subprocess.run(["sudo", "apt-get", "install", "-y", "python3-tk"])
            else:
                print("\033[91m[Error] Auto-install only supports apt-based Linux distributions.\033[0m")
                return False
        else:
            print("\033[91m[Error] Windows requires Tkinter to be selected during the standard Python installation wizard.\033[0m")
            return False

        try:
            import tkinter
            print("\033[92m[System] Tkinter installed successfully!\033[0m")
        except ImportError:
            return False

    print("\n\033[94m[System]\033[0m Launching Graphical User Interface (GUI)...")
    try:
        result = subprocess.run([sys.executable, "gui_runner.py"])
        if result.returncode == 0:
            return True
        return False
    except Exception:
        return False

def main():
    # 1. Guarantee no ImportErrors happen for the CLI
    ensure_dependencies()
    
    # Now we can safely use rich for cool prompts
    from rich.prompt import Prompt, Confirm
    from rich.console import Console
    from rich.panel import Panel
    console = Console()
    
    console.print(Panel("[bold cyan]Welcome to the WAKA Hotel Booking System[/]", expand=False))
    
    # 2. Ask user what they want to run
    console.print()
    console.print("[bold yellow]How would you like to launch the application?[/]")
    console.print("  [bold cyan][1][/] Graphical Interface (GUI)")
    console.print("  [bold cyan][2][/] Terminal Console Interface")
    
    choice = Prompt.ask("\n[cyan]Enter your choice[/]", choices=["1", "2"], default="1")
    
    run_console = False
    
    if choice == "1":
        if try_gui():
            console.print("\n[green]Exiting GUI safely. Goodbye![/]")
            sys.exit(0)
        else:
            # 3. If GUI crashed or was missing tkinter (non-zero exit), ask about fallback
            console.print("\n[bold red][System] GUI launch failed (missing library or macOS trace crash).[/]")
            if Confirm.ask("[bold yellow]Would you like to run the robust Terminal version instead?[/]"):
                run_console = True
            else:
                console.print("\n[bold red]Exiting system. Goodbye![/]")
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
 