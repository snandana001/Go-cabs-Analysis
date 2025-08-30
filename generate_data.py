import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import execute_batch

# DB connection info
DB_PARAMS = {
    "host": "localhost",
    "port": 5432,
    "dbname": "superset_db",
    "user": "superset",
    "password": "superset"
}

# Setup Faker and seeds
fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# Parameters
NUM_USERS = 5000
NUM_DRIVERS = 1000
NUM_RIDES = 30000
START_DATE = datetime(2025, 3, 1)
END_DATE = datetime(2025, 8, 28)

campaigns = [
    {"channel": "Google Ads", "campaign": "Spring Boost", "spend": 5000, "cac": 25},
    {"channel": "Facebook", "campaign": "Summer Surge", "spend": 3000, "cac": 20},
    {"channel": "Instagram", "campaign": "Ride & Save", "spend": 2000, "cac": 15},
    {"channel": "Referral", "campaign": "Refer & Earn", "spend": 500, "cac": 5},
    {"channel": "Organic", "campaign": "N/A", "spend": 0, "cac": 0}
]

promo_codes = [
    {"promo_code": "WELCOME50", "discount_percent": 50},
    {"promo_code": "RIDENOW20", "discount_percent": 20},
    {"promo_code": "SUMMER10", "discount_percent": 10},
    {"promo_code": None, "discount_percent": 0}
]

def connect_db():
    conn = psycopg2.connect(**DB_PARAMS)
    conn.autocommit = True
    return conn

