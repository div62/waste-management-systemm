import os
import sqlite3
import csv
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

BACKGROUND = "#F5F7F8"
DARK_GREEN = "#087F68"
GREEN = "#079879"
LIGHT_GREEN = "#E5F5F0"
WHITE = "#FFFFFF"
TEXT = "#222831"
MUTED = "#7B858D"
BORDER = "#E3E9E7"
RED = "#D9534F"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "bingo.db")

MODULES = {
    "User Management": ("users", ["id", "name", "phone", "city"]),
    "Waste Management": ("waste_types", ["id", "name", "category", "description"]),
    "City Management": ("cities", ["id", "name", "state"]),
    "Service Providers": ("providers", ["id", "name", "service_type", "city_id"]),
    "Waste Collections": ("waste_collections", [
        "id", "waste_type", "quantity", "city_id", "area_id",
        "provider_id", "collection_date", "status"
    ]),
    "Scheduling": ("schedules", ["id", "collection_id", "date", "time", "provider_id", "status"]),
    "Requests": ("requests", [
        "id", "user_id", "waste_type", "quantity", "city_id",
        "area_id", "preferred_date", "status"
    ]),
    "Billing": ("bills", ["id", "user_id", "collection_id", "quantity", "rate", "total_amount", "payment_status"])
}
def get_connection():
    return sqlite3.connect(DB_PATH)
def get_count(table_name):
    """Return the number of records in a database table."""
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM " + table_name)
        count = cursor.fetchone()[0]
        connection.close()
        return count
    except sqlite3.Error:
        return 0
def get_rows(table_name, columns):
    """Read records for a module table."""
    connection = get_connection()
    cursor = connection.cursor()
    column_text = ", ".join('"' + column + '"' for column in columns)
    cursor.execute("SELECT " + column_text + " FROM \"" + table_name + "\"")
    rows = cursor.fetchall()
    connection.close()
    return rows
class BinGOApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BinGO | Smart Waste Management System")
        self.geometry("1250x760")
        self.minsize(1050, 650)
        self.configure(fg_color=BACKGROUND)
        self.current_page = "Dashboard"
        self.chart_canvas = None
        self.selected_record = None
        self.create_layout()
        self.show_dashboard()
        self.after(30000, self.auto_refresh_dashboard)

    def create_layout(self):
        self.sidebar = ctk.CTkFrame(self, width=235, corner_radius=0, fg_color=DARK_GREEN)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(
            self.sidebar, text="♻️ BinGO", font=("Segoe UI", 27, "bold"),
            text_color=WHITE
        ).pack(anchor="w", padx=22, pady=(25, 2))
        ctk.CTkLabel(
            self.sidebar, text="SMART WASTE MANAGEMENT", font=("Segoe UI", 9, "bold"),
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
            ("Billing", "🧾")
        ]

        for name, icon in menu_items:
            button = ctk.CTkButton(
                self.sidebar,
                text=icon + "    " + name,
                height=42,
                corner_radius=9,
                anchor="w",
                font=("Segoe UI", 12),
                fg_color="transparent",
                hover_color="#15977D",
                text_color=WHITE,
                command=lambda page=name: self.open_page(page)
            )
            button.pack(fill="x", padx=12, pady=3)
            self.nav_buttons[name] = button

        ctk.CTkFrame(self.sidebar, height=1, fg_color="#3C9B87").pack(fill="x", padx=18, pady=(20, 12))
        ctk.CTkButton(
            self.sidebar, text="✕    Exit Application", height=40,
            corner_radius=9, fg_color="#B84040", hover_color="#963333",
            text_color=WHITE, command=self.confirm_exit
        ).pack(side="bottom", fill="x", padx=12, pady=18)

        self.main_panel = ctk.CTkFrame(self, corner_radius=0, fg_color=BACKGROUND)
        self.main_panel.pack(side="right", fill="both", expand=True)

        self.topbar = ctk.CTkFrame(self.main_panel, height=58, corner_radius=0, fg_color=WHITE)
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)
        self.topbar_title = ctk.CTkLabel(
            self.topbar, text="BinGO Dashboard", font=("Segoe UI", 16, "bold"),
            text_color=TEXT
        )
        self.topbar_title.pack(side="left", padx=24)
        ctk.CTkLabel(
            self.topbar, text="●  System Ready", font=("Segoe UI", 11),
            text_color=GREEN
        ).pack(side="right", padx=24)

        self.page_area = ctk.CTkFrame(self.main_panel, fg_color=BACKGROUND, corner_radius=0)
        self.page_area.pack(fill="both", expand=True, padx=18, pady=15)

    def clear_page(self):
        for widget in self.page_area.winfo_children():
            widget.destroy()
        self.chart_canvas = None

    def set_active_button(self, page_name):
        for name, button in self.nav_buttons.items():
            if name == page_name:
                button.configure(fg_color="#15977D")
            else:
                button.configure(fg_color="transparent")

    def open_page(self, page_name):
        self.current_page = page_name
        self.topbar_title.configure(text="BinGO  /  " + page_name)
        self.set_active_button(page_name)
        if page_name == "Dashboard":
            self.show_dashboard()
        else:
            self.show_module(page_name)

    def auto_refresh_dashboard(self):
        """Refresh dashboard cards and charts periodically when Dashboard is open."""
        if not self.winfo_exists():
            return
        if self.current_page == "Dashboard":
            self.show_dashboard()
        self.after(30000, self.auto_refresh_dashboard)

    def create_heading(self, title, subtitle):
        ctk.CTkLabel(
            self.page_area, text=title, font=("Segoe UI", 26, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=8, pady=(3, 0))
        ctk.CTkLabel(
            self.page_area, text=subtitle, font=("Segoe UI", 12),
            text_color=MUTED
        ).pack(anchor="w", padx=8, pady=(2, 15))

    def show_dashboard(self):
        self.clear_page()
        self.current_page = "Dashboard"
        self.topbar_title.configure(text="BinGO  /  Dashboard")
        self.set_active_button("Dashboard")

        body = ctk.CTkScrollableFrame(self.page_area, fg_color=BACKGROUND, corner_radius=10)
        body.pack(fill="both", expand=True)

        dashboard_heading = ctk.CTkFrame(body, fg_color="transparent")
        dashboard_heading.pack(fill="x", padx=8, pady=(8, 0))
        ctk.CTkLabel(
            dashboard_heading, text="Dashboard & Analytics", font=("Segoe UI", 26, "bold"),
            text_color=TEXT
        ).pack(side="left", anchor="w")
        ctk.CTkButton(
            dashboard_heading, text="↻ Refresh Dashboard", width=150, height=32,
            fg_color=GREEN, hover_color=DARK_GREEN,
            command=self.show_dashboard
        ).pack(side="right", padx=(8, 0), pady=(2, 0))
        ctk.CTkLabel(
            body, text="Welcome back! Here is an overview of your waste management system.",
            font=("Segoe UI", 12), text_color=MUTED
        ).pack(anchor="w", padx=8, pady=(3, 15))

        stats = [
            ("Registered Users", "users", "People using BinGO"),
            ("Waste Types", "waste_types", "Types of waste"),
            ("Service Providers", "providers", "Available providers"),
            ("Waste Collections", "waste_collections", "Collection records"),
            ("Registered Cities", "cities", "Cities in the system"),
            ("Schedules", "schedules", "Planned collections"),
            ("Requests", "requests", "Collection requests"),
            ("Bills", "bills", "Billing records")
        ]
        cards = ctk.CTkFrame(body, fg_color="transparent")
        cards.pack(fill="x", padx=3, pady=(0, 14))

        for index, (title, table, description) in enumerate(stats):
            row = index // 4
            column = index % 4
            cards.grid_columnconfigure(column, weight=1, uniform="stats")
            card_color = GREEN if index == 0 else WHITE
            main_color = WHITE if index == 0 else TEXT
            sub_color = "#E4FFF6" if index == 0 else MUTED
            card = ctk.CTkFrame(
                cards, fg_color=card_color, corner_radius=12,
                border_width=0 if index == 0 else 1, border_color=BORDER
            )
            card.grid(row=row, column=column, sticky="nsew", padx=5, pady=5)
            ctk.CTkLabel(card, text=title, font=("Segoe UI", 11), text_color=main_color).pack(
                anchor="w", padx=13, pady=(12, 3)
            )
            ctk.CTkLabel(
                card, text=str(get_count(table)), font=("Segoe UI", 25, "bold"),
                text_color=main_color
            ).pack(anchor="w", padx=13, pady=(0, 2))
            ctk.CTkLabel(card, text=description, font=("Segoe UI", 9), text_color=sub_color).pack(
                anchor="w", padx=13, pady=(0, 12)
            )

        chart_section = ctk.CTkFrame(body, fg_color="transparent")
        chart_section.pack(fill="both", expand=True, padx=3, pady=(0, 10))
        chart_section.grid_columnconfigure(0, weight=3)
        chart_section.grid_columnconfigure(1, weight=2)

        bar_card = ctk.CTkFrame(chart_section, fg_color=WHITE, corner_radius=12, border_width=1, border_color=BORDER)
        bar_card.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        pie_card = ctk.CTkFrame(chart_section, fg_color=WHITE, corner_radius=12, border_width=1, border_color=BORDER)
        pie_card.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # A third graph spans the width below the first two charts.
        trend_card = ctk.CTkFrame(chart_section, fg_color=WHITE, corner_radius=12, border_width=1, border_color=BORDER)
        trend_card.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(bar_card, text="Waste Quantity by Type", font=("Segoe UI", 14, "bold"), text_color=TEXT).pack(
            anchor="w", padx=14, pady=(12, 0)
        )
        ctk.CTkLabel(pie_card, text="Collection Status", font=("Segoe UI", 14, "bold"), text_color=TEXT).pack(
            anchor="w", padx=14, pady=(12, 0)
        )
        ctk.CTkLabel(trend_card, text="Waste Collected by Date", font=("Segoe UI", 14, "bold"), text_color=TEXT).pack(
            anchor="w", padx=14, pady=(12, 0)
        )
        self.create_charts(bar_card, pie_card)
        self.create_collection_trend_chart(trend_card)

        if not os.path.exists(DB_PATH):
            ctk.CTkLabel(
                body, text="Database file not found yet. Run your existing BinGO program first to create bingo.db.",
                text_color=RED, font=("Segoe UI", 11)
            ).pack(anchor="w", padx=10, pady=8)

    def create_charts(self, bar_card, pie_card):
        figure = Figure(figsize=(6.3, 3.0), dpi=90, facecolor=WHITE)
        axis = figure.add_subplot(111)
        axis.set_facecolor(WHITE)
        labels = []
        quantities = []

        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT waste_type, quantity FROM waste_collections")
            rows = cursor.fetchall()
            connection.close()
            totals = {}
            for waste_type, quantity in rows:
                label = str(waste_type) if waste_type else "Unspecified"
                try:
                    amount = float(quantity)
                except (TypeError, ValueError):
                    amount = 0
                totals[label] = totals.get(label, 0) + amount
            labels = list(totals.keys())
            quantities = list(totals.values())
        except sqlite3.Error:
            labels = []
            quantities = []

        if labels:
            axis.bar(labels, quantities, color=GREEN)
            axis.set_ylabel("Quantity (kg)", fontsize=9)
            axis.tick_params(axis="x", labelrotation=25, labelsize=8)
            axis.tick_params(axis="y", labelsize=8)
            axis.grid(axis="y", alpha=0.2)
            axis.set_axisbelow(True)
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
            cursor = connection.cursor()
            cursor.execute("SELECT status, COUNT(*) FROM waste_collections GROUP BY status")
            status_rows = cursor.fetchall()
            connection.close()
        except sqlite3.Error:
            status_rows = []

        status_labels = [str(row[0]) if row[0] else "Unspecified" for row in status_rows]
        status_counts = [row[1] for row in status_rows]
        if status_counts and sum(status_counts) > 0:
            pie_axis.pie(
                status_counts, labels=status_labels, autopct="%1.0f%%",
                startangle=90, textprops={"fontsize": 8}
            )
        else:
            pie_axis.text(0.5, 0.5, "No status data yet", ha="center", va="center", color=MUTED)
            pie_axis.set_xticks([])
            pie_axis.set_yticks([])
        pie_figure.tight_layout(pad=1)
        pie_canvas = FigureCanvasTkAgg(pie_figure, master=pie_card)
        pie_canvas.draw()
        pie_canvas.get_tk_widget().pack(fill="both", expand=True, padx=4, pady=4)


    def create_collection_trend_chart(self, trend_card):
        """Draw a line graph showing total waste collected on each date."""
        figure = Figure(figsize=(8.0, 2.7), dpi=90, facecolor=WHITE)
        axis = figure.add_subplot(111)
        axis.set_facecolor(WHITE)

        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT collection_date, quantity FROM waste_collections")
            rows = cursor.fetchall()
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

        # Sort dates in DD/MM/YYYY format when possible; keep other labels safe.
        from datetime import datetime
        def date_sort_key(label):
            try:
                return datetime.strptime(label, "%d/%m/%Y")
            except ValueError:
                try:
                    return datetime.strptime(label, "%Y-%m-%d")
                except ValueError:
                    return datetime.max

        dates = sorted(daily_totals.keys(), key=date_sort_key)
        amounts = [daily_totals[date_label] for date_label in dates]

        if dates:
            axis.plot(dates, amounts, marker="o", linewidth=2, color=GREEN)
            axis.set_ylabel("Quantity (kg)", fontsize=9)
            axis.tick_params(axis="x", labelrotation=25, labelsize=8)
            axis.tick_params(axis="y", labelsize=8)
            axis.grid(axis="y", alpha=0.2)
            axis.set_axisbelow(True)
        else:
            axis.text(0.5, 0.5, "No collection date data yet", ha="center", va="center", color=MUTED)
            axis.set_xticks([])
            axis.set_yticks([])

        figure.tight_layout(pad=2)
        canvas = FigureCanvasTkAgg(figure, master=trend_card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=4)

    def show_module(self, page_name, search_text=""):
        self.clear_page()
        self.create_heading(page_name, "View records saved in your BinGO database.")

        if page_name not in MODULES:
            ctk.CTkLabel(self.page_area, text="This section is not available yet.", text_color=MUTED).pack(pady=20)
            return

        table_name, columns = MODULES[page_name]
        self.selected_record = None
        toolbar = ctk.CTkFrame(self.page_area, fg_color="transparent")
        toolbar.pack(fill="x", padx=8, pady=(0, 10))
        ctk.CTkLabel(
            toolbar, text="Total records: " + str(get_count(table_name)),
            font=("Segoe UI", 12, "bold"), text_color=TEXT
        ).pack(side="left", padx=(0, 10))
        search_entry = ctk.CTkEntry(
            toolbar, width=190, height=32, placeholder_text="Search records..."
        )
        search_entry.pack(side="left", padx=(0, 6))
        if search_text:
            search_entry.insert(0, search_text)
        ctk.CTkButton(
            toolbar, text="🔍 Search", width=90, height=32,
            fg_color=DARK_GREEN, hover_color=GREEN,
            command=lambda: self.show_module(page_name, search_entry.get())
        ).pack(side="left", padx=(0, 6))
        ctk.CTkButton(
            toolbar, text="Clear", width=60, height=32,
            fg_color="#DDE5E2", hover_color="#C9D5D0", text_color=TEXT,
            command=lambda: self.show_module(page_name)
        ).pack(side="left")
        ctk.CTkButton(
            toolbar, text="🔄️ Refresh", width=100, height=32,
            fg_color=GREEN, hover_color=DARK_GREEN,
            command=lambda: self.show_module(page_name, search_entry.get())
        ).pack(side="right", padx=(8, 0))
        ctk.CTkButton(
            toolbar, text="⏬ Export CSV", width=110, height=32,
            fg_color="#2878A5", hover_color="#205F83",
            command=lambda: self.export_module_csv(page_name, search_entry.get())
        ).pack(side="right", padx=(8, 0))
        ctk.CTkButton(
            toolbar, text="🚮 Delete Selected", width=135, height=32,
            fg_color="#C94C4C", hover_color="#A93636",
            command=lambda: self.delete_selected_record(page_name)
        ).pack(side="right", padx=(8, 0))
        ctk.CTkButton(
            toolbar, text="🖋️ Update Selected", width=135, height=32,
            fg_color="#D98C24", hover_color="#B87518",
            command=lambda: self.open_update_form(page_name)
        ).pack(side="right", padx=(8, 0))
        ctk.CTkButton(
            toolbar, text=" ➕ Add Record", width=120, height=32,
            fg_color=DARK_GREEN, hover_color=GREEN,
            command=lambda: self.open_add_form(page_name)
        ).pack(side="right")

        table_frame = ctk.CTkScrollableFrame(
            self.page_area, fg_color=WHITE, corner_radius=10,
            border_width=1, border_color=BORDER
        )
        table_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        try:
            rows = get_rows(table_name, columns)
            # Search every displayed column without changing the saved database data.
            if search_text:
                search_value = search_text.lower()
                rows = [
                    row for row in rows
                    if any(search_value in str(value).lower() for value in row if value is not None)
                ]
        except sqlite3.Error as error:
            ctk.CTkLabel(
                table_frame,
                text="Could not load this table. Make sure your BinGO database has been created.\n" + str(error),
                text_color=RED, justify="left"
            ).pack(anchor="w", padx=12, pady=15)
            return

        for column_index, column_name in enumerate(columns):
            table_frame.grid_columnconfigure(column_index, weight=1, uniform="table")
            ctk.CTkLabel(
                table_frame, text=column_name.replace("_", " ").title(),
                font=("Segoe UI", 11, "bold"), text_color=WHITE,
                fg_color=DARK_GREEN, corner_radius=4, padx=8, pady=8
            ).grid(row=0, column=column_index, sticky="ew", padx=2, pady=2)

        if not rows:
            ctk.CTkLabel(
                table_frame, text="No matching records found.",
                font=("Segoe UI", 12), text_color=MUTED
            ).grid(row=1, column=0, columnspan=len(columns), sticky="w", padx=12, pady=20)
            return

        for row_index, row_data in enumerate(rows, start=1):
            for column_index, value in enumerate(row_data):
                cell = ctk.CTkLabel(
                    table_frame, text="" if value is None else str(value),
                    font=("Segoe UI", 10), text_color=TEXT,
                    fg_color="#F6FAF8" if row_index % 2 == 1 else WHITE,
                    corner_radius=3, padx=8, pady=8, anchor="w"
                )
                cell.grid(row=row_index, column=column_index, sticky="ew", padx=2, pady=2)
                cell.bind(
                    "<Button-1>",
                    lambda event, record=row_data, row=row_index: self.select_record(record, row, table_frame, columns)
                )
                cell.configure(cursor="hand2")

    def export_module_csv(self, page_name, search_text=""):
        """Export the selected module's records to a CSV file."""
        if page_name not in MODULES:
            return

        table_name, columns = MODULES[page_name]
        default_name = page_name.lower().replace(" ", "_") + "_report.csv"
        file_path = filedialog.asksaveasfilename(
            parent=self,
            title="Export " + page_name + " Report",
            defaultextension=".csv",
            initialfile=default_name,
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not file_path:
            return

        connection = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            column_text = ", ".join('"' + column + '"' for column in columns)
            cursor.execute("SELECT " + column_text + " FROM \"" + table_name + "\"")
            rows = cursor.fetchall()

            # If a search is active, export only the matching displayed records.
            if search_text:
                search_value = search_text.lower()
                rows = [
                    row for row in rows
                    if any(search_value in str(value).lower() for value in row if value is not None)
                ]

            with open(file_path, "w", newline="", encoding="utf-8-sig") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([column.replace("_", " ").title() for column in columns])
                writer.writerows(rows)

            messagebox.showinfo(
                "Export Successful",
                str(len(rows)) + " record(s) exported to:\n" + file_path,
                parent=self
            )
        except (sqlite3.Error, OSError, csv.Error) as error:
            messagebox.showerror(
                "Export Failed", "Could not export the report:\n" + str(error), parent=self
            )
        finally:
            if connection is not None:
                connection.close()

    def select_record(self, record, row_index, table_frame, columns):
        """Remember the row clicked by the user and highlight it."""
        self.selected_record = record
        for widget in table_frame.winfo_children():
            info = widget.grid_info()
            if str(info.get("row")) != "0":
                widget.configure(fg_color=WHITE if int(info.get("row", 0)) % 2 == 0 else "#F6FAF8")
        for widget in table_frame.winfo_children():
            info = widget.grid_info()
            if str(info.get("row")) == str(row_index):
                widget.configure(fg_color=LIGHT_GREEN)

    def delete_selected_record(self, page_name):
        """Delete the selected database record after confirmation."""
        if page_name not in MODULES:
            return

        if self.selected_record is None:
            messagebox.showwarning(
                "Select a Record",
                "Click a record row in the table first, then click Delete Selected."
            )
            return

        table_name, columns = MODULES[page_name]
        record_id = self.selected_record[0]

        confirmed = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this record?\n\nRecord ID: " + str(record_id) +
            "\n\nThis action cannot be undone."
        )
        if not confirmed:
            return

        connection = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM \"" + table_name + "\" WHERE \"id\" = ?",
                (record_id,)
            )
            if cursor.rowcount == 0:
                messagebox.showwarning("Not Found", "This record no longer exists.")
            else:
                connection.commit()
                messagebox.showinfo("Success", "Record deleted successfully!")
        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error", "Could not delete the record:\n" + str(error)
            )
        finally:
            if connection is not None:
                connection.close()

        self.selected_record = None
        self.show_module(page_name)

    def open_update_form(self, page_name):
        """Open an edit form for the row selected in the records table."""
        if page_name not in MODULES:
            return
        if self.selected_record is None:
            messagebox.showwarning(
                "Select a Record", "Click a record row in the table first, then click Update Selected."
            )
            return

        table_name, columns = MODULES[page_name]
        original_record = self.selected_record
        record_values = dict(zip(columns, original_record))
        record_id = record_values.get("id")

        form = ctk.CTkToplevel(self)
        form.title("Update Record - " + page_name)
        form.geometry("520x650")
        form.minsize(420, 400)
        form.configure(fg_color=BACKGROUND)
        form.transient(self)
        form.grab_set()

        ctk.CTkLabel(
            form, text="Update Record", font=("Segoe UI", 22, "bold"), text_color=TEXT
        ).pack(anchor="w", padx=24, pady=(20, 2))
        ctk.CTkLabel(
            form, text="Change the details and click Save Changes. The record ID cannot be changed.",
            font=("Segoe UI", 11), text_color=MUTED
        ).pack(anchor="w", padx=24, pady=(0, 12))

        form_fields = ctk.CTkScrollableFrame(form, fg_color=WHITE, corner_radius=10)
        form_fields.pack(fill="both", expand=True, padx=20, pady=(0, 12))
        entries = {}

        for column in columns:
            ctk.CTkLabel(
                form_fields, text=column.replace("_", " ").title(),
                font=("Segoe UI", 11, "bold"), text_color=TEXT
            ).pack(anchor="w", padx=14, pady=(10, 3))
            entry = ctk.CTkEntry(form_fields, height=34)
            entry.pack(fill="x", padx=14, pady=(0, 3))
            value = record_values.get(column)
            if value is not None:
                entry.insert(0, str(value))
            if column == "id":
                entry.configure(state="disabled")
            entries[column] = entry

        def save_changes():
            update_columns = [column for column in columns if column != "id"]
            values = [entries[column].get() for column in update_columns]
            empty_fields = [column.replace("_", " ").title() for column, value in zip(update_columns, values) if value == ""]
            if empty_fields:
                messagebox.showwarning(
                    "Missing Information", "Please fill in all fields:\n" + ", ".join(empty_fields), parent=form
                )
                return

            set_clause = ", ".join('"' + column + '" = ?' for column in update_columns)
            try:
                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute(
                    "UPDATE \"" + table_name + "\" SET " + set_clause + " WHERE \"id\" = ?",
                    values + [record_id]
                )
                if cursor.rowcount == 0:
                    connection.close()
                    messagebox.showwarning("Not Found", "This record no longer exists.", parent=form)
                    form.destroy()
                    self.show_module(page_name)
                    return
                connection.commit()
                connection.close()
                messagebox.showinfo("Success", "Record updated successfully!", parent=form)
                form.destroy()
                self.show_module(page_name)
            except sqlite3.Error as error:
                try:
                    connection.close()
                except Exception:
                    pass
                messagebox.showerror("Database Error", "Could not update the record:\n" + str(error), parent=form)

        buttons = ctk.CTkFrame(form, fg_color="transparent")
        buttons.pack(fill="x", padx=20, pady=(0, 18))
        ctk.CTkButton(
            buttons, text="Cancel", width=100, height=38,
            fg_color="#DDE5E2", hover_color="#C9D5D0", text_color=TEXT,
            command=form.destroy
        ).pack(side="right", padx=(8, 0))
        ctk.CTkButton(
            buttons, text="Save Changes", width=130, height=38,
            fg_color=GREEN, hover_color=DARK_GREEN, command=save_changes
        ).pack(side="right")

    def open_add_form(self, page_name):
        """Open a simple form to insert a record into the selected database table."""
        if page_name not in MODULES:
            return

        table_name, columns = MODULES[page_name]
        form = ctk.CTkToplevel(self)
        form.title("Add Record - " + page_name)
        form.geometry("520x650")
        form.minsize(420, 400)
        form.configure(fg_color=BACKGROUND)
        form.transient(self)
        form.grab_set()

        ctk.CTkLabel(
            form, text="Add New Record", font=("Segoe UI", 22, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=24, pady=(20, 2))
        ctk.CTkLabel(
            form, text="Enter the details below and click Save Record.",
            font=("Segoe UI", 11), text_color=MUTED
        ).pack(anchor="w", padx=24, pady=(0, 12))

        form_fields = ctk.CTkScrollableFrame(form, fg_color=WHITE, corner_radius=10)
        form_fields.pack(fill="both", expand=True, padx=20, pady=(0, 12))
        entries = {}

        for column in columns:
            ctk.CTkLabel(
                form_fields, text=column.replace("_", " ").title(),
                font=("Segoe UI", 11, "bold"), text_color=TEXT
            ).pack(anchor="w", padx=14, pady=(10, 3))
            entry = ctk.CTkEntry(
                form_fields, height=34, placeholder_text="Enter " + column.replace("_", " ")
            )
            entry.pack(fill="x", padx=14, pady=(0, 3))
            entries[column] = entry

        def save_record():
            values = [entries[column].get() for column in columns]
            empty_fields = []
            for column, value in zip(columns, values):
                if value == "":
                    empty_fields.append(column.replace("_", " ").title())

            if empty_fields:
                messagebox.showwarning(
                    "Missing Information",
                    "Please fill in all fields:\n" + ", ".join(empty_fields),
                    parent=form
                )
                return

            column_text = ", ".join('"' + column + '"' for column in columns)
            placeholders = ", ".join("?" for column in columns)
            try:
                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO \"" + table_name + "\" (" + column_text + ") VALUES (" + placeholders + ")",
                    values
                )
                connection.commit()
                connection.close()
                messagebox.showinfo("Success", "Record added successfully!", parent=form)
                form.destroy()
                self.show_module(page_name)
            except sqlite3.IntegrityError:
                try:
                    connection.close()
                except Exception:
                    pass
                messagebox.showerror(
                    "Duplicate Record", "This ID may already exist. Please enter a unique ID.",
                    parent=form
                )
            except sqlite3.Error as error:
                try:
                    connection.close()
                except Exception:
                    pass
                messagebox.showerror(
                    "Database Error", "Could not save the record:\n" + str(error), parent=form
                )

        buttons = ctk.CTkFrame(form, fg_color="transparent")
        buttons.pack(fill="x", padx=20, pady=(0, 18))
        ctk.CTkButton(
            buttons, text="Cancel", width=100, height=38,
            fg_color="#DDE5E2", hover_color="#C9D5D0", text_color=TEXT,
            command=form.destroy
        ).pack(side="right", padx=(8, 0))
        ctk.CTkButton(
            buttons, text="Save Record", width=130, height=38,
            fg_color=GREEN, hover_color=DARK_GREEN, command=save_record
        ).pack(side="right")

    def confirm_exit(self):
        if messagebox.askyesno("Exit BinGO", "Are you sure you want to close BinGO?"):
            self.destroy()

if __name__ == "__main__":
    app = BinGOApp()
    app.mainloop()
