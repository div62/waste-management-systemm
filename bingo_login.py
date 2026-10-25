import getpass
import hashlib
import hmac
import re
import secrets
import sqlite3
import sys
import customtkinter as ctk
from gui import (
    BACKGROUND, BORDER, DARK_GREEN, GREEN, LIGHT_GREEN, MUTED, RED, TEXT,
    WHITE, BinGOApp, generate_id, get_connection)
ITERATIONS = 100_000
MIN_PASSWORD_LENGTH = 6
NOT_LISTED = "My city is not listed"
SELECT_STATE = "Select your state"
NOT_LISTED_STATE = "My state is not listed"

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"
SELECT_CITY = "Select your city"
USERNAME_PATTERN = r"[A-Za-z0-9_]{3,20}"  
PHONE_PATTERN = r"\d{10}"

CITY_DATA = [
    # Punjab
    ("Amritsar", "Punjab"),
    ("Barnala", "Punjab"),
    ("Bathinda", "Punjab"),
    ("Faridkot", "Punjab"),
    ("Fatehgarh Sahib", "Punjab"),
    ("Fazilka", "Punjab"),
    ("Firozpur", "Punjab"),
    ("Gurdaspur", "Punjab"),
    ("Hoshiarpur", "Punjab"),
    ("Jalandhar", "Punjab"),
    ("Kapurthala", "Punjab"),
    ("Ludhiana", "Punjab"),
    ("Malerkotla", "Punjab"),
    ("Mansa", "Punjab"),
    ("Moga", "Punjab"),
    ("Mohali", "Punjab"),
    ("Muktsar", "Punjab"),
    ("Nawanshahr", "Punjab"),
    ("Pathankot", "Punjab"),
    ("Patiala", "Punjab"),
    ("Rupnagar", "Punjab"),
    ("Sangrur", "Punjab"),
    ("Tarn Taran", "Punjab"),
    # Chandigarh
    ("Chandigarh", "Chandigarh"),
    # Haryana
    ("Ambala", "Haryana"),
    ("Bhiwani", "Haryana"),
    ("Faridabad", "Haryana"),
    ("Gurugram", "Haryana"),
    ("Hisar", "Haryana"),
    ("Jind", "Haryana"),
    ("Karnal", "Haryana"),
    ("Kurukshetra", "Haryana"),
    ("Panchkula", "Haryana"),
    ("Panipat", "Haryana"),
    ("Rewari", "Haryana"),
    ("Rohtak", "Haryana"),
    ("Sirsa", "Haryana"),
    ("Sonipat", "Haryana"),
    ("Yamunanagar", "Haryana"),
    # Himachal Pradesh
    ("Bilaspur", "Himachal Pradesh"),
    ("Chamba", "Himachal Pradesh"),
    ("Dharamshala", "Himachal Pradesh"),
    ("Hamirpur", "Himachal Pradesh"),
    ("Kullu", "Himachal Pradesh"),
    ("Mandi", "Himachal Pradesh"),
    ("Nahan", "Himachal Pradesh"),
    ("Shimla", "Himachal Pradesh"),
    ("Solan", "Himachal Pradesh"),
    ("Una", "Himachal Pradesh"),
]

PROFILE_FIELDS = {
    "Customer": [("name", "Full name"), ("phone", "Phone number")],
    "Service Provider": [
        ("name", "Provider name"),
        ("service_type", "Service type (e.g. Home pickup)"),
    ],
}

def ensure_accounts_table():
    """Create the accounts table if it doesn't exist yet."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            linked_id TEXT )""")
    conn.commit()
    conn.close()

def ensure_default_admin():
    """Create the default Admin login if it isn't saved yet, so there's always a way in."""
    conn = get_connection()
    exists = conn.execute(
        "SELECT 1 FROM accounts WHERE username = ?", (DEFAULT_ADMIN_USERNAME,)
    ).fetchone()
    conn.close()
    if not exists:
        create_admin_account(DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD)

def hash_password(password, salt=None):
    """Return 'salt$hash'. Pass the stored salt to check a password."""
    if salt is None:
        salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), ITERATIONS
    )
    return salt + "$" + digest.hex()

