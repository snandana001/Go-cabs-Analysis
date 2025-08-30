<<<<<<< HEAD
Ride Sharing Revenue & Discount Analysis
Project Overview

This project analyzes a ride-sharing platform's data to understand the impact of promotional discounts on revenue, ride frequency, and customer behavior. Data was generated using Python, stored in a PostgreSQL database, and visualized using Apache Superset. The primary focus was on identifying trends in Customer Lifetime Value (CLV), Customer Acquisition Cost (CAC), discount schemes, and vehicle popularity.

Table of Contents

Project Workflow

Data Generation

SQL Queries

Data Visualizations

How to Run the Project

License

Project Workflow

The project consists of three main parts:

Data Generation:

Python scripts were used to generate synthetic datasets for users, drivers, rides, and promo codes. These datasets were designed to simulate real-world behavior on a ride-sharing platform.

Data Storage:

The generated data was stored in a PostgreSQL database, structured across multiple tables such as users, drivers, rides, and promo_codes.

Data Analysis & Visualization:

SQL queries were written to analyze the impact of promotional discounts, vehicle types, and driver earnings.

Apache Superset was used to create interactive dashboards and visualizations to identify trends in CLV, CAC, and revenue impact based on promo code usage.

Data Generation
Overview

A Python script was used to generate synthetic data that mimics a real-world ride-sharing platform:

Users: Generated 5,000 user records with attributes like signup channel, acquisition cost (CAC), promo code usage, and city.

Drivers: Generated 1,000 driver records with attributes like name, vehicle type, rating, and city.

Rides: Generated 30,000 rides with details like ride fare, discount amount, vehicle type, ride status, and origin/destination coordinates.

Promo Codes: Defined a set of promo codes with discount percentages.

Python Libraries Used:

Faker: For generating fake names, dates, cities, and other random data.

NumPy: For generating numerical data (e.g., fare amounts, discount percentages).

psycopg2: For inserting data into the PostgreSQL database.

To run the data generation:

python data_generation.py


This script connects to a PostgreSQL database, creates the necessary tables, and populates them with the synthetic data.

SQL Queries

Once the data is stored in PostgreSQL, the following SQL queries are used to analyze the impact of discounts, ride frequency, and other trends:

1. Discount Impact on Ride Frequency & Revenue
SELECT 
    p.discount_percent,
    COUNT(r.ride_id) AS total_rides,
    ROUND(AVG(r.fare_amount), 2) AS avg_fare_before_discount,
    ROUND(AVG(r.fare_amount - r.discount_amount), 2) AS avg_fare_after_discount,
    ROUND(SUM(r.fare_amount), 2) AS total_fare_before_discount,
    ROUND(SUM(r.fare_amount - r.discount_amount), 2) AS total_fare_after_discount,
    ROUND(COUNT(r.ride_id) * 100.0 / (SELECT COUNT(*) FROM rides WHERE ride_status = 'completed'), 2) AS percentage_of_total_rides
FROM 
    users u
JOIN 
    promo_codes p ON u.promo_code_used = p.promo_code
JOIN 
    rides r ON u.user_id = r.user_id
WHERE 
    r.ride_status = 'completed'
GROUP BY 
    p.discount_percent
ORDER BY 
    p.discount_percent DESC;

2. Revenue by Discount Percentage
SELECT 
    p.discount_percent,
    COUNT(r.ride_id) AS total_rides,
    ROUND(SUM(r.fare_amount), 2) AS total_revenue
FROM 
    users u
JOIN 
    promo_codes p ON u.promo_code_used = p.promo_code
JOIN 
    rides r ON u.user_id = r.user_id
WHERE 
    r.ride_status = 'completed'
GROUP BY 
    p.discount_percent;

3. Vehicle Type Popularity
SELECT 
    vehicle_type, 
    COUNT(ride_id) AS total_rides
FROM 
    rides
WHERE 
    ride_status = 'completed'
GROUP BY 
    vehicle_type
ORDER BY 
    total_rides DESC;

Data Visualizations

Once the SQL queries were written, the results were visualized using Apache Superset. Key visualizations include:

1. Rides by Discount Percentage

A bar chart to compare the number of rides for each discount percentage.

2. Revenue by Discount Percentage

A bar chart showing the total revenue for each discount level.

3. Vehicle Type Popularity

A pie chart showing the distribution of rides taken in each vehicle type (Economy, Premium, SUV).

4. Discount Impact on Average Fare

A line chart comparing the average fare before and after discount for each discount percentage.

These visualizations helped to identify trends like:

The impact of discount percentages on ride frequency and total revenue.

The popularity of vehicle types and driver earnings across different discount campaigns.

How to Run the Project
1. Install Dependencies

Ensure that you have Python 3.x installed. Install the required dependencies by running:

pip install -r requirements.txt

2. Set Up PostgreSQL

Make sure PostgreSQL is installed and running. Create a database and update the DB_PARAMS in the data_generation.py script with your PostgreSQL credentials (e.g., username, password, database name).

3. Generate the Data

Run the following Python script to generate and insert synthetic data into your PostgreSQL database:

python data_generation.py

4. Set Up Apache Superset

Install and configure Apache Superset (follow this guide
).

Connect Superset to your PostgreSQL database and import the relevant tables (users, drivers, rides, promo_codes, marketing_campaigns).

Use Superset’s SQL Lab to run the SQL queries for analysis.

Create visualizations and dashboards based on the results.

License

This project is licensed under the MIT License - see the LICENSE
 file for details.

Final Notes

If you want to explore the database directly, you can use pgAdmin or any other PostgreSQL client.

The visualizations in Apache Superset provide a clear, interactive way to analyze the data and identify trends in the ride-sharing platform’s performance.


