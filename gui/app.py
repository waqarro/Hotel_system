"""
gui/app.py
Hotel Room Booking System - SEGi University Final Assessment
GUI built with tkinter (cross-platform: Windows, macOS, Linux)

No external libraries needed - tkinter is included with Python.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime


# -------------------------------------------------------
# Colour Palette and Font Settings
# -------------------------------------------------------
BG          = "#F8FAFC"
SIDEBAR_BG  = "#0F172A"
ACCENT      = "#3B82F6"
ACCENT_DARK = "#2563EB"
WHITE       = "#FFFFFF"
TEXT_DARK   = "#0F172A"
TEXT_LIGHT  = "#475569"
SUCCESS     = "#10B981"
WARNING     = "#F59E0B"
DANGER      = "#EF4444"
ROW_ODD     = "#F1F5F9"
ROW_EVEN    = "#FFFFFF"

FONT_HEADING  = ("Helvetica Neue", 20, "bold")
FONT_SUBHEAD  = ("Helvetica Neue", 14, "bold")
FONT_LABEL    = ("Helvetica Neue", 11)
FONT_BOLD     = ("Helvetica Neue", 11, "bold")
FONT_SMALL    = ("Helvetica Neue", 10)
FONT_MONO     = ("Menlo", 11)


# -------------------------------------------------------
# Helper: styled label
# -------------------------------------------------------
def make_label(parent, text, font=FONT_LABEL, fg=TEXT_DARK, bg=BG, **kw):
    return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kw)


def make_entry(parent, width=28):
    e = tk.Entry(parent, width=width, font=FONT_LABEL,
                 relief="flat", bd=0,
                 highlightthickness=1,
                 highlightbackground="#CBD5E1",
                 highlightcolor=ACCENT,
                 fg=TEXT_DARK, bg=WHITE, insertbackground=TEXT_DARK)
    return e


def make_button(parent, text, command, color=ACCENT, fg=WHITE, width=18):
    # macOS ignores background colors on native tk.Buttons.
    # Using tk.Label bound to click events creates perfectly colored, cross-platform flat buttons.
    btn = tk.Label(
        parent, text=text,
        bg=color, fg=fg, font=FONT_BOLD,
        padx=10, pady=6, cursor="hand2", width=width
    )
    btn.bind("<Button-1>", lambda e: command())
    return btn


# -------------------------------------------------------
# Main Application Window
# -------------------------------------------------------
class HotelApp(tk.Tk):
    """
    Main tkinter window.
    Contains the sidebar navigation and a content area that swaps frames.
    """

    def __init__(self, hotel):
        super().__init__()

        self.hotel = hotel  # reference to the Hotel model

        self.title("Grand Azure Hotel — Booking System")
        self.geometry("1050x650")
        self.minsize(900, 580)
        self.configure(bg=BG)

        # Try to set a nice window icon (won't crash if it fails)
        try:
            self.iconbitmap("")
        except Exception:
            pass

        self._build_layout()
        self._show_dashboard()  # default screen on startup

    # ---------------------------------------------------
    # Layout: sidebar + content area
    # ---------------------------------------------------
    def _build_layout(self):
        # Left sidebar
        self.sidebar = tk.Frame(self, bg=SIDEBAR_BG, width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Hotel name in sidebar
        tk.Label(
            self.sidebar, text="Grand Azure\nHotel",
            font=("Helvetica Neue", 12, "bold"), bg=SIDEBAR_BG,
            fg=WHITE, justify="center"
        ).pack(pady=(4, 24))

        # Separator
        tk.Frame(self.sidebar, bg="#2E3E50", height=1).pack(fill="x", padx=16)

        # Navigation buttons
        nav_items = [
            ("Dashboard",        self._show_dashboard),
            ("Rooms",            self._show_rooms),
            ("Register Guest",   self._show_register_guest),
            ("Guests",           self._show_guests),
            ("New Booking",      self._show_new_booking),
            ("Bookings",         self._show_bookings),
        ]

        self._nav_buttons = {}
        for label, command in nav_items:
            btn = tk.Label(
                self.sidebar, text=label,
                bg=SIDEBAR_BG, fg="#BDC3C7",
                font=FONT_LABEL, anchor="w", padx=24, pady=10,
                cursor="hand2", width=20
            )
            # Bind the click event to act like a button
            btn.bind("<Button-1>", lambda e, cmd=command: cmd())
            btn.pack(fill="x")
            self._nav_buttons[label] = btn

        # Version info at bottom of sidebar
        tk.Label(
            self.sidebar,
            text="SEGi University\nJan 2026",
            font=FONT_SMALL, bg=SIDEBAR_BG,
            fg="#566573"
        ).pack(side="bottom", pady=16)

        # Right content area
        self.content = tk.Frame(self, bg=BG)
        self.content.pack(side="right", fill="both", expand=True)

    def _highlight_nav(self, active_label):
        """Highlight the active sidebar button."""
        for label, btn in self._nav_buttons.items():
            if label == active_label:
                btn.configure(bg=ACCENT, fg=WHITE)
            else:
                btn.configure(bg=SIDEBAR_BG, fg="#BDC3C7")

    def _clear_content(self):
        """Remove all widgets from the content area."""
        for widget in self.content.winfo_children():
            widget.destroy()

    def _page_header(self, title, subtitle=""):
        """Draw a consistent page header."""
        header = tk.Frame(self.content, bg=WHITE, pady=18)
        header.pack(fill="x", padx=0)
        tk.Frame(header, bg=BG, width=28).pack(side="left")
        make_label(header, title, font=FONT_HEADING, bg=WHITE).pack(side="left")
        if subtitle:
            make_label(header, f"   {subtitle}", font=FONT_LABEL,
                       fg=TEXT_LIGHT, bg=WHITE).pack(side="left", pady=(6, 0))
        tk.Frame(self.content, bg="#E8EAF6", height=1).pack(fill="x")

    # ---------------------------------------------------
    # Dashboard screen
    # ---------------------------------------------------
    def _show_dashboard(self):
        self._clear_content()
        self._highlight_nav("Dashboard")
        self._page_header("Dashboard", "Hotel overview")

        stats = self.hotel.get_stats()

        # Stat cards row
        cards_frame = tk.Frame(self.content, bg=BG)
        cards_frame.pack(fill="x", padx=28, pady=22)

        card_data = [
            ("Total Rooms",      stats["total_rooms"],      ACCENT),
            ("Available",        stats["available_rooms"],  SUCCESS),
            ("Booked",           stats["booked_rooms"],     WARNING),
            ("Guests",           stats["total_guests"],     "#8E44AD"),
            ("Bookings",         stats["total_bookings"],   "#16A085"),
        ]

        for i, (label, value, color) in enumerate(card_data):
            card = tk.Frame(cards_frame, bg=WHITE, padx=16, pady=14,
                            relief="flat", bd=0,
                            highlightthickness=1,
                            highlightbackground="#E8EAF6")
            card.grid(row=0, column=i, padx=6, sticky="nsew")
            cards_frame.columnconfigure(i, weight=1)

            tk.Label(card, text=str(value), font=("Helvetica Neue", 22, "bold"),
                     fg=color, bg=WHITE).pack()
            tk.Label(card, text=label, font=FONT_SMALL,
                     fg=TEXT_LIGHT, bg=WHITE).pack()

        # Revenue box
        rev_frame = tk.Frame(self.content, bg=SUCCESS, pady=14, padx=24)
        rev_frame.pack(fill="x", padx=28, pady=(0, 18))
        tk.Label(rev_frame, text="Total Revenue",
                 font=FONT_BOLD, fg=WHITE, bg=SUCCESS).pack(side="left")
        tk.Label(rev_frame, text=f"RM {stats['total_revenue']:,.2f}",
                 font=("Helvetica Neue", 16, "bold"), fg=WHITE, bg=SUCCESS).pack(side="right")

        # Occupancy bar
        occ = stats["booked_rooms"] / stats["total_rooms"] if stats["total_rooms"] else 0
        occ_frame = tk.Frame(self.content, bg=WHITE, padx=24, pady=16,
                             highlightthickness=1, highlightbackground="#E8EAF6")
        occ_frame.pack(fill="x", padx=28, pady=(0, 16))
        tk.Label(occ_frame, text=f"Occupancy Rate   {occ*100:.1f}%",
                 font=FONT_BOLD, fg=TEXT_DARK, bg=WHITE).pack(anchor="w")
        bar_bg = tk.Frame(occ_frame, bg="#E8EAF6", height=12)
        bar_bg.pack(fill="x", pady=(6, 0))
        if occ > 0:
            bar_fill = tk.Frame(occ_frame, bg=ACCENT, height=12)
            bar_fill.place(in_=bar_bg, relwidth=occ, relheight=1)

        # Room type breakdown table
        tk.Label(self.content, text="Room Type Summary",
                 font=FONT_SUBHEAD, fg=TEXT_DARK, bg=BG).pack(anchor="w", padx=28, pady=(8, 6))

        table_frame = tk.Frame(self.content, bg=WHITE,
                               highlightthickness=1, highlightbackground="#E8EAF6")
        table_frame.pack(fill="x", padx=28)

        headers = ["Type", "Total", "Booked", "Available", "Rate/Night"]
        for col, h in enumerate(headers):
            tk.Label(table_frame, text=h, font=FONT_BOLD, fg=TEXT_LIGHT,
                     bg="#F0F3F4", padx=14, pady=8, anchor="w"
                     ).grid(row=0, column=col, sticky="ew", padx=1)
            table_frame.columnconfigure(col, weight=1)

        all_rooms = self.hotel.get_all_rooms()
        room_types = [("Standard", "RM 150.00"), ("Deluxe", "RM 280.00"), ("Suite", "RM 550.00")]
        for row_i, (rtype, rate) in enumerate(room_types):
            total  = sum(1 for r in all_rooms if r.get_room_type() == rtype)
            booked = sum(1 for r in all_rooms if r.get_room_type() == rtype and r.is_booked())
            bg     = ROW_ODD if row_i % 2 == 0 else ROW_EVEN
            for col, val in enumerate([rtype, total, booked, total-booked, rate]):
                tk.Label(table_frame, text=str(val), font=FONT_LABEL,
                         fg=TEXT_DARK, bg=bg, padx=14, pady=7, anchor="w"
                         ).grid(row=row_i+1, column=col, sticky="ew")

    # ---------------------------------------------------
    # Rooms screen
    # ---------------------------------------------------
    def _show_rooms(self):
        self._clear_content()
        self._highlight_nav("Rooms")
        self._page_header("Rooms", "All hotel rooms")

        # Filter bar
        filter_frame = tk.Frame(self.content, bg=BG)
        filter_frame.pack(fill="x", padx=28, pady=12)

        tk.Label(filter_frame, text="Filter by type:", font=FONT_LABEL,
                 fg=TEXT_DARK, bg=BG).pack(side="left")

        filter_var = tk.StringVar(value="All")
        for rtype in ["All", "Standard", "Deluxe", "Suite"]:
            tk.Radiobutton(
                filter_frame, text=rtype, variable=filter_var,
                value=rtype, bg=BG, fg=TEXT_DARK, font=FONT_LABEL,
                activebackground=BG, selectcolor=BG,
                command=lambda: self._refresh_rooms_table(tree, filter_var.get())
            ).pack(side="left", padx=8)

        # Scrollable table
        cols = ("Room No.", "Type", "Floor", "Capacity", "Rate/Night", "Status", "Description")
        tree, frame = self._make_table(cols)
        self._refresh_rooms_table(tree, "All")

        # Click to view details
        def on_select(event):
            sel = tree.selection()
            if sel:
                item  = tree.item(sel[0])
                rnum  = int(item["values"][0])
                room  = self.hotel.find_room(rnum)
                if room:
                    self._room_detail_popup(room)

        tree.bind("<Double-1>", on_select)
        tk.Label(self.content, text="Double-click a room to view details",
                 font=FONT_SMALL, fg=TEXT_LIGHT, bg=BG).pack(pady=4)

    def _refresh_rooms_table(self, tree, filter_type):
        tree.delete(*tree.get_children())
        rooms = self.hotel.get_all_rooms()
        if filter_type != "All":
            rooms = [r for r in rooms if r.get_room_type() == filter_type]
        for i, r in enumerate(rooms):
            status = "Booked" if r.is_booked() else "Available"
            tag    = "booked" if r.is_booked() else ("odd" if i % 2 == 0 else "even")
            tree.insert("", "end", tags=(tag,), values=(
                r.get_room_number(),
                r.get_room_type(),
                r.get_floor(),
                r.get_capacity(),
                f"RM {r.get_price_per_night():.2f}",
                status,
                r.get_description()[:55] + "..."
            ))
        tree.tag_configure("booked", background="#FDEDEC", foreground=DANGER)
        tree.tag_configure("odd",    background=ROW_ODD)
        tree.tag_configure("even",   background=ROW_EVEN)

    def _room_detail_popup(self, room):
        """Show room details in a small popup window."""
        popup = tk.Toplevel(self)
        popup.title(f"Room {room.get_room_number()} Details")
        popup.geometry("420x280")
        popup.resizable(False, False)
        popup.configure(bg=WHITE)
        popup.grab_set()    # make it modal

        status     = "Booked" if room.is_booked() else "Available"
        status_col = DANGER if room.is_booked() else SUCCESS

        tk.Label(popup, text=f"Room {room.get_room_number()} — {room.get_room_type()}",
                 font=FONT_SUBHEAD, fg=TEXT_DARK, bg=WHITE).pack(pady=(20, 4))
        tk.Frame(popup, bg="#E8EAF6", height=1).pack(fill="x", padx=20)

        info_frame = tk.Frame(popup, bg=WHITE, padx=24, pady=12)
        info_frame.pack(fill="both")

        rows = [
            ("Floor",        str(room.get_floor())),
            ("Capacity",     f"{room.get_capacity()} guests"),
            ("Rate/Night",   f"RM {room.get_price_per_night():.2f}"),
            ("Status",       status),
            ("Description",  room.get_description()),
        ]
        for label, value in rows:
            row = tk.Frame(info_frame, bg=WHITE)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=f"{label}:", font=FONT_BOLD, fg=TEXT_LIGHT,
                     bg=WHITE, width=14, anchor="w").pack(side="left")
            col = status_col if label == "Status" else TEXT_DARK
            tk.Label(row, text=value, font=FONT_LABEL, fg=col,
                     bg=WHITE, wraplength=240, anchor="w").pack(side="left")

        make_button(popup, "Close", popup.destroy, color=ACCENT_DARK, width=12
                    ).pack(pady=14)

    # ---------------------------------------------------
    # Register Guest screen
    # ---------------------------------------------------
    def _show_register_guest(self):
        self._clear_content()
        self._highlight_nav("Register Guest")
        self._page_header("Register Guest", "Add a new guest")

        form = tk.Frame(self.content, bg=WHITE, padx=32, pady=28,
                        highlightthickness=1, highlightbackground="#E8EAF6")
        form.pack(padx=40, pady=20, fill="x")

        fields = [
            ("Full Name *",              "name"),
            ("IC / Passport Number *",   "ic"),
            ("Phone Number *",           "phone"),
            ("Email Address (optional)", "email"),
        ]

        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(form, text=label, font=FONT_BOLD, fg=TEXT_DARK,
                     bg=WHITE, anchor="w").grid(row=i*2, column=0, columnspan=2,
                                                sticky="w", pady=(10, 2))
            e = make_entry(form, width=44)
            e.grid(row=i*2+1, column=0, columnspan=2, sticky="w", pady=(0, 4))
            entries[key] = e

        msg_var = tk.StringVar()
        msg_lbl = tk.Label(form, textvariable=msg_var, font=FONT_LABEL,
                           bg=WHITE, fg=SUCCESS)
        msg_lbl.grid(row=len(fields)*2+1, column=0, columnspan=2, pady=6)

        def do_register():
            name  = entries["name"].get().strip()
            ic    = entries["ic"].get().strip()
            phone = entries["phone"].get().strip()
            email = entries["email"].get().strip()

            if not name or not ic or not phone:
                msg_var.set("Please fill in all required fields.")
                msg_lbl.configure(fg=DANGER)
                return
            try:
                guest = self.hotel.register_guest(name, ic, phone, email)
                msg_var.set(f"Guest registered! ID: {guest.get_guest_id()}")
                msg_lbl.configure(fg=SUCCESS)
                for e in entries.values():
                    e.delete(0, "end")
            except Exception as ex:
                msg_var.set(str(ex))
                msg_lbl.configure(fg=DANGER)

        make_button(form, "Register Guest", do_register,
                    color=SUCCESS, width=20
                    ).grid(row=len(fields)*2, column=0, pady=(16, 0), sticky="w")

    # ---------------------------------------------------
    # Guests screen
    # ---------------------------------------------------
    def _show_guests(self):
        self._clear_content()
        self._highlight_nav("Guests")
        self._page_header("Guests", "All registered guests")

        cols = ("Guest ID", "Name", "IC (Masked)", "Phone", "Email", "Bookings")
        tree, _ = self._make_table(cols)

        guests = self.hotel.get_all_guests()
        if not guests:
            tree.insert("", "end", values=("—", "No guests registered yet.", "", "", "", ""))
        else:
            for i, g in enumerate(guests):
                bg_tag = "odd" if i % 2 == 0 else "even"
                tree.insert("", "end", tags=(bg_tag,), values=(
                    g.get_guest_id(),
                    g.get_name(),
                    g.get_ic_number(),
                    g.get_phone(),
                    g.get_email() or "—",
                    len(g.get_bookings()),
                ))
            tree.tag_configure("odd",  background=ROW_ODD)
            tree.tag_configure("even", background=ROW_EVEN)

    # ---------------------------------------------------
    # New Booking screen
    # ---------------------------------------------------
    def _show_new_booking(self):
        self._clear_content()
        self._highlight_nav("New Booking")
        self._page_header("New Booking", "Reserve a room")

        # Two-column layout
        outer = tk.Frame(self.content, bg=BG)
        outer.pack(fill="both", expand=True, padx=28, pady=16)

        # Left: form
        form = tk.Frame(outer, bg=WHITE, padx=28, pady=24,
                        highlightthickness=1, highlightbackground="#E8EAF6")
        form.pack(side="left", fill="both", expand=True, padx=(0, 12))

        # Right: available rooms
        right = tk.Frame(outer, bg=WHITE, padx=12, pady=16,
                         highlightthickness=1, highlightbackground="#E8EAF6")
        right.pack(side="right", fill="both", expand=True)

        tk.Label(right, text="Available Rooms", font=FONT_SUBHEAD,
                 fg=TEXT_DARK, bg=WHITE).pack(anchor="w", pady=(0, 8))

        room_cols = ("Room No.", "Type", "Floor", "Rate/Night")
        rooms_tree = ttk.Treeview(right, columns=room_cols, show="headings",
                                  height=14)
        for col in room_cols:
            rooms_tree.heading(col, text=col)
            rooms_tree.column(col, width=80, anchor="center")
        rooms_tree.pack(fill="both", expand=True)

        def refresh_rooms_list():
            rooms_tree.delete(*rooms_tree.get_children())
            avail = self.hotel.get_available_rooms()
            for i, r in enumerate(avail):
                tag = "odd" if i % 2 == 0 else "even"
                rooms_tree.insert("", "end", tags=(tag,), values=(
                    r.get_room_number(), r.get_room_type(),
                    r.get_floor(), f"RM {r.get_price_per_night():.2f}"
                ))
            rooms_tree.tag_configure("odd",  background=ROW_ODD)
            rooms_tree.tag_configure("even", background=ROW_EVEN)

        refresh_rooms_list()

        def fill_room_from_click(event):
            sel = rooms_tree.selection()
            if sel:
                rnum = rooms_tree.item(sel[0])["values"][0]
                room_entry.delete(0, "end")
                room_entry.insert(0, str(rnum))

        rooms_tree.bind("<Double-1>", fill_room_from_click)
        tk.Label(right, text="Double-click to select a room",
                 font=FONT_SMALL, fg=TEXT_LIGHT, bg=WHITE).pack(pady=4)

        # --- Form fields ---
        tk.Label(form, text="Guest ID *", font=FONT_BOLD, fg=TEXT_DARK,
                 bg=WHITE, anchor="w").pack(anchor="w", pady=(0, 2))
        guest_entry = make_entry(form, 32)
        guest_entry.pack(anchor="w", pady=(0, 10))

        tk.Label(form, text="Room Number *", font=FONT_BOLD, fg=TEXT_DARK,
                 bg=WHITE, anchor="w").pack(anchor="w", pady=(0, 2))
        room_entry = make_entry(form, 32)
        room_entry.pack(anchor="w", pady=(0, 10))

        tk.Label(form, text="Check-In Date * (DD/MM/YYYY)", font=FONT_BOLD,
                 fg=TEXT_DARK, bg=WHITE, anchor="w").pack(anchor="w", pady=(0, 2))
        checkin_entry = make_entry(form, 32)
        checkin_entry.insert(0, date.today().strftime("%d/%m/%Y"))
        checkin_entry.pack(anchor="w", pady=(0, 10))

        tk.Label(form, text="Number of Nights *", font=FONT_BOLD,
                 fg=TEXT_DARK, bg=WHITE, anchor="w").pack(anchor="w", pady=(0, 2))
        nights_entry = make_entry(form, 32)
        nights_entry.pack(anchor="w", pady=(0, 10))

        # Price preview label
        price_var = tk.StringVar(value="")
        tk.Label(form, textvariable=price_var, font=FONT_BOLD,
                 fg=ACCENT, bg=WHITE).pack(anchor="w", pady=(0, 6))

        def preview_price(*args):
            try:
                rnum  = int(room_entry.get())
                n     = int(nights_entry.get())
                room  = self.hotel.find_room(rnum)
                if room and n > 0:
                    total = room.calculate_price(n)  # Polymorphism used here
                    price_var.set(f"Estimated Total: RM {total:,.2f}")
                else:
                    price_var.set("")
            except (ValueError, TypeError):
                price_var.set("")

        room_entry.bind("<KeyRelease>",   preview_price)
        nights_entry.bind("<KeyRelease>", preview_price)

        msg_var = tk.StringVar()
        msg_lbl = tk.Label(form, textvariable=msg_var, font=FONT_LABEL,
                           bg=WHITE, fg=SUCCESS, wraplength=300, justify="left")
        msg_lbl.pack(anchor="w", pady=4)

        def do_book():
            guest_id = guest_entry.get().strip().upper()
            try:
                room_num = int(room_entry.get().strip())
                nights   = int(nights_entry.get().strip())
            except ValueError:
                msg_var.set("Room number and nights must be numbers.")
                msg_lbl.configure(fg=DANGER)
                return

            guest = self.hotel.find_guest(guest_id)
            if not guest:
                msg_var.set(f"Guest '{guest_id}' not found. Please register first.")
                msg_lbl.configure(fg=DANGER)
                return

            try:
                checkin_str = checkin_entry.get().strip()
                checkin     = datetime.strptime(checkin_str, "%d/%m/%Y").date()
            except ValueError:
                msg_var.set("Invalid date. Use DD/MM/YYYY.")
                msg_lbl.configure(fg=DANGER)
                return

            try:
                booking = self.hotel.make_booking(guest, room_num, checkin, nights)
                msg_var.set(f"Booking confirmed! ID: {booking.get_booking_id()}")
                msg_lbl.configure(fg=SUCCESS)
                # Show receipt popup
                self._receipt_popup(booking)
                refresh_rooms_list()
                for e in [guest_entry, room_entry, nights_entry]:
                    e.delete(0, "end")
                checkin_entry.delete(0, "end")
                checkin_entry.insert(0, date.today().strftime("%d/%m/%Y"))
                price_var.set("")
            except Exception as ex:
                msg_var.set(str(ex))
                msg_lbl.configure(fg=DANGER)

        make_button(form, "Confirm Booking", do_book,
                    color=SUCCESS, width=22).pack(anchor="w", pady=(6, 0))

    # ---------------------------------------------------
    # Bookings screen
    # ---------------------------------------------------
    def _show_bookings(self):
        self._clear_content()
        self._highlight_nav("Bookings")
        self._page_header("Bookings", "Manage all bookings")

        # Action buttons row
        action_frame = tk.Frame(self.content, bg=BG)
        action_frame.pack(fill="x", padx=28, pady=(10, 6))

        booking_id_var = tk.StringVar()
        tk.Label(action_frame, text="Booking ID:", font=FONT_LABEL,
                 fg=TEXT_DARK, bg=BG).pack(side="left")
        id_entry = make_entry(action_frame, 12)
        id_entry.pack(side="left", padx=(6, 16))

        msg_var = tk.StringVar()
        msg_lbl = tk.Label(action_frame, textvariable=msg_var,
                           font=FONT_LABEL, fg=SUCCESS, bg=BG)
        msg_lbl.pack(side="right", padx=12)

        cols = ("Booking ID", "Guest", "Room", "Type",
                "Check-In", "Check-Out", "Nights", "Total", "Status")
        tree, _ = self._make_table(cols)

        # Click to fill booking ID field
        def on_select(event):
            sel = tree.selection()
            if sel:
                bk_id = tree.item(sel[0])["values"][0]
                id_entry.delete(0, "end")
                id_entry.insert(0, str(bk_id))

        tree.bind("<ButtonRelease-1>", on_select)

        def refresh():
            tree.delete(*tree.get_children())
            bookings = self.hotel.get_all_bookings()
            status_tags = {
                "Confirmed"   : "confirmed",
                "Checked In"  : "checkedin",
                "Checked Out" : "checkedout",
                "Cancelled"   : "cancelled",
            }
            if not bookings:
                tree.insert("", "end", values=("—", "No bookings yet.", "", "", "", "", "", "", ""))
            for i, b in enumerate(bookings):
                tag = status_tags.get(b.get_status(), "even")
                tree.insert("", "end", tags=(tag,), values=(
                    b.get_booking_id(),
                    b.get_guest().get_name(),
                    b.get_room().get_room_number(),
                    b.get_room().get_room_type(),
                    b.get_check_in().strftime("%d/%m/%Y"),
                    b.get_check_out().strftime("%d/%m/%Y"),
                    b.get_nights(),
                    f"RM {b.get_total_price():.2f}",
                    b.get_status(),
                ))
            tree.tag_configure("confirmed",  background="#EBF5FB")
            tree.tag_configure("checkedin",  background="#EAFAF1", foreground=SUCCESS)
            tree.tag_configure("checkedout", background="#F2F3F4", foreground=TEXT_LIGHT)
            tree.tag_configure("cancelled",  background="#FDEDEC", foreground=DANGER)

        refresh()

        def action(fn, success_msg):
            bid = id_entry.get().strip().upper()
            if not bid:
                msg_var.set("Enter a Booking ID first.")
                msg_lbl.configure(fg=DANGER)
                return
            try:
                fn(bid)
                msg_var.set(success_msg)
                msg_lbl.configure(fg=SUCCESS)
                refresh()
            except Exception as ex:
                msg_var.set(str(ex))
                msg_lbl.configure(fg=DANGER)

        def show_receipt():
            bid     = id_entry.get().strip().upper()
            booking = self.hotel.find_booking(bid)
            if not booking:
                msg_var.set(f"Booking '{bid}' not found.")
                msg_lbl.configure(fg=DANGER)
                return
            self._receipt_popup(booking)

        # Buttons
        for text, color, fn in [
            ("Check In",       SUCCESS,  lambda: action(self.hotel.check_in,      "Guest checked in.")),
            ("Check Out",      WARNING,  lambda: action(self.hotel.check_out,     "Guest checked out.")),
            ("Cancel",         DANGER,   lambda: action(self.hotel.cancel_booking,"Booking cancelled.")),
            ("View Receipt",   ACCENT,   show_receipt),
        ]:
            make_button(action_frame, text, fn, color=color, width=12).pack(side="left", padx=4)

    # ---------------------------------------------------
    # Helpers: reusable scrollable table
    # ---------------------------------------------------
    def _make_table(self, columns):
        frame = tk.Frame(self.content, bg=BG)
        frame.pack(fill="both", expand=True, padx=28, pady=(8, 0))

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview",
                        background=WHITE,
                        foreground=TEXT_DARK,
                        rowheight=28,
                        fieldbackground=WHITE,
                        font=FONT_LABEL)
        style.configure("Custom.Treeview.Heading",
                        background="#F0F3F4",
                        foreground=TEXT_LIGHT,
                        font=FONT_BOLD,
                        relief="flat")
        style.map("Custom.Treeview", background=[("selected", ACCENT)])

        tree = ttk.Treeview(frame, columns=columns, show="headings",
                            style="Custom.Treeview")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=110, anchor="w", minwidth=60)

        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        return tree, frame

    # ---------------------------------------------------
    # Receipt popup
    # ---------------------------------------------------
    def _receipt_popup(self, booking):
        popup = tk.Toplevel(self)
        popup.title(f"Receipt — {booking.get_booking_id()}")
        popup.geometry("440x480")
        popup.resizable(False, False)
        popup.configure(bg=WHITE)
        popup.grab_set()

        text = tk.Text(popup, font=FONT_MONO, bg="#FAFAFA", fg=TEXT_DARK,
                       relief="flat", padx=16, pady=12, bd=0,
                       state="normal", wrap="none")
        text.pack(fill="both", expand=True, padx=16, pady=(16, 0))
        text.insert("1.0", booking.get_receipt_text())
        text.configure(state="disabled")   # make read-only
        
        # Save to file
        import os
        os.makedirs("Receipts", exist_ok=True)
        path = f"Receipts/{booking.get_booking_id()}_receipt.txt"
        with open(path, "w") as f:
            f.write(booking.get_receipt_text())
            
        tk.Label(popup, text=f"Saved to {path}", font=FONT_SMALL, fg=SUCCESS, bg=WHITE).pack(pady=(8, 0))

        make_button(popup, "Close", popup.destroy, color=ACCENT_DARK, width=14
                    ).pack(pady=10)
