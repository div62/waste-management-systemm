"""
BinGO dashboard and pages.
bingo_login.py starts the app and passes in the role and the linked profile ID.
"""
import csv
import os
import sqlite3
from datetime import datetime
from tkinter import filedialog, messagebox

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

BACKGROUND = "#F2F6F4"
DARK_GREEN = "#075E4B"
GREEN = "#0B8F70"
LIGHT_GREEN = "#E4F4ED"
WHITE = "#FFFFFF"
TEXT = "#222831"
MUTED = "#7B858D"
BORDER = "#DCE7E2"
RED = "#D9534F"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "bingo.db")

SELECT_TEXT = "Select..."

MODULES = {
    "User Management": ("users", ["id", "name", "phone", "city"]),
    "Waste Management": ("waste_types", ["id", "name", "category", "description"]),
    "City Management": ("cities", ["id", "name", "state"]),
    "Service Providers": ("providers", ["id", "name", "service_type", "city_id"]),
    "Waste Collections": ("waste_collections", [
        "id", "waste_type", "quantity", "city_id", "area_id",
        "provider_id", "collection_date", "status",
    ]),
    "Scheduling": ("schedules", ["id", "collection_id", "date", "time", "provider_id", "status"]),
    "Requests": ("requests", [
        "id", "user_id", "waste_type", "quantity", "city_id",
        "area_id", "preferred_date", "status",
    ]),
    "Billing": ("bills", ["id", "user_id", "collection_id", "quantity", "rate", "total_amount", "payment_status"]),
}

# The pages each role can open. None means every page.
ROLE_PAGES = {
    "Admin": None,
    "Customer": {"Dashboard", "Requests", "Billing"},
    "Service Provider": {"Dashboard", "Requests", "Waste Collections", "Scheduling"},
}

ID_PREFIXES = {
    "users": "U", "waste_types": "W", "cities": "C", "providers": "P",
    "waste_collections": "WC", "schedules": "S", "requests": "R", "bills": "B",
}

# Fields that point to another table. The dropdown shows a name,
# and the database stores the related record ID.
REFERENCE_FIELDS = {
    ("providers", "city_id"): ("cities", "name"),
    ("waste_collections", "waste_type"): ("waste_types", "name"),
    ("waste_collections", "city_id"): ("cities", "name"),
    ("waste_collections", "provider_id"): ("providers", "name"),
    ("schedules", "collection_id"): ("waste_collections", "id"),
    ("schedules", "provider_id"): ("providers", "name"),
    ("requests", "user_id"): ("users", "name"),
    ("requests", "waste_type"): ("waste_types", "name"),
    ("requests", "city_id"): ("cities", "name"),
    ("bills", "user_id"): ("users", "name"),
    ("bills", "collection_id"): ("waste_collections", "id"),
}


# ---------- Database helpers ----------

def get_connection():
    return sqlite3.connect(DB_PATH)


def get_count(table_name):
    """Return the number of records in a table."""
    try:
        connection = get_connection()
        count = connection.execute('SELECT COUNT(*) FROM "' + table_name + '"').fetchone()[0]
        connection.close()
        return count
    except sqlite3.Error:
        return 0


def get_rows(table_name, columns):
    """Read the given columns from a table."""
    connection = get_connection()
    column_text = ", ".join('"' + column + '"' for column in columns)
    rows = connection.execute("SELECT " + column_text + ' FROM "' + table_name + '"').fetchall()
    connection.close()
    return rows


def generate_id(table_name):
    """Make the next ID for a table, such as R003 after R002."""
    prefix = ID_PREFIXES[table_name]
    connection = get_connection()
    existing_ids = connection.execute('SELECT id FROM "' + table_name + '"').fetchall()
    connection.close()
    highest_number = 0
    for (value,) in existing_ids:
        value = str(value)
        if value.startswith(prefix):
            number_part = value[len(prefix):]
            if number_part.isdigit() and int(number_part) > highest_number:
                highest_number = int(number_part)
    return prefix + str(highest_number + 1).zfill(3)


def get_reference_options(table_name, column):
    """Return dropdown labels mapped to the ID stored in the database."""
    reference = REFERENCE_FIELDS.get((table_name, column))
    if not reference:
        return None
    related_table, display_column = reference
    connection = get_connection()
    rows = connection.execute(
        'SELECT id, "' + display_column + '" FROM "' + related_table + '" ORDER BY id'
    ).fetchall()
    connection.close()
    return {
        str(display_name) + " (" + str(record_id) + ")": str(record_id)
        for record_id, display_name in rows
    }


def search_rows(rows, search_text):
    """Keep the rows where any shown value contains the search text."""
    search_value = search_text.lower()
    return [
        row for row in rows
        if any(search_value in str(value).lower() for value in row if value is not None)
    ]


def row_stripe(row_index):
    """Alternate the background colour of table rows."""
    return "#F6FAF8" if row_index % 2 == 1 else WHITE


# ---------- Main window ----------

