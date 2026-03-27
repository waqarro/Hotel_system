from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box
from rich.layout import Layout
from rich.text import Text

console = Console()

class HotelCLI:
    def __init__(self, hotel):
        self.hotel = hotel

    def run(self):
        while True:
            console.clear()
            title = Text(f"{self.hotel.get_name()} Booking System", style="bold cyan", justify="center")
            console.print(Panel(title, box=box.DOUBLE, padding=(1, 2), border_style="cyan"))
            
            menu = Table.grid(padding=(0, 2))
            menu.add_column(style="bold green", justify="right")
            menu.add_column(style="white")
            
            menu.add_row("[1]", "Dashboard")
            menu.add_row("[2]", "View All Rooms")
            menu.add_row("[3]", "Register Guest")
            menu.add_row("[4]", "View All Guests")
            menu.add_row("[5]", "Make New Booking")
            menu.add_row("[6]", "Manage Bookings")
            menu.add_row("[0]", "Exit")
            
            console.print(Panel(menu, title="[yellow]Main Menu", box=box.ROUNDED, expand=False, border_style="yellow"))
            
            choice = Prompt.ask("[bold cyan]Enter your choice[/]", choices=["1", "2", "3", "4", "5", "6", "0"], default="1")
            
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
            elif choice == '0':
                console.print("\n[bold green]Thank you for using the Hotel Booking System. Goodbye![/]\n")
                break
                
            if choice != '0':
                Prompt.ask("\n[dim]Press Enter to return to the main menu...[/]")

    def show_dashboard(self):
        console.clear()
        stats = self.hotel.get_stats()
        
        table = Table(title="Hotel Dashboard", show_header=False, box=box.SIMPLE_HEAVY, title_style="bold magenta")
        table.add_column("Metric", style="bold cyan")
        table.add_column("Value", style="bold white")
        
        table.add_row("Total Rooms", str(stats['total_rooms']))
        table.add_row("Available Rooms", f"[green]{stats['available_rooms']}[/green]")
        table.add_row("Booked Rooms", f"[red]{stats['booked_rooms']}[/red]")
        table.add_row("Total Guests", str(stats['total_guests']))
        table.add_row("Total Bookings", str(stats['total_bookings']))
        table.add_row("Total Revenue", f"[bold yellow]RM {stats['total_revenue']:,.2f}[/bold yellow]")
        
        console.print(Panel(table, border_style="magenta", expand=False))

    def show_rooms(self):
        console.clear()
        rooms = self.hotel.get_all_rooms()
        
        table = Table(title="All Hotel Rooms", box=box.ROUNDED, header_style="bold blue")
        table.add_column("Room", justify="center")
        table.add_column("Type")
        table.add_column("Floor", justify="center")
        table.add_column("Capacity", justify="center")
        table.add_column("Rate/Night", justify="right")
        table.add_column("Status", justify="center")
        
        for r in rooms:
            status = "[bold red]Booked[/]" if r.is_booked() else "[bold green]Available[/]"
            table.add_row(
                str(r.get_room_number()),
                r.get_room_type(),
                str(r.get_floor()),
                str(r.get_capacity()),
                f"RM {r.get_price_per_night():.2f}",
                status
            )
            
        console.print(table)

    def register_guest(self):
        console.clear()
        console.print(Panel("[bold yellow]Register a New Guest[/]", border_style="yellow", expand=False))
        
        name = Prompt.ask("[cyan]Full Name[/]")
        ic = Prompt.ask("[cyan]IC/Passport Number[/]")
        phone = Prompt.ask("[cyan]Phone Number[/]")
        email = Prompt.ask("[cyan]Email (optional)[/]", default="")

        if not name or not ic or not phone:
            console.print("[bold red]Error: Name, IC, and Phone are strongly required.[/]")
            return

        try:
            guest = self.hotel.register_guest(name, ic, phone, email)
            console.print(f"\n[bold green]Success![/] Guest registered with ID: [bold white]{guest.get_guest_id()}[/]")
        except Exception as e:
            console.print(f"\n[bold red]Error:[/] {e}")

    def show_guests(self):
        console.clear()
        guests = self.hotel.get_all_guests()
        
        if not guests:
            console.print("[yellow]No guests registered yet.[/]")
            return
            
        table = Table(title="Registered Guests", box=box.ROUNDED, header_style="bold blue")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="white")
        table.add_column("IC/Passport")
        table.add_column("Phone")
        
        for g in guests:
            table.add_row(
                g.get_guest_id(),
                g.get_name(),
                g.get_ic_number(),
                g.get_phone()
            )
            
        console.print(table)

    def new_booking(self):
        console.clear()
        console.print(Panel("[bold yellow]Make a New Booking[/]", border_style="yellow", expand=False))
        
        # Show available rooms first
        avail_rooms = self.hotel.get_available_rooms()
        if not avail_rooms:
            console.print("[bold red]Sorry, no rooms are currently available.[/]")
            return
            
        room_list = ", ".join([str(r.get_room_number()) for r in avail_rooms])
        console.print(f"[dim]Available Rooms: {room_list}[/]\n")
        
        guest_id = Prompt.ask("[cyan]Enter Guest ID[/]").upper()
        guest = self.hotel.find_guest(guest_id)
        if not guest:
            console.print("[bold red]Error:[/] Guest not found. Please register the guest first.")
            return

        try:
            room_num = int(Prompt.ask("[cyan]Enter Room Number[/]"))
            checkin_str = Prompt.ask("[cyan]Check-In Date (DD/MM/YYYY)[/] [dim](Leave blank for today)[/]", default="")
            
            if not checkin_str:
                checkin = datetime.today().date()
            else:
                checkin = datetime.strptime(checkin_str, "%d/%m/%Y").date()
            
            nights = int(Prompt.ask("[cyan]Number of Nights[/]"))
        except ValueError:
            console.print("[bold red]Error:[/] Invalid input format. Please check your numbers and dates.")
            return

        try:
            booking = self.hotel.make_booking(guest, room_num, checkin, nights)
            console.print(Panel(
                f"[bold green]Booking Confirmed![/]\n"
                f"Booking ID: [bold white]{booking.get_booking_id()}[/]\n"
                f"Total Price: [bold yellow]RM {booking.get_total_price():.2f}[/]",
                border_style="green", expand=False
            ))
            
            import os
            os.makedirs("Receipts", exist_ok=True)
            with open(f"Receipts/{booking.get_booking_id()}_receipt.txt", "w") as f:
                f.write(booking.get_receipt_text())
            console.print(f"[dim]Receipt also saved to: Receipts/{booking.get_booking_id()}_receipt.txt[/]")
            
        except Exception as e:
            console.print(f"\n[bold red]Error:[/] {e}")

    def manage_bookings(self):
        console.clear()
        bookings = self.hotel.get_all_bookings()
        if not bookings:
            console.print("[yellow]No bookings exist yet.[/]")
            return
            
        table = Table(title="Manage Bookings", box=box.ROUNDED, header_style="bold blue")
        table.add_column("ID", style="cyan")
        table.add_column("Guest")
        table.add_column("Room", justify="center")
        table.add_column("Check-In")
        table.add_column("Check-Out")
        table.add_column("Status", justify="center")
        
        for b in bookings:
            status = b.get_status()
            status_color = "white"
            if status == "Confirmed": status_color = "blue"
            elif status == "Checked In": status_color = "green"
            elif status == "Checked Out": status_color = "dim"
            elif status == "Cancelled": status_color = "red"
            
            table.add_row(
                b.get_booking_id(),
                b.get_guest().get_name()[:15],
                str(b.get_room().get_room_number()),
                b.get_check_in().strftime('%d/%m/%Y'),
                b.get_check_out().strftime('%d/%m/%Y'),
                f"[bold {status_color}]{status}[/]"
            )
            
        console.print(table)
        
        console.print("\n[bold cyan]Actions:[/]")
        console.print("  [1] Check-In")
        console.print("  [2] Check-Out")
        console.print("  [3] Cancel Booking")
        console.print("  [4] View Receipt")
        console.print("  [0] Back to Menu")
        
        action = Prompt.ask("\n[cyan]Select an action[/]", choices=["1", "2", "3", "4", "0"], default="0")
        if action == '0':
            return
            
        bid = Prompt.ask("[cyan]Enter Booking ID[/]").upper()
        
        try:
            if action == '1':
                self.hotel.check_in(bid)
                console.print(f"[bold green]Successfully checked in booking {bid}![/]")
            elif action == '2':
                self.hotel.check_out(bid)
                console.print(f"[bold green]Successfully checked out booking {bid}![/]")
            elif action == '3':
                if Confirm.ask("[bold red]Are you sure you want to cancel this booking?[/]"):
                    self.hotel.cancel_booking(bid)
                    console.print(f"[bold green]Booking {bid} cancelled.[/]")
            elif action == '4':
                b = self.hotel.find_booking(bid)
                if b:
                    receipt_panel = Panel(b.get_receipt_text(), title="[green]Receipt[/]", border_style="green", expand=False)
                    console.clear()
                    console.print(receipt_panel)
                    
                    import os
                    os.makedirs("Receipts", exist_ok=True)
                    with open(f"Receipts/{b.get_booking_id()}_receipt.txt", "w") as f:
                        f.write(b.get_receipt_text())
                    console.print(f"\n[dim]Receipt downloaded to: Receipts/{b.get_booking_id()}_receipt.txt[/]")
                else:
                    console.print("[bold red]Error:[/] Booking not found.")
        except Exception as e:
            console.print(f"[bold red]Error:[/] {e}")