def login(username, password):
    """Return (role, linked_id) if the login is correct, otherwise None."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT password_hash, role, linked_id FROM accounts WHERE username = ?",
        (username,),
    )
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    stored_hash, role, linked_id = row
    salt = stored_hash.split("$", 1)[0]
    if hmac.compare_digest(hash_password(password, salt), stored_hash):
        return role, linked_id
    return None


def get_state_city_options():
    """Return {state: {city name: city ID}}, so the city list depends on the state."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, state FROM cities ORDER BY state, name")
    rows = cursor.fetchall()
    conn.close()
    state_map = {}
    for city_id, name, state in rows:
        city_map = state_map.setdefault(state or "Other", {})
        label = name
        if label in city_map:  # Same name twice in one state: add the ID to tell them apart.
            label = name + " (" + str(city_id) + ")"
        city_map[label] = city_id
    return state_map

def load_city_data():
    """Add every city in CITY_DATA that isn't already saved. Returns how many were added."""
    added = 0
    conn = get_connection()
    for city_name, state in CITY_DATA:
        exists = conn.execute(
            "SELECT 1 FROM cities WHERE name = ? AND state = ?",
            (city_name, state),
        ).fetchone()
        if exists:
            continue
        city_id = generate_id("cities")
        conn.execute(
            "INSERT INTO cities (id, name, state) VALUES (?, ?, ?)",
            (city_id, city_name, state),
        )
        conn.commit()
        added += 1
    conn.close()
    return added

def sign_up(role, name, detail, city_id, username, password):
    """Save the profile row and the login together. Returns (ok, message, linked_id)."""
    if role == "Customer":
        table = "users"
        profile_sql = "INSERT INTO users (id, name, phone, city) VALUES (?, ?, ?, ?)"
    else:
        table = "providers"
        profile_sql = (
            "INSERT INTO providers (id, name, service_type, city_id) "
            "VALUES (?, ?, ?, ?)"
        )

    linked_id = generate_id(table)
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM accounts WHERE username = ?", (username,))
        if cursor.fetchone():
            return False, "That username is already taken.", None
        cursor.execute(profile_sql, (linked_id, name, detail, city_id))
        cursor.execute(
            "INSERT INTO accounts (username, password_hash, role, linked_id) "
            "VALUES (?, ?, ?, ?)",
            (username, hash_password(password), role, linked_id),
        )
        conn.commit()
        return True, "Account created.", linked_id
    except sqlite3.Error as error:
        conn.rollback()
        return False, "Could not save the account: " + str(error), None
    finally:
        conn.close()

def create_admin_account(username, password):
    """Save the Admin login. Used only by 'python bingo_login.py setup'."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM accounts WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, "That username is already taken."
    cursor.execute(
        "INSERT INTO accounts (username, password_hash, role, linked_id) "
        "VALUES (?, ?, ?, ?)",
        (username, hash_password(password), "Admin", None),
    )
    conn.commit()
    conn.close()
    return True, "Admin account created."

def create_first_admin():
    """Terminal prompt used once to create the Admin account."""
    print("Create the first Admin account.")
    username = input("Admin username: ").strip()
    password = getpass.getpass("Admin password (typing stays hidden): ")
    if not username or not password:
        print("Username and password can't be empty.")
        return
    ok, message = create_admin_account(username, password)
    print(message)

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BinGO | Log In")
        self.resizable(False, False)
        self.configure(fg_color=BACKGROUND)
        self.logged_in = None  # Set to (role, linked_id) after a correct login.
        self.entries = {}

        self.card = ctk.CTkFrame(self, fg_color=WHITE, corner_radius=16,
                                 border_width=1, border_color=BORDER)
        self.card.pack(fill="both", expand=True, padx=30, pady=30)
        self.show_login_screen()

    def clear_card(self):
        for widget in self.card.winfo_children():
            widget.destroy()

    def show_login_screen(self, notice="", notice_color=RED, username=""):
        self.geometry("420x580")
        self.clear_card()
        ctk.CTkLabel(self.card, text="♻️ BinGO", font=("Segoe UI", 28, "bold"),
                     text_color=DARK_GREEN).pack(pady=(34, 2))
        ctk.CTkLabel(self.card, text="SMART WASTE MANAGEMENT",
                     font=("Segoe UI", 10, "bold"), text_color=GREEN
                     ).pack(pady=(0, 28))
        ctk.CTkLabel(self.card, text="Username", font=("Segoe UI", 11, "bold"),
                     text_color=TEXT).pack(anchor="w", padx=36)
        self.username_entry = ctk.CTkEntry(
            self.card, height=38, placeholder_text="Enter your username")
        self.username_entry.pack(fill="x", padx=36, pady=(4, 14))
        if username:
            self.username_entry.insert(0, username)
        ctk.CTkLabel(self.card, text="Password", font=("Segoe UI", 11, "bold"),
                     text_color=TEXT).pack(anchor="w", padx=36)
        self.password_entry = ctk.CTkEntry(
            self.card, height=38, show="•", placeholder_text="Enter your password")
        self.password_entry.pack(fill="x", padx=36, pady=(4, 0))

        self.message = ctk.CTkLabel(self.card, text=notice,
                                    font=("Segoe UI", 11),
                                    text_color=notice_color, wraplength=320)
        self.message.pack(pady=(12, 0))

        ctk.CTkButton(self.card, text="Log In", height=42, fg_color=GREEN,
                      hover_color=DARK_GREEN, command=self.try_login
                      ).pack(fill="x", padx=36, pady=(12, 0))
        ctk.CTkButton(self.card, text="New here? Create an account", height=36,
                      fg_color="transparent", text_color=DARK_GREEN,
                      hover_color=LIGHT_GREEN, command=self.show_signup_screen
                      ).pack(fill="x", padx=36, pady=(10, 0))

        self.username_entry.bind("<Return>", lambda event: self.try_login())
        self.password_entry.bind("<Return>", lambda event: self.try_login())
        self.username_entry.focus()

    def try_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        if not username or not password:
            self.message.configure(text="Enter your username and password.",
                                   text_color=RED)
            return

        try:
            result = login(username, password)
        except sqlite3.Error as error:
            self.message.configure(text="Database error: " + str(error),
                                   text_color=RED)
            return

        if result is None:
            self.message.configure(text="Wrong username or password.",
                                   text_color=RED)
            self.password_entry.delete(0, "end")
            return

        self.logged_in = result
        self.destroy()

    def show_signup_screen(self):
        self.geometry("440x780")
        self.clear_card()
        self.state_map = get_state_city_options()

        ctk.CTkLabel(self.card, text="Create an Account",
                     font=("Segoe UI", 22, "bold"), text_color=TEXT
                     ).pack(anchor="w", padx=30, pady=(26, 2))
        ctk.CTkLabel(self.card, text="Choose your role, then fill in your details.",
                     font=("Segoe UI", 11), text_color=MUTED
                     ).pack(anchor="w", padx=30, pady=(0, 12))

        if not self.state_map:
            ctk.CTkLabel(self.card,
                         text="The city list is empty. Ask the admin to load the cities first.",
                         font=("Segoe UI", 11, "bold"), text_color=RED,
                         wraplength=360).pack(anchor="w", padx=30, pady=(0, 8))

        self.role_choice = ctk.CTkSegmentedButton(
            self.card, values=list(PROFILE_FIELDS.keys()),
            command=self.build_profile_fields,
            selected_color=GREEN, selected_hover_color=DARK_GREEN)
        self.role_choice.pack(fill="x", padx=30)
        self.role_choice.set("Customer")

        self.profile_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.profile_frame.pack(fill="x", padx=30)
        self.build_profile_fields("Customer")

        account_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        account_frame.pack(fill="x", padx=30, pady=(6, 0))
        self.add_field(account_frame, "username", "Username")
        self.add_field(account_frame, "password",
                       "Password (at least 6 characters)", show="•")
        self.add_field(account_frame, "confirm", "Confirm password", show="•")
        self.entries["confirm"].bind("<Return>",
                                     lambda event: self.create_account_from_form())

        self.message = ctk.CTkLabel(self.card, text="", font=("Segoe UI", 11),
                                    text_color=RED, wraplength=350)
        self.message.pack(pady=(10, 0))

        buttons = ctk.CTkFrame(self.card, fg_color="transparent")
        buttons.pack(fill="x", padx=30, pady=(8, 0))
        ctk.CTkButton(buttons, text="Back", width=110, height=40,
                      fg_color="#DDE5E2", hover_color="#C9D5D0", text_color=TEXT,
                      command=self.show_login_screen).pack(side="left")
        ctk.CTkButton(buttons, text="Create Account", height=40,
                      fg_color=GREEN, hover_color=DARK_GREEN,
                      command=self.create_account_from_form
                      ).pack(side="right", fill="x", expand=True, padx=(10, 0))

    def build_profile_fields(self, role):
        """Rebuild the role-specific fields when the role changes."""
        for widget in self.profile_frame.winfo_children():
            widget.destroy()
        for key, label in PROFILE_FIELDS[role]:
            self.add_field(self.profile_frame, key, label)

        ctk.CTkLabel(self.profile_frame, text="State",
                     font=("Segoe UI", 11, "bold"), text_color=TEXT
                     ).pack(anchor="w", pady=(8, 3))
        state_values = ([SELECT_STATE] + sorted(self.state_map.keys())
                        + [NOT_LISTED_STATE])
        self.entries["state"] = ctk.CTkOptionMenu(
            self.profile_frame, height=38, values=state_values,
            command=self.refresh_city_menu)
        self.entries["state"].set(SELECT_STATE)
        self.entries["state"].pack(fill="x")

        ctk.CTkLabel(self.profile_frame, text="City",
                     font=("Segoe UI", 11, "bold"), text_color=TEXT
                     ).pack(anchor="w", pady=(8, 3))
        self.entries["city"] = ctk.CTkOptionMenu(
            self.profile_frame, height=38, values=[SELECT_CITY])
        self.entries["city"].set(SELECT_CITY)
        self.entries["city"].pack(fill="x")

    def refresh_city_menu(self, chosen_state):
        """When the state changes, show only that state's cities."""
        cities = list(self.state_map.get(chosen_state, {}).keys())
        values = [SELECT_CITY] + cities + ([NOT_LISTED] if cities else [])
        self.entries["city"].configure(values=values)
        self.entries["city"].set(SELECT_CITY)

    def add_field(self, parent, key, label, show=""):
        ctk.CTkLabel(parent, text=label, font=("Segoe UI", 11, "bold"),
                     text_color=TEXT).pack(anchor="w", pady=(8, 3))
        entry = ctk.CTkEntry(parent, height=38, show=show)
        entry.pack(fill="x")
        self.entries[key] = entry

    def create_account_from_form(self):
        role = self.role_choice.get()
        name = self.entries["name"].get().strip()
        detail_key = PROFILE_FIELDS[role][1][0]  # "phone" or "service_type"
        detail = self.entries[detail_key].get().strip()
        state_label = self.entries["state"].get()
        city_label = self.entries["city"].get()
        city_id = self.state_map.get(state_label, {}).get(city_label)
        username = self.entries["username"].get().strip()
        password = self.entries["password"].get()
        confirm = self.entries["confirm"].get()

        error = None
        if not (name and detail and username and password):
            error = "Fill in every field."
        elif state_label == NOT_LISTED_STATE or city_label == NOT_LISTED:
            error = "Sorry, BinGO is not yet available in your area."
        elif city_id is None:
            error = "Choose a state and a city from the lists."
        elif not re.fullmatch(USERNAME_PATTERN, username):
            error = "Username: 3 to 20 letters, numbers, or underscores. No spaces."
        elif role == "Customer" and not re.fullmatch(PHONE_PATTERN, detail):
            error = "Enter a 10-digit phone number."
        elif len(password) < MIN_PASSWORD_LENGTH:
            error = "Password must be at least " + str(MIN_PASSWORD_LENGTH) + " characters."
        elif password != confirm:
            error = "The two passwords don't match."

        if error:
            self.message.configure(text=error, text_color=RED)
            return

        ok, message, _ = sign_up(role, name, detail, city_id, username, password)
        if ok:
            self.show_login_screen(
                notice="Account created. Log in with your new username and password.",
                notice_color=GREEN, username=username)
        else:
            self.message.configure(text=message, text_color=RED)


if __name__ == "__main__":
    ensure_accounts_table()
    ensure_default_admin()
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "setup":
        create_first_admin()
    elif command == "load_cities":
        added = load_city_data()
        print("Added " + str(added) + " new cities.")
    else:
        login_window = LoginWindow()
        login_window.mainloop()
        if login_window.logged_in is not None:
            role, linked_id = login_window.logged_in
            BinGOApp(role=role, linked_id=linked_id).mainloop()