import os
import sqlite3
def connect_db():
    conn = sqlite3.connect("bingo.db")
    return conn

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT,
            phone TEXT,
            city TEXT) """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS waste_types (
            id TEXT PRIMARY KEY,
            name TEXT,
            category TEXT,
            description TEXT  )""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cities (
            id TEXT PRIMARY KEY,
            name TEXT,
            state TEXT ) """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS providers (
            id TEXT PRIMARY KEY,
            name TEXT,
            service_type TEXT,
            city_id TEXT )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS waste_collections (
            id TEXT PRIMARY KEY,
            waste_type TEXT,
            quantity TEXT,
            city_id TEXT,
            area_id TEXT,
            provider_id TEXT,
            collection_date TEXT,
            status TEXT )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedules (
            id TEXT PRIMARY KEY,
            collection_id TEXT,
            date TEXT,
            time TEXT,
            provider_id TEXT,
            status TEXT )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            waste_type TEXT,
            quantity TEXT,
            city_id TEXT,
            area_id TEXT,
            preferred_date TEXT,
            status TEXT ) """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            collection_id TEXT,
            quantity REAL,
            rate REAL,
            total_amount REAL,
            payment_status TEXT)""")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("BinGO database created successfully!")