class BinGOApp(ctk.CTk):
    def __init__(self, role="Admin", linked_id=None):
        super().__init__()
        self.role = role
        self.linked_id = linked_id
        self.title("BinGO | Smart Waste Management System")
        self.geometry("1280x800")
        self.minsize(1100, 680)
        self.configure(fg_color=BACKGROUND)
        self.current_page = "Dashboard"
        self.selected_record = None
        self.row_cells = []
        self.create_layout()
        self.show_dashboard()
        self.after(30000, self.auto_refresh_dashboard)

    def create_layout(self):
        self.sidebar = ctk.CTkFrame(self, width=245, corner_radius=0, fg_color=DARK_GREEN)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(
            self.sidebar, text="♻️ BinGO", font=("Segoe UI", 29, "bold"), text_color=WHITE
        ).pack(anchor="w", padx=22, pady=(25, 2))
        ctk.CTkLabel(
            self.sidebar, text="SMART WASTE MANAGEMENT", font=("Segoe UI", 10, "bold"),
            text_color="#CDEDE3"
        ).pack(anchor="w", padx=23, pady=(0, 25))

        self.nav_buttons = {}
        menu_items = [
            ("Dashboard", "🏠"),
            ("User Management", "🚹"),
            ("Waste Management", "🗑️"),
            ("City Management", "🏢"),
            ("Service Providers", "👥"),
            ("Waste Collections", "🔶"),
            ("Scheduling", "🕑"),
            ("Requests", "🗳️"),
            ("Billing", "🧾"),
        ]

        allowed_pages = ROLE_PAGES.get(self.role)
        for name, icon in menu_items:
            if allowed_pages is not None and name not in allowed_pages:
                continue
            button = ctk.CTkButton(
                self.sidebar,
                text=icon + "    " + name,
                height=44,
                corner_radius=10,
                anchor="w",
                font=("Segoe UI", 12),
                fg_color="transparent",
                hover_color="#0B8066",
                text_color=WHITE,
                command=lambda page=name: self.open_page(page),
            )
            button.pack(fill="x", padx=12, pady=3)
            self.nav_buttons[name] = button

        ctk.CTkFrame(self.sidebar, height=1, fg_color="#3C9B87").pack(fill="x", padx=18, pady=(20, 12))
        ctk.CTkButton(
            self.sidebar, text="↪    Exit Application", height=42,
            corner_radius=9, fg_color="#B84040", hover_color="#963333",
            text_color=WHITE, command=self.confirm_exit,
        ).pack(side="bottom", fill="x", padx=12, pady=18)

        self.main_panel = ctk.CTkFrame(self, corner_radius=0, fg_color=BACKGROUND)
        self.main_panel.pack(side="right", fill="both", expand=True)

        self.topbar = ctk.CTkFrame(
            self.main_panel, height=64, corner_radius=0, fg_color=WHITE,
            border_width=1, border_color=BORDER,
        )
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)
        self.topbar_title = ctk.CTkLabel(
            self.topbar, text="BinGO Dashboard", font=("Segoe UI", 17, "bold"), text_color=TEXT
        )
        self.topbar_title.pack(side="left", padx=24)
        ctk.CTkLabel(
            self.topbar, text="●  System Ready", font=("Segoe UI", 11), text_color=GREEN
        ).pack(side="right", padx=24)

        self.page_area = ctk.CTkFrame(self.main_panel, fg_color=BACKGROUND, corner_radius=0)
        self.page_area.pack(fill="both", expand=True, padx=22, pady=18)

    def clear_page(self):
        for widget in self.page_area.winfo_children():
            widget.destroy()

    def add_card_hover(self, card, normal_color=WHITE, hover_color=LIGHT_GREEN):
        """Give a card a colour and border change when the mouse moves over it."""
        def on_enter(event=None):
            try:
                card.configure(fg_color=hover_color, border_color=GREEN, border_width=2)
            except Exception:
                pass

        def on_leave(event=None):
            try:
                card.configure(fg_color=normal_color, border_color=BORDER, border_width=1)
            except Exception:
                pass

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        for child in card.winfo_children():
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)

    def set_active_button(self, page_name):
        for name, button in self.nav_buttons.items():
            button.configure(fg_color="#15977D" if name == page_name else "transparent")

    def open_page(self, page_name):
        self.current_page = page_name
        self.topbar_title.configure(text="BinGO  /  " + page_name)
        self.set_active_button(page_name)
        if page_name == "Dashboard":
            self.show_dashboard()
        else:
            self.show_module(page_name)

    def auto_refresh_dashboard(self):
        """Refresh the dashboard every 30 seconds while it is open."""
        if not self.winfo_exists():
            return
        if self.current_page == "Dashboard":
            self.show_dashboard()
        self.after(30000, self.auto_refresh_dashboard)

    def create_heading(self, title, subtitle):
        ctk.CTkLabel(
            self.page_area, text=title, font=("Segoe UI", 27, "bold"), text_color=TEXT
        ).pack(anchor="w", padx=8, pady=(3, 0))
        ctk.CTkLabel(
            self.page_area, text=subtitle, font=("Segoe UI", 12), text_color=MUTED
        ).pack(anchor="w", padx=8, pady=(2, 15))

    # ---------- Dashboard ----------

    def show_dashboard(self):
        self.clear_page()
        self.current_page = "Dashboard"
        self.topbar_title.configure(text="BinGO  /  Dashboard")
        self.set_active_button("Dashboard")

        is_admin = self.role == "Admin"
        body = ctk.CTkScrollableFrame(self.page_area, fg_color=BACKGROUND, corner_radius=10)
        body.pack(fill="both", expand=True)

        heading = ctk.CTkFrame(body, fg_color="transparent")
        heading.pack(fill="x", padx=8, pady=(8, 0))
        ctk.CTkLabel(
            heading, text="Dashboard & Analytics", font=("Segoe UI", 27, "bold"), text_color=TEXT
        ).pack(side="left", anchor="w")
        ctk.CTkButton(
            heading, text="↻ Refresh Dashboard", width=150, height=32,
            fg_color=GREEN, hover_color=DARK_GREEN, command=self.show_dashboard,
        ).pack(side="right", padx=(8, 0), pady=(2, 0))

        welcome = ("Welcome back! Click any card to open that section." if is_admin
                   else "Welcome back! Click a card to open that section.")
        ctk.CTkLabel(body, text=welcome, font=("Segoe UI", 12), text_color=MUTED).pack(
            anchor="w", padx=8, pady=(3, 15))

        def count_rows(table_name, column=None):
            """Count all rows, or only the rows that belong to this login."""
            try:
                connection = get_connection()
                if column is None:
                    count = connection.execute('SELECT COUNT(*) FROM "' + table_name + '"').fetchone()[0]
                else:
                    count = connection.execute(
                        'SELECT COUNT(*) FROM "' + table_name + '" WHERE "' + column + '" = ?',
                        (self.linked_id,),
                    ).fetchone()[0]
                connection.close()
                return count
            except sqlite3.Error:
                return 0

        def make_clickable(widget, page_name):
            """Open a page when the card, or anything inside it, is clicked."""
            widget.bind("<Button-1>", lambda event: self.open_page(page_name))
            try:
                widget.configure(cursor="hand2")
            except Exception:
                pass
            for child in widget.winfo_children():
                make_clickable(child, page_name)

        # Each card: (title, number, description, page to open, icon)
        if is_admin:
            stats = [
                ("Registered Users", count_rows("users"), "People using BinGO", "User Management", "👤"),
                ("Waste Types", count_rows("waste_types"), "Types of waste", "Waste Management", "♻️"),
                ("Service Providers", count_rows("providers"), "Available providers", "Service Providers", "🚛"),
                ("Waste Collections", count_rows("waste_collections"), "Collection records", "Waste Collections", "📦"),
                ("Registered Cities", count_rows("cities"), "Cities in the system", "City Management", "🏙️"),
                ("Schedules", count_rows("schedules"), "Planned collections", "Scheduling", "🗓️"),
                ("Requests", count_rows("requests"), "Collection requests", "Requests", "📨"),
                ("Bills", count_rows("bills"), "Billing records", "Billing", "🧾"),
            ]
        elif self.role == "Customer":
            stats = [
                ("My Requests", count_rows("requests", "user_id"), "Your pickup requests", "Requests", "📨"),
                ("My Bills", count_rows("bills", "user_id"), "Your billing records", "Billing", "🧾"),
            ]
        else:
            stats = [
                ("My Collections", count_rows("waste_collections", "provider_id"),
                 "Collections assigned to you", "Waste Collections", "📦"),
                ("My Schedules", count_rows("schedules", "provider_id"),
                 "Your planned collections", "Scheduling", "🗓️"),
            ]

        ctk.CTkLabel(
            body, text="SYSTEM OVERVIEW" if is_admin else "YOUR OVERVIEW",
            font=("Segoe UI", 10, "bold"), text_color=GREEN,
        ).pack(anchor="w", padx=8, pady=(0, 4))

        cards = ctk.CTkFrame(body, fg_color="transparent")
        cards.pack(fill="x", padx=3, pady=(0, 18))

        for index, (title, value, description, page_name, icon) in enumerate(stats):
            row = index // 4
            column = index % 4
            cards.grid_columnconfigure(column, weight=1, uniform="stats")
            card = ctk.CTkFrame(cards, fg_color=WHITE, corner_radius=15, border_width=1, border_color=BORDER)
            card.grid(row=row, column=column, sticky="nsew", padx=5, pady=5)

            ctk.CTkFrame(card, height=4, fg_color=GREEN, corner_radius=0).pack(fill="x")
            card_top = ctk.CTkFrame(card, fg_color="transparent")
            card_top.pack(fill="x", padx=13, pady=(10, 1))
            ctk.CTkLabel(card_top, text=title, font=("Segoe UI", 11, "bold"), text_color=TEXT).pack(
                side="left", anchor="w")
            ctk.CTkLabel(card_top, text=icon, font=("Segoe UI Emoji", 17), text_color=GREEN).pack(
                side="right", anchor="e")
            ctk.CTkLabel(card, text=str(value), font=("Segoe UI", 27, "bold"), text_color=DARK_GREEN).pack(
                anchor="w", padx=13, pady=(1, 1))
            ctk.CTkLabel(card, text=description, font=("Segoe UI", 9), text_color=MUTED).pack(
                anchor="w", padx=13, pady=(0, 12))

            self.add_card_hover(card)
            make_clickable(card, page_name)

        if is_admin:
            chart_section = ctk.CTkFrame(body, fg_color="transparent")
            chart_section.pack(fill="both", expand=True, padx=3, pady=(0, 10))
            chart_section.grid_columnconfigure(0, weight=3, uniform="charts")
            chart_section.grid_columnconfigure(1, weight=2, uniform="charts")
            chart_section.grid_rowconfigure(0, weight=3, minsize=280)
            chart_section.grid_rowconfigure(1, weight=2, minsize=250)

            bar_card = ctk.CTkFrame(chart_section, fg_color=WHITE, corner_radius=15, border_width=1, border_color=BORDER)
            bar_card.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            pie_card = ctk.CTkFrame(chart_section, fg_color=WHITE, corner_radius=15, border_width=1, border_color=BORDER)
            pie_card.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
            trend_card = ctk.CTkFrame(chart_section, fg_color=WHITE, corner_radius=15, border_width=1, border_color=BORDER)
            trend_card.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
            self.add_card_hover(bar_card)
            self.add_card_hover(pie_card)
            self.add_card_hover(trend_card)

            ctk.CTkLabel(bar_card, text="Waste Quantity by Type", font=("Segoe UI", 14, "bold"),
                         text_color=TEXT).pack(anchor="w", padx=14, pady=(12, 0))
            ctk.CTkLabel(pie_card, text="Collection Status", font=("Segoe UI", 14, "bold"),
                         text_color=TEXT).pack(anchor="w", padx=14, pady=(12, 0))
            ctk.CTkLabel(trend_card, text="Waste Collected by Date", font=("Segoe UI", 14, "bold"),
                         text_color=TEXT).pack(anchor="w", padx=14, pady=(12, 0))
            self.create_charts(bar_card, pie_card)
            self.create_collection_trend_chart(trend_card)
        else:
            ctk.CTkLabel(body, text="Charts show all records, so only the Admin can see them.",
                         font=("Segoe UI", 11), text_color=MUTED).pack(anchor="w", padx=8, pady=10)

        if not os.path.exists(DB_PATH):
            ctk.CTkLabel(
                body, text="Database file not found yet. Run your existing BinGO program first to create bingo.db.",
                text_color=RED, font=("Segoe UI", 11),
            ).pack(anchor="w", padx=10, pady=8)

    def create_charts(self, bar_card, pie_card):
        figure = Figure(figsize=(6.3, 3.0), dpi=90, facecolor=WHITE)
        axis = figure.add_subplot(111)
        axis.set_facecolor(WHITE)

        try:
            connection = get_connection()
            rows = connection.execute("SELECT waste_type, quantity FROM waste_collections").fetchall()
            connection.close()
        except sqlite3.Error:
            rows = []

        totals = {}
        for waste_type, quantity in rows:
            label = str(waste_type) if waste_type else "Unspecified"
            try:
                amount = float(quantity)
            except (TypeError, ValueError):
                amount = 0
            totals[label] = totals.get(label, 0) + amount

        if totals:
            bars = axis.bar(list(totals.keys()), list(totals.values()), color=GREEN, width=0.62)
            axis.set_ylabel("Quantity (kg)", fontsize=9, color=MUTED)
            axis.tick_params(axis="x", labelrotation=25, labelsize=8, colors=MUTED)
            axis.tick_params(axis="y", labelsize=8, colors=MUTED)
            axis.grid(axis="y", alpha=0.18, linestyle="--")
            axis.set_axisbelow(True)
            axis.spines["top"].set_visible(False)
            axis.spines["right"].set_visible(False)
            axis.spines["left"].set_color(BORDER)
            axis.spines["bottom"].set_color(BORDER)
            for bar in bars:
                axis.annotate(
                    format(bar.get_height(), "g"),
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    ha="center", va="bottom", fontsize=8, color=DARK_GREEN,
                    xytext=(0, 3), textcoords="offset points",
                )
        else:
            axis.text(0.5, 0.5, "No collection data yet", ha="center", va="center", color=MUTED)
            axis.set_xticks([])
            axis.set_yticks([])
        figure.tight_layout(pad=2)
        canvas = FigureCanvasTkAgg(figure, master=bar_card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=4)

        pie_figure = Figure(figsize=(4.0, 3.0), dpi=90, facecolor=WHITE)
        pie_axis = pie_figure.add_subplot(111)
        try:
            connection = get_connection()
            status_rows = connection.execute(
                "SELECT status, COUNT(*) FROM waste_collections GROUP BY status"
            ).fetchall()
            connection.close()
        except sqlite3.Error:
            status_rows = []

        status_labels = [str(row[0]) if row[0] else "Unspecified" for row in status_rows]
        status_counts = [row[1] for row in status_rows]
        if status_counts and sum(status_counts) > 0:
            pie_axis.pie(
                status_counts, labels=status_labels, autopct="%1.0f%%",
                startangle=90, counterclock=False,
                colors=["#0B8F70", "#75C9A8", "#F2C879", "#7FA8D8", "#DCE7E2"],
                wedgeprops={"width": 0.42, "edgecolor": WHITE, "linewidth": 2},
                pctdistance=0.78, textprops={"fontsize": 8, "color": TEXT},
            )
            pie_axis.set_aspect("equal")
        else:
            pie_axis.text(0.5, 0.5, "No status data yet", ha="center", va="center", color=MUTED)
            pie_axis.set_xticks([])
            pie_axis.set_yticks([])
        pie_figure.tight_layout(pad=1)
        pie_canvas = FigureCanvasTkAgg(pie_figure, master=pie_card)
        pie_canvas.draw()
        pie_canvas.get_tk_widget().pack(fill="both", expand=True, padx=4, pady=4)

    def create_collection_trend_chart(self, trend_card):
        """Draw a line graph of the total waste collected on each date."""
        figure = Figure(figsize=(8.0, 2.7), dpi=90, facecolor=WHITE)
        axis = figure.add_subplot(111)
        axis.set_facecolor(WHITE)

        try:
            connection = get_connection()
            rows = connection.execute("SELECT collection_date, quantity FROM waste_collections").fetchall()
            connection.close()
        except sqlite3.Error:
            rows = []

        daily_totals = {}
        for collection_date, quantity in rows:
            date_label = str(collection_date) if collection_date else "Unknown date"
            try:
                amount = float(quantity)
            except (TypeError, ValueError):
                amount = 0
            daily_totals[date_label] = daily_totals.get(date_label, 0) + amount

        def date_sort_key(label):
            for date_format in ("%d/%m/%Y", "%Y-%m-%d"):
                try:
                    return datetime.strptime(label, date_format)
                except ValueError:
                    pass
            return datetime.max

        dates = sorted(daily_totals.keys(), key=date_sort_key)
        amounts = [daily_totals[date_label] for date_label in dates]

        if dates:
            axis.plot(dates, amounts, marker="o", markersize=5, linewidth=2.5, color=GREEN)
            axis.fill_between(dates, amounts, color=GREEN, alpha=0.10)
            axis.set_ylabel("Quantity (kg)", fontsize=9, color=MUTED)
            axis.tick_params(axis="x", labelrotation=25, labelsize=8, colors=MUTED)
            axis.tick_params(axis="y", labelsize=8, colors=MUTED)
            axis.grid(axis="y", alpha=0.18, linestyle="--")
            axis.set_axisbelow(True)
            axis.spines["top"].set_visible(False)
            axis.spines["right"].set_visible(False)
            axis.spines["left"].set_color(BORDER)
            axis.spines["bottom"].set_color(BORDER)
        else:
            axis.text(0.5, 0.5, "No collection date data yet", ha="center", va="center", color=MUTED)
            axis.set_xticks([])
            axis.set_yticks([])

        figure.tight_layout(pad=2)
        canvas = FigureCanvasTkAgg(figure, master=trend_card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=4)

    # ---------- Record pages ----------

    def filter_rows_for_role(self, page_name, columns, rows):
        """Keep only the rows this login is allowed to see."""
        if self.role == "Admin":
            return rows

        if self.role == "Customer" and page_name in ("Requests", "Billing"):
            owner_index = columns.index("user_id")
            return [row for row in rows if row[owner_index] == self.linked_id]

        if self.role == "Service Provider":
            if page_name in ("Waste Collections", "Scheduling"):
                owner_index = columns.index("provider_id")
                return [row for row in rows if row[owner_index] == self.linked_id]
            if page_name == "Requests":
                # Pending requests from this provider's city, plus accepted requests
                # whose collection was deleted, so they can be accepted again.
                city_index = columns.index("city_id")
                status_index = columns.index("status")
                id_index = columns.index("id")
                provider_city = self.get_provider_city()
                linked_ids = self.get_linked_request_ids()
                return [
                    row for row in rows
                    if row[city_index] == provider_city
                    and (row[status_index] == "Pending"
                         or (row[status_index] == "Accepted" and row[id_index] not in linked_ids))
                ]

        return rows

    def display_value(self, table_name, column, value):
        """Show a friendly value. Provider cities show the name next to the ID."""
        if value is None:
            return ""
        if table_name == "providers" and column == "city_id":
            connection = get_connection()
            row = connection.execute("SELECT name FROM cities WHERE id = ?", (value,)).fetchone()
            connection.close()
            if row:
                return str(row[0]) + " (" + str(value) + ")"
        return str(value)

    def add_toolbar_button(self, toolbar, text, width, color, hover, command, text_color=WHITE):
        ctk.CTkButton(
            toolbar, text=text, width=width, height=32, fg_color=color, hover_color=hover,
            text_color=text_color, command=command,
        ).pack(side="right", padx=(8, 0))

    def show_module(self, page_name, search_text=""):
        self.clear_page()
        self.create_heading(page_name, "View records saved in your BinGO database.")

        if page_name not in MODULES:
            ctk.CTkLabel(self.page_area, text="This section is not available yet.",
                         text_color=MUTED).pack(pady=20)
            return

        table_name, columns = MODULES[page_name]
        self.selected_record = None
        self.row_cells = []

        toolbar = ctk.CTkFrame(self.page_area, fg_color="transparent")
        toolbar.pack(fill="x", padx=8, pady=(0, 10))
        ctk.CTkLabel(toolbar, text="Total records: " + str(get_count(table_name)),
                     font=("Segoe UI", 12, "bold"), text_color=TEXT).pack(side="left", padx=(0, 10))

        search_entry = ctk.CTkEntry(toolbar, width=190, height=32, placeholder_text="Search records...")
        search_entry.pack(side="left", padx=(0, 6))
        if search_text:
            search_entry.insert(0, search_text)
        ctk.CTkButton(
            toolbar, text="🔍 Search", width=90, height=32, fg_color=DARK_GREEN, hover_color=GREEN,
            command=lambda: self.show_module(page_name, search_entry.get()),
        ).pack(side="left", padx=(0, 6))
        ctk.CTkButton(
            toolbar, text="Clear", width=60, height=32, fg_color="#DDE5E2", hover_color="#C9D5D0",
            text_color=TEXT, command=lambda: self.show_module(page_name),
        ).pack(side="left")

        # Buttons on the right side. The first one added sits furthest right.
        self.add_toolbar_button(
            toolbar, "🔄 Refresh", 100, GREEN, DARK_GREEN,
            lambda: self.show_module(page_name, search_entry.get()))
        self.add_toolbar_button(
            toolbar, "⏬ Export CSV", 110, "#2878A5", "#205F83",
            lambda: self.export_module_csv(page_name, search_entry.get()))

        if self.role == "Admin":
            self.add_toolbar_button(
                toolbar, "🚮 Delete Selected", 135, "#C94C4C", "#A93636",
                lambda: self.delete_selected_record(page_name))
            self.add_toolbar_button(
                toolbar, "🖋️ Update Selected", 135, "#D98C24", "#B87518",
                lambda: self.open_update_form(page_name))
            self.add_toolbar_button(
                toolbar, "➕ Add Record", 120, DARK_GREEN, GREEN,
                lambda: self.open_add_form(page_name))

        if self.role == "Customer" and page_name == "Requests":
            self.add_toolbar_button(
                toolbar, "➕ New Request", 140, DARK_GREEN, GREEN, self.open_new_request_form)

        if self.role == "Service Provider" and page_name == "Requests":
            self.add_toolbar_button(
                toolbar, "✅ Accept Request", 150, DARK_GREEN, GREEN, self.accept_selected_request)

        if self.role == "Service Provider" and page_name == "Waste Collections":
            self.add_toolbar_button(
                toolbar, "✅ Mark Collected", 150, DARK_GREEN, GREEN, self.mark_selected_collected)

        table_frame = ctk.CTkScrollableFrame(
            self.page_area, fg_color=WHITE, corner_radius=10, border_width=1, border_color=BORDER
        )
        table_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        try:
            rows = self.filter_rows_for_role(page_name, columns, get_rows(table_name, columns))
        except sqlite3.Error as error:
            ctk.CTkLabel(
                table_frame,
                text="Could not load this table. Make sure your BinGO database has been created.\n" + str(error),
                text_color=RED, justify="left",
            ).pack(anchor="w", padx=12, pady=15)
            return

        if search_text:
            rows = search_rows(rows, search_text)

        for column_index, column_name in enumerate(columns):
            table_frame.grid_columnconfigure(column_index, weight=1, uniform="table")
            ctk.CTkLabel(
                table_frame, text=column_name.replace("_", " ").title(),
                font=("Segoe UI", 11, "bold"), text_color=WHITE,
                fg_color=DARK_GREEN, corner_radius=4, padx=8, pady=8,
            ).grid(row=0, column=column_index, sticky="ew", padx=2, pady=2)

        if not rows:
            ctk.CTkLabel(table_frame, text="No matching records found.",
                         font=("Segoe UI", 12), text_color=MUTED
                         ).grid(row=1, column=0, columnspan=len(columns), sticky="w", padx=12, pady=20)
            return

        for row_index, row_data in enumerate(rows, start=1):
            cells = []
            for column_index, value in enumerate(row_data):
                cell = ctk.CTkLabel(
                    table_frame,
                    text=self.display_value(table_name, columns[column_index], value),
                    font=("Segoe UI", 10), text_color=TEXT,
                    fg_color=row_stripe(row_index), corner_radius=3, padx=8, pady=8, anchor="w",
                )
                cell.grid(row=row_index, column=column_index, sticky="ew", padx=2, pady=2)
                cell.bind("<Button-1>",
                          lambda event, record=row_data, index=row_index: self.select_record(record, index))
                cell.configure(cursor="hand2")
                cells.append(cell)
            self.row_cells.append(cells)

    def select_record(self, record, row_index):
        """Remember the clicked row and highlight it."""
        self.selected_record = record
        for index, cells in enumerate(self.row_cells, start=1):
            color = LIGHT_GREEN if index == row_index else row_stripe(index)
            for cell in cells:
                cell.configure(fg_color=color)

    def export_module_csv(self, page_name, search_text=""):
        """Export the rows this login can see to a CSV file."""
        if page_name not in MODULES:
            return

        table_name, columns = MODULES[page_name]
        default_name = page_name.lower().replace(" ", "_") + "_report.csv"
        file_path = filedialog.asksaveasfilename(
            parent=self,
            title="Export " + page_name + " Report",
            defaultextension=".csv",
            initialfile=default_name,
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not file_path:
            return

        try:
            rows = self.filter_rows_for_role(page_name, columns, get_rows(table_name, columns))
            if search_text:
                rows = search_rows(rows, search_text)

            with open(file_path, "w", newline="", encoding="utf-8-sig") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([column.replace("_", " ").title() for column in columns])
                writer.writerows(rows)

            messagebox.showinfo("Export Successful",
                                str(len(rows)) + " record(s) exported to:\n" + file_path, parent=self)
        except (sqlite3.Error, OSError, csv.Error) as error:
            messagebox.showerror("Export Failed", "Could not export the report:\n" + str(error), parent=self)

    def delete_selected_record(self, page_name):
        """Delete the selected record after confirmation. Admin only."""
        if page_name not in MODULES:
            return
        if self.selected_record is None:
            messagebox.showwarning("Select a Record",
                                   "Click a record row in the table first, then click Delete Selected.")
            return

        table_name, columns = MODULES[page_name]
        record_id = self.selected_record[0]
        confirmed = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this record?\n\nRecord ID: " + str(record_id)
            + "\n\nThis action cannot be undone.",
        )
        if not confirmed:
            return

        connection = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute('DELETE FROM "' + table_name + '" WHERE "id" = ?', (record_id,))
            if cursor.rowcount == 0:
                messagebox.showwarning("Not Found", "This record no longer exists.")
            else:
                connection.commit()
                messagebox.showinfo("Success", "Record deleted successfully!")
        except sqlite3.Error as error:
            messagebox.showerror("Database Error", "Could not delete the record:\n" + str(error))
        finally:
            if connection is not None:
                connection.close()

        self.selected_record = None
        self.show_module(page_name)

    def open_update_form(self, page_name):
        """Open an edit form for the selected record. Admin only."""
        if page_name not in MODULES:
            return
        if self.selected_record is None:
            messagebox.showwarning("Select a Record",
                                   "Click a record row in the table first, then click Update Selected.")
            return

        table_name, columns = MODULES[page_name]
        record_values = dict(zip(columns, self.selected_record))
        record_id = record_values.get("id")

        form = ctk.CTkToplevel(self)
        form.title("Update Record - " + page_name)
        form.geometry("520x650")
        form.minsize(420, 400)
        form.configure(fg_color=BACKGROUND)
        form.transient(self)
        form.grab_set()

        ctk.CTkLabel(form, text="Update Record", font=("Segoe UI", 22, "bold"),
                     text_color=TEXT).pack(anchor="w", padx=24, pady=(20, 2))
        ctk.CTkLabel(form, text="Change the details and click Save Changes. The record ID cannot be changed.",
                     font=("Segoe UI", 11), text_color=MUTED).pack(anchor="w", padx=24, pady=(0, 12))

        form_fields = ctk.CTkScrollableFrame(form, fg_color=WHITE, corner_radius=10)
        form_fields.pack(fill="both", expand=True, padx=20, pady=(0, 12))
        entries = {}
        entry_maps = {}

        for column in columns:
            label = column.replace("_", " ").title() + (" (automatic)" if column == "id" else "")
            ctk.CTkLabel(form_fields, text=label, font=("Segoe UI", 11, "bold"),
                         text_color=TEXT).pack(anchor="w", padx=14, pady=(10, 3))
            value = record_values.get(column)
            options = get_reference_options(table_name, column)

            if column == "id":
                entry = ctk.CTkEntry(form_fields, height=34)
                entry.pack(fill="x", padx=14, pady=(0, 3))
                entry.insert(0, "" if value is None else str(value))
                entry.configure(state="disabled")
                entry_maps[column] = None
            elif options is not None:
                entry = ctk.CTkOptionMenu(form_fields, height=34, values=list(options.keys()))
                entry.pack(fill="x", padx=14, pady=(0, 3))
                selected_label = next((text for text, stored in options.items() if stored == str(value)), "")
                entry.set(selected_label or (list(options.keys())[0] if options else ""))
                entry_maps[column] = options
            else:
                entry = ctk.CTkEntry(form_fields, height=34)
                entry.pack(fill="x", padx=14, pady=(0, 3))
                if value is not None:
                    entry.insert(0, str(value))
                entry_maps[column] = None
            entries[column] = entry

        def get_field_value(column):
            displayed_value = entries[column].get()
            options = entry_maps.get(column)
            if options is not None:
                return options.get(displayed_value, "")
            return displayed_value

        def save_changes():
            update_columns = [column for column in columns if column != "id"]
            values = [get_field_value(column) for column in update_columns]
            empty = [column.replace("_", " ").title()
                     for column, value in zip(update_columns, values) if value == ""]
            if empty:
                messagebox.showwarning("Missing Information",
                                       "Please fill in all fields:\n" + ", ".join(empty), parent=form)
                return

            set_clause = ", ".join('"' + column + '" = ?' for column in update_columns)
            saved = False
            connection = None
            try:
                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute(
                    'UPDATE "' + table_name + '" SET ' + set_clause + ' WHERE "id" = ?',
                    values + [record_id],
                )
                if cursor.rowcount == 0:
                    messagebox.showwarning("Not Found", "This record no longer exists.", parent=form)
                else:
                    connection.commit()
                    saved = True
            except sqlite3.Error as error:
                messagebox.showerror("Database Error", "Could not update the record:\n" + str(error), parent=form)
            finally:
                if connection is not None:
                    connection.close()

            if saved:
                messagebox.showinfo("Success", "Record updated successfully!", parent=form)
                form.destroy()
                self.show_module(page_name)

        buttons = ctk.CTkFrame(form, fg_color="transparent")
        buttons.pack(fill="x", padx=20, pady=(0, 18))
        ctk.CTkButton(buttons, text="Cancel", width=100, height=38, fg_color="#DDE5E2",
                      hover_color="#C9D5D0", text_color=TEXT, command=form.destroy
                      ).pack(side="right", padx=(8, 0))
        ctk.CTkButton(buttons, text="Save Changes", width=130, height=38, fg_color=GREEN,
                      hover_color=DARK_GREEN, command=save_changes).pack(side="right")

    def open_add_form(self, page_name):
        """Open a form to add a record. Admin only."""
        if page_name not in MODULES:
            return

        table_name, columns = MODULES[page_name]
        form = ctk.CTkToplevel(self)
        form.title("Add Record - " + page_name)
        form.geometry("520x650")
        form.minsize(420, 400)
        form.configure(fg_color=BACKGROUND)
        form.transient(self)
        form.update_idletasks()
        form.lift()
        form.focus_force()
        form.grab_set()

        ctk.CTkLabel(form, text="Add New Record", font=("Segoe UI", 22, "bold"),
                     text_color=TEXT).pack(anchor="w", padx=24, pady=(20, 2))
        ctk.CTkLabel(form, text="Enter the details below and click Save Record.",
                     font=("Segoe UI", 11), text_color=MUTED).pack(anchor="w", padx=24, pady=(0, 12))

        form_fields = ctk.CTkScrollableFrame(form, fg_color=WHITE, corner_radius=10)
        form_fields.pack(fill="both", expand=True, padx=20, pady=(0, 12))
        entries = {}
        entry_maps = {}
        generated_id = generate_id(table_name)

        for column in columns:
            label = column.replace("_", " ").title() + (" (automatic)" if column == "id" else "")
            ctk.CTkLabel(form_fields, text=label, font=("Segoe UI", 11, "bold"),
                         text_color=TEXT).pack(anchor="w", padx=14, pady=(10, 3))
            options = get_reference_options(table_name, column)

            if column == "id":
                entry = ctk.CTkEntry(form_fields, height=34)
                entry.pack(fill="x", padx=14, pady=(0, 3))
                entry.insert(0, generated_id)
                entry.configure(state="disabled")
                entry_maps[column] = None
            elif options is not None:
                entry = ctk.CTkOptionMenu(form_fields, height=34,
                                          values=list(options.keys()) or ["No records available"])
                entry.pack(fill="x", padx=14, pady=(0, 3))
                entry.set(list(options.keys())[0] if options else "No records available")
                entry_maps[column] = options
            else:
                entry = ctk.CTkEntry(form_fields, height=34,
                                     placeholder_text="Enter " + column.replace("_", " "))
                entry.pack(fill="x", padx=14, pady=(0, 3))
                entry_maps[column] = None
            entries[column] = entry

        def get_field_value(column):
            displayed_value = entries[column].get()
            options = entry_maps.get(column)
            if options is not None:
                return options.get(displayed_value, "")
            return displayed_value

        def save_record():
            values = [get_field_value(column) for column in columns]
            empty = [column.replace("_", " ").title() for column, value in zip(columns, values) if value == ""]
            if empty:
                messagebox.showwarning("Missing Information",
                                       "Please fill in all fields:\n" + ", ".join(empty), parent=form)
                return

            column_text = ", ".join('"' + column + '"' for column in columns)
            placeholders = ", ".join("?" for _ in columns)
            saved = False
            connection = None
            try:
                connection = get_connection()
                connection.execute(
                    'INSERT INTO "' + table_name + '" (' + column_text + ") VALUES (" + placeholders + ")",
                    values,
                )
                connection.commit()
                saved = True
            except sqlite3.IntegrityError:
                messagebox.showerror("Duplicate Record",
                                     "This generated ID already exists. Close the form and try again.",
                                     parent=form)
            except sqlite3.Error as error:
                messagebox.showerror("Database Error", "Could not save the record:\n" + str(error), parent=form)
            finally:
                if connection is not None:
                    connection.close()

            if saved:
                messagebox.showinfo("Success", "Record added successfully!", parent=form)
                form.destroy()
                self.show_module(page_name)

        buttons = ctk.CTkFrame(form, fg_color="transparent")
        buttons.pack(fill="x", padx=20, pady=(0, 18))
        ctk.CTkButton(buttons, text="Cancel", width=100, height=38, fg_color="#DDE5E2",
                      hover_color="#C9D5D0", text_color=TEXT, command=form.destroy
                      ).pack(side="right", padx=(8, 0))
        ctk.CTkButton(buttons, text="Save Record", width=130, height=38, fg_color=GREEN,
                      hover_color=DARK_GREEN, command=save_record).pack(side="right")

    # ---------- Service provider actions ----------

    def get_provider_city(self):
        """Return the city ID saved on this service provider's profile."""
        connection = get_connection()
        row = connection.execute(
            "SELECT city_id FROM providers WHERE id = ?", (self.linked_id,)
        ).fetchone()
        connection.close()
        return row[0] if row else None

    def get_linked_request_ids(self):
        """Return the request IDs that already have a collection."""
        connection = get_connection()
        rows = connection.execute(
            'SELECT "request_id" FROM "waste_collections" WHERE "request_id" IS NOT NULL'
        ).fetchall()
        connection.close()
        return {row[0] for row in rows}

    def accept_selected_request(self):
        """Accept a pending request, or an accepted one whose collection was deleted."""
        if self.selected_record is None:
            messagebox.showwarning("Select a Request", "Click a request row first, then click Accept Request.")
            return

        columns = MODULES["Requests"][1]
        request_id = self.selected_record[columns.index("id")]
        waste_type = self.selected_record[columns.index("waste_type")]
        quantity = self.selected_record[columns.index("quantity")]
        city_id = self.selected_record[columns.index("city_id")]
        area_id = self.selected_record[columns.index("area_id")]
        preferred_date = self.selected_record[columns.index("preferred_date")]
        status = self.selected_record[columns.index("status")]
        if status not in ("Pending", "Accepted"):
            messagebox.showwarning("Not Available", "This request can't be accepted.")
            return

        collection_id = generate_id("waste_collections")
        connection = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            # Accept only if the request is Pending, or Accepted with no collection left.
            # The check and the update happen in one step, so two providers can't both win.
            cursor.execute(
                'UPDATE "requests" SET "status" = ? WHERE "id" = ? AND ("status" = ? OR '
                '("status" = ? AND "id" NOT IN (SELECT "request_id" FROM "waste_collections" '
                'WHERE "request_id" IS NOT NULL)))',
                ("Accepted", request_id, "Pending", "Accepted"),
            )
            if cursor.rowcount == 0:
                connection.rollback()
                messagebox.showwarning("Not Available", "Another provider already accepted this request.")
            else:
                cursor.execute(
                    'INSERT INTO "waste_collections" ("id", "waste_type", "quantity", "city_id", '
                    '"area_id", "provider_id", "collection_date", "status", "request_id") '
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (collection_id, waste_type, quantity, city_id, area_id,
                     self.linked_id, preferred_date, "Assigned", request_id),
                )
                connection.commit()
                messagebox.showinfo("Accepted", "Request " + request_id + " accepted. Collection "
                                    + collection_id + " was created.")
        except sqlite3.Error as error:
            if connection is not None:
                connection.rollback()
            messagebox.showerror("Database Error", "Could not accept the request:\n" + str(error))
        finally:
            if connection is not None:
                connection.close()

        self.selected_record = None
        self.show_module("Requests")

    def mark_selected_collected(self):
        """Mark an Assigned collection as Collected, and its request as Completed."""
        if self.selected_record is None:
            messagebox.showwarning("Select a Collection",
                                   "Click a collection row first, then click Mark Collected.")
            return

        columns = MODULES["Waste Collections"][1]
        collection_id = self.selected_record[columns.index("id")]
        status = self.selected_record[columns.index("status")]
        if status != "Assigned":
            messagebox.showwarning("Not Available",
                                   "Only collections with status Assigned can be marked Collected.")
            return

        connection = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            # The provider_id check means a provider can only change their own collections.
            cursor.execute(
                'SELECT "request_id" FROM "waste_collections" WHERE "id" = ? AND "provider_id" = ?',
                (collection_id, self.linked_id),
            )
            row = cursor.fetchone()
            if row is None:
                connection.rollback()
                messagebox.showwarning("Not Found", "This collection is no longer assigned to you.")
            else:
                request_id = row[0]
                cursor.execute(
                    'UPDATE "waste_collections" SET "status" = ? '
                    'WHERE "id" = ? AND "provider_id" = ? AND "status" = ?',
                    ("Collected", collection_id, self.linked_id, "Assigned"),
                )
                if request_id:  # Older collections have no linked request.
                    cursor.execute('UPDATE "requests" SET "status" = ? WHERE "id" = ?',
                                   ("Completed", request_id))
                connection.commit()
                messagebox.showinfo("Collected", "Collection " + collection_id + " is marked as Collected.")
        except sqlite3.Error as error:
            if connection is not None:
                connection.rollback()
            messagebox.showerror("Database Error", "Could not update the collection:\n" + str(error))
        finally:
            if connection is not None:
                connection.close()

        self.selected_record = None
        self.show_module("Waste Collections")

    # ---------- Customer actions ----------

    def open_new_request_form(self):
        """Customer creates a pickup request. Every field is a choice from a list."""
        connection = get_connection()
        city_rows = connection.execute(
            "SELECT id, name, state FROM cities ORDER BY state, name").fetchall()
        waste_rows = connection.execute("SELECT id, name FROM waste_types ORDER BY name").fetchall()
        connection.close()

        if not city_rows:
            messagebox.showwarning("No Cities", "The admin needs to add cities in City Management first.", parent=self)
            return
        if not waste_rows:
            messagebox.showwarning("No Waste Types", "The admin needs to add waste types first.", parent=self)
            return

        # state -> {city label -> city ID}. Labels are plain names, like "Amritsar".
        state_map = {}
        for city_id, name, state in city_rows:
            city_map = state_map.setdefault(state or "Other", {})
            label = name
            if label in city_map:
                label = name + " (" + str(city_id) + ")"
            city_map[label] = city_id

        # waste type label -> waste type ID
        waste_map = {}
        for waste_id, name in waste_rows:
            label = name
            if label in waste_map:
                label = name + " (" + str(waste_id) + ")"
            waste_map[label] = waste_id

        state_names = [SELECT_TEXT] + sorted(state_map.keys())
        waste_names = [SELECT_TEXT] + list(waste_map.keys())

        form = ctk.CTkToplevel(self)
        form.title("New Pickup Request")
        form.geometry("480x700")
        form.configure(fg_color=BACKGROUND)
        form.transient(self)
        form.update_idletasks()
        form.lift()
        form.focus_force()
        form.grab_set()

        ctk.CTkLabel(form, text="New Pickup Request", font=("Segoe UI", 22, "bold"),
                     text_color=TEXT).pack(anchor="w", padx=24, pady=(20, 2))
        ctk.CTkLabel(form, text="Pick from each list. Your request will be saved as Pending.",
                     font=("Segoe UI", 11), text_color=MUTED).pack(anchor="w", padx=24, pady=(0, 12))

        fields = ctk.CTkFrame(form, fg_color=WHITE, corner_radius=10)
        fields.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        def add_label(text):
            ctk.CTkLabel(fields, text=text, font=("Segoe UI", 11, "bold"),
                         text_color=TEXT).pack(anchor="w", padx=14, pady=(10, 3))

        def refresh_cities(chosen_state):
            """When the state changes, show only that state's cities."""
            options = [SELECT_TEXT] + list(state_map.get(chosen_state, {}).keys())
            city_box.configure(values=options)
            city_box.set(SELECT_TEXT)

        add_label("State")
        state_box = ctk.CTkOptionMenu(fields, height=34, values=state_names,
                                      command=lambda chosen: refresh_cities(chosen))
        state_box.set(SELECT_TEXT)
        state_box.pack(fill="x", padx=14)

        add_label("City")
        city_box = ctk.CTkOptionMenu(fields, height=34, values=[SELECT_TEXT])
        city_box.set(SELECT_TEXT)
        city_box.pack(fill="x", padx=14)

        add_label("Waste type")
        waste_box = ctk.CTkOptionMenu(fields, height=34, values=waste_names)
        waste_box.set(SELECT_TEXT)
        waste_box.pack(fill="x", padx=14)

        add_label("Quantity (kg)")
        quantity_entry = ctk.CTkEntry(fields, height=34, placeholder_text="e.g. 5")
        quantity_entry.pack(fill="x", padx=14)

        add_label("Preferred date (DD/MM/YYYY)")
        date_entry = ctk.CTkEntry(fields, height=34, placeholder_text="e.g. 05/11/2026")
        date_entry.pack(fill="x", padx=14)

        add_label("Area (optional)")
        area_entry = ctk.CTkEntry(fields, height=34, placeholder_text="e.g. Sector 14")
        area_entry.pack(fill="x", padx=14, pady=(0, 10))

        message = ctk.CTkLabel(form, text="", font=("Segoe UI", 11), text_color=RED, wraplength=430)
        message.pack(pady=(0, 6))

        def save_request():
            city_id = state_map.get(state_box.get(), {}).get(city_box.get())
            waste_id = waste_map.get(waste_box.get())
            quantity_text = quantity_entry.get().strip()
            date_text = date_entry.get().strip()
            area_text = area_entry.get().strip()

            error = None
            if city_id is None:
                error = "Choose a state and a city from the lists."
            elif waste_id is None:
                error = "Choose a waste type from the list."
            else:
                try:
                    if float(quantity_text) <= 0:
                        raise ValueError
                except ValueError:
                    error = "Quantity must be a number greater than 0."
            if error is None:
                try:
                    datetime.strptime(date_text, "%d/%m/%Y")
                except ValueError:
                    error = "Enter the date as DD/MM/YYYY, like 05/11/2026."
            if error:
                message.configure(text=error)
                return

            request_id = generate_id("requests")
            connection = None
            try:
                connection = get_connection()
                connection.execute(
                    'INSERT INTO "requests" ("id", "user_id", "waste_type", "quantity", '
                    '"city_id", "area_id", "preferred_date", "status") '
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (request_id, self.linked_id, waste_id, quantity_text,
                     city_id, area_text, date_text, "Pending"),
                )
                connection.commit()
                saved = True
            except sqlite3.Error as save_error:
                message.configure(text="Could not save the request: " + str(save_error))
                saved = False
            finally:
                if connection is not None:
                    connection.close()

            if saved:
                messagebox.showinfo("Request Sent",
                                    "Your request " + request_id + " was saved as Pending.", parent=form)
                form.destroy()
                self.show_module("Requests")

        buttons = ctk.CTkFrame(form, fg_color="transparent")
        buttons.pack(fill="x", padx=20, pady=(0, 18))
        ctk.CTkButton(buttons, text="Cancel", width=100, height=38, fg_color="#DDE5E2",
                      hover_color="#C9D5D0", text_color=TEXT, command=form.destroy
                      ).pack(side="right", padx=(8, 0))
        ctk.CTkButton(buttons, text="Send Request", width=140, height=38, fg_color=GREEN,
                      hover_color=DARK_GREEN, command=save_request).pack(side="right")

    def confirm_exit(self):
        if messagebox.askyesno("Exit BinGO", "Are you sure you want to close BinGO?"):
            self.destroy()