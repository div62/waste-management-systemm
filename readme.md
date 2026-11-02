# BinGO - Smart Waste Management System

BinGO is a desktop app for keeping track of waste collection. Customers ask for a pickup, service providers take the requests in their city, and the admin can see and manage everything from one place. It's written in Python with a CustomTkinter interface and keeps all its data in a local SQLite file, so there's no server to set up.

I started this as a college project and kept adding to it. It's not finished yet, but the main parts work: login and sign-up, the dashboard, the record pages, and the request flow.

## Features

**Login and roles**

There are three kinds of accounts, and each one sees a different version of the app:

- **Admin** can see and change everything.
- **Customer** can ask for pickups and see their own requests and bills.
- **Service Provider** handles the collections in their city.

Customers and providers sign up from the login screen. They pick their state and city from a list. If your city isn't in the list, the app tells you BinGO isn't available there yet. Usernames need 3 to 20 letters, numbers or underscores, passwords need at least 6 characters, and customers enter a 10-digit phone number. Passwords are never stored as plain text. They're hashed with PBKDF2-HMAC-SHA256 and a random salt.

**Dashboard**

The dashboard shows a count card for each section, and clicking a card opens that section. The admin also gets three charts: waste quantity by type, collection status, and waste collected by date. The dashboard refreshes itself every 30 seconds.

Customers and providers only see counts for their own records.

**Records**

Every section has a table with:

- search across the visible columns
- a refresh button
- Export CSV, which saves the rows you can currently see (search and role filters included)

Click a row to select it. Admins can then update or delete it. Linked fields are dropdowns that show names instead of raw IDs, so you pick something like `Amritsar (C001)` and not a bare code.

IDs are generated automatically with a prefix for each table: U for users, W for waste types, C for cities, P for providers, WC for waste collections, S for schedules, R for requests and B for bills. So the fourth request is R004.

**Requests and collections**

- Customers create a new request with the waste type, quantity, city, area and preferred date. It starts as Pending.
- Providers see the pending requests in their city and can accept them.
- Providers see their own collections and schedules, and can mark a collection as collected.

**Terminal version**

`function.py` has the same add, view, search, update and delete operations for the console. It works on the same `bingo.db`.

## Tech stack

- Python 3
- CustomTkinter for the GUI
- Matplotlib for the charts
- SQLite, through Python's built-in `sqlite3` module

The interface uses the Segoe UI font, so it looks best on Windows.

## Project structure

```
waste-management-systemm/
├── bingo_login.py   # start here: login, sign-up, admin setup
├── gui.py           # main window, dashboard, charts, tables and forms
├── database.py      # creates the tables in bingo.db
├── function.py      # terminal version of the record operations
└── bingo.db         # SQLite database
```

## Database

The database has nine tables:

| Table | ID prefix | What it holds |
|---|---|---|
| `users` | U | Customer profiles (name, phone, city) |
| `providers` | P | Service provider profiles (name, service type, city) |
| `cities` | C | Cities and the states they belong to |
| `waste_types` | W | Types of waste and their categories |
| `waste_collections` | WC | Collection records (type, quantity, date, status) |
| `schedules` | S | Planned collection dates and times |
| `requests` | R | Pickup requests from customers |
| `bills` | B | Billing records (quantity, rate, total, payment status) |
| `accounts` | none | Usernames, password hashes and roles |

Customers are stored in `users` and service providers in `providers`. The `accounts` table holds the usernames and password hashes, and each login points to its profile row through `linked_id`. Admin accounts don't have a linked row. Dates are stored as text in DD/MM/YYYY format.

## Getting started

You need Python 3.8 or newer. Install the two libraries:

```
pip install customtkinter matplotlib
```

Then, from the project folder, run these in order:

```
python database.py                  # creates the tables
python bingo_login.py load_cities   # adds the cities for Punjab, Chandigarh, Haryana and Himachal Pradesh
python bingo_login.py               # opens the app
```

`load_cities` only adds cities that aren't already in the database, so it's safe to run again.

On the first launch, the app creates a default Admin account so you can log in. The username and password are set near the top of `bingo_login.py`. Change them before you use the app for anything real. If you'd rather create your own Admin from the terminal, run `python bingo_login.py setup`.

## How it works for each role

| Role | Sidebar pages | What they can do |
|---|---|---|
| Admin | Everything | Add, update and delete any record. Sees all the charts. |
| Customer | Dashboard, Requests, Billing | Create requests. See their own requests and bills. |
| Service Provider | Dashboard, Requests, Waste Collections, Scheduling | Accept pending requests in their city. See their own collections and schedules, and mark collections as collected. |

## Status

This is still a work in progress. Things I want to fix or add next:

- There's no way to change a password yet.
- Dates and statuses are typed in as free text, so a typo gets saved as it is. Dropdowns and a date picker would help.
- Some of the rules are in `gui.py` and some are in `function.py`, so the terminal and the GUI don't always behave the same way.
- There are no automated tests yet.

## Ideas for later

These are things I'd like to build when I get the time. Some are small and some are bigger.

- We can let customers pay their bills online and download a receipt as a PDF.
- We can send an SMS or email when a provider accepts a request, and a reminder the day before the pickup.
- We can add route planning, so a provider sees all their pickups in an area in the order they should visit them.
- We can connect smart bins with a fill-level sensor, so a request gets created automatically when a bin is nearly full. That's the "smart" part of the name, and I'd love to try it.
- We can add a "missed pickup" button for customers, which sends a note to the provider and the admin.
- We can add a rating system, so customers can rate a provider after a collection and the admin can see who's doing a good job.
- We can generate monthly bills automatically from the collections that were marked as collected.
- We can add a map view that shows where the pending requests are in each city.
- We can lock an account for a few minutes after too many wrong passwords.
- We can keep an activity log, so the admin can see who added, changed or deleted a record and when.
- We can add a backup button that copies `bingo.db` to a safe folder with the date in the file name.
- We can build a web version or a phone app, so customers don't have to install anything.

## Author

Built by Divyansha Sharma [div62](https://github.com/div62) and Eshmeet kaur [Eshmeetk](https://github.com/eshmeetk) as a college project.