def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
          user_id SERIAL PRIMARY KEY,
          signup_date DATE NOT NULL,
          signup_channel VARCHAR(50),
          campaign_name VARCHAR(100),
          acquisition_cost NUMERIC(10, 2),
          promo_code_used VARCHAR(50),
          city VARCHAR(100)
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS drivers (
          driver_id SERIAL PRIMARY KEY,
          name VARCHAR(100),
          signup_date DATE,
          vehicle_type VARCHAR(50),
          rating NUMERIC(2,1),
          city VARCHAR(100)
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS rides (
          ride_id SERIAL PRIMARY KEY,
          user_id INTEGER REFERENCES users(user_id),
          driver_id INTEGER REFERENCES drivers(driver_id),
          request_time TIMESTAMP,
          pickup_time TIMESTAMP,
          dropoff_time TIMESTAMP,
          fare_amount NUMERIC(10,2),
          discount_amount NUMERIC(10,2),
          payment_method VARCHAR(50),
          ride_status VARCHAR(20),
          vehicle_type VARCHAR(50),
          origin_lat NUMERIC(9,6),
          origin_lng NUMERIC(9,6),
          destination_lat NUMERIC(9,6),
          destination_lng NUMERIC(9,6)
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS marketing_campaigns (
          channel VARCHAR(50),
          campaign VARCHAR(100),
          spend NUMERIC(12,2),
          cac NUMERIC(10,2)
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS promo_codes (
          promo_code VARCHAR(50) PRIMARY KEY,
          discount_percent INTEGER
        );
        """)

def generate_data():
    # Drivers
    drivers = []
    for i in range(NUM_DRIVERS):
        drivers.append((
            fake.name(),
            fake.date_between(START_DATE - timedelta(days=90), START_DATE),
            random.choice(["Economy", "Premium", "SUV"]),
            round(random.uniform(3.5, 5.0), 2),
            fake.city()
        ))
    drivers_df = pd.DataFrame(drivers, columns=["name", "signup_date", "vehicle_type", "rating", "city"])

    # Users
    users = []
    for _ in range(NUM_USERS):
        signup_date = fake.date_between(start_date=START_DATE, end_date=END_DATE)
        campaign = random.choices(campaigns, weights=[0.3, 0.25, 0.2, 0.15, 0.1])[0]
        promo = random.choices(promo_codes, weights=[0.2, 0.3, 0.2, 0.3])[0]
        users.append((
            signup_date,
            campaign["channel"],
            campaign["campaign"],
            campaign["cac"],
            promo["promo_code"],
            fake.city()
        ))
    users_df = pd.DataFrame(users, columns=["signup_date", "signup_channel", "campaign_name", "acquisition_cost", "promo_code_used", "city"])

    # Insert drivers and users first to get IDs
    return drivers_df, users_df

def insert_users_drivers(conn, drivers_df, users_df):
    with conn.cursor() as cur:
        # Insert drivers
        execute_batch(cur,
            "INSERT INTO drivers (name, signup_date, vehicle_type, rating, city) VALUES (%s, %s, %s, %s, %s) RETURNING driver_id",
            drivers_df.values.tolist()
        )
        # Get driver ids to assign later - simple way: assume serials from 1 to NUM_DRIVERS

        # Insert users
        execute_batch(cur,
            "INSERT INTO users (signup_date, signup_channel, campaign_name, acquisition_cost, promo_code_used, city) VALUES (%s, %s, %s, %s, %s, %s) RETURNING user_id",
            users_df.values.tolist()
        )
        # IDs from 1 to NUM_USERS

def insert_campaigns_promos(conn):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM marketing_campaigns")
        for c in campaigns:
            cur.execute(
                "INSERT INTO marketing_campaigns (channel, campaign, spend, cac) VALUES (%s, %s, %s, %s)",
                (c["channel"], c["campaign"], c["spend"], c["cac"])
            )
        cur.execute("DELETE FROM promo_codes")
        for p in promo_codes:
            if p["promo_code"] is not None:
                cur.execute(
                    "INSERT INTO promo_codes (promo_code, discount_percent) VALUES (%s, %s)",
                    (p["promo_code"], p["discount_percent"])
                )

def generate_and_insert_rides(conn):
    with conn.cursor() as cur:
        # We will assign random user_id and driver_id based on counts
        rides = []
        for _ in range(NUM_RIDES):
            user_id = random.randint(1, NUM_USERS)
            driver_id = random.randint(1, NUM_DRIVERS)
            # For simplicity we assume signup dates from users exist
            # In reality, better to query or cache users' signup dates
            request_date = fake.date_between(start_date=START_DATE, end_date=END_DATE)
            request_time = datetime.combine(request_date, datetime.min.time()) + timedelta(minutes=random.randint(300, 1320))
            pickup_time = request_time + timedelta(minutes=random.randint(1, 10))
            dropoff_time = pickup_time + timedelta(minutes=random.randint(5, 45))

            fare = round(np.random.exponential(10) + 5, 2)
            # Find promo_code_used and discount_pct for user
            # For simplicity, assume discount 0
            discount_amt = 0

            status = random.choices(["completed", "cancelled", "no-show"], weights=[0.85, 0.1, 0.05])[0]

            rides.append((
                user_id,
                driver_id,
                request_time,
                pickup_time if status == "completed" else None,
                dropoff_time if status == "completed" else None,
                fare if status == "completed" else 0,
                discount_amt if status == "completed" else 0,
                random.choice(["credit_card", "wallet", "cash"]),
                status,
                random.choice(["Economy", "Premium", "SUV"]),
                round(fake.latitude(), 6),
                round(fake.longitude(), 6),
                round(fake.latitude(), 6),
                round(fake.longitude(), 6)
            ))

        execute_batch(cur,
            """
            INSERT INTO rides (
                user_id, driver_id, request_time, pickup_time, dropoff_time,
                fare_amount, discount_amount, payment_method, ride_status,
                vehicle_type, origin_lat, origin_lng, destination_lat, destination_lng
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            rides
        )

def main():
    conn = connect_db()
    create_tables(conn)
    drivers_df, users_df = generate_data()
    insert_users_drivers(conn, drivers_df, users_df)
    insert_campaigns_promos(conn)
    generate_and_insert_rides(conn)
    print("✅ Data generated and loaded into Postgres successfully")
if __name__ == "__main__":
    main()
