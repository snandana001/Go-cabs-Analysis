 # Taxi Analytics Project

Welcome to the **Taxi Analytics** project! This project is aimed at analyzing ride-hailing data for understanding trends in customer lifetime value (CLV), customer acquisition cost (CAC), driver earnings, and other key performance metrics.

## Project Overview

This project involves:

- **Data generation**: Simulating a large dataset of users, drivers, and rides.
- **Data storage**: Storing the data in a PostgreSQL database.
- **Data visualization**: Using Apache Superset to visualize the data and extract key insights.
- **Analysis**: Identifying trends in customer lifetime value (CLV), acquisition cost (CAC), vehicle type popularity, and more.

## Technologies Used

- **Python**: For generating synthetic data using the `Faker` library.
- **PostgreSQL**: For storing the data in a relational database.
- **Apache Superset**: For data visualization and dashboard creation.
- **Git**: For version control.

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/snandana001/Go-cabs-Analysis.git
    ```

2. Navigate to the project directory:

    ```bash
    cd taxi_analytics
    ```

3. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    .\venv\Scripts\Activate.ps1  # On Windows
    ```

4. Install the necessary dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Set up the database and run the Python script to generate data:

    ```bash
    python generate_data.py
    ```

6. Visualize the data using Apache Superset.

## Features

- **Data Generation**: Automatically generates ride, user, and driver data for analysis.
- **Database Integration**: Data is stored in PostgreSQL for easy access.
- **Visualization**: Create insightful dashboards in Superset.

## Data Model

The following tables are created in the PostgreSQL database:

- **Users**: Stores information about users who booked rides.
- **Drivers**: Stores information about the drivers and their ratings.
- **Rides**: Contains ride data, including fares and statuses.
- **Marketing Campaigns**: Tracks marketing campaigns used for customer acquisition.
- **Promo Codes**: Stores discount promo codes used by customers.

## Insights and Trends

The project includes analysis of various trends:

- **Customer Lifetime Value (CLV)**
- **Customer Acquisition Cost (CAC)**
- **Number of Rides per Driver**
- **Earnings per Driver**
- **Vehicle Type Popularity**
- **Discount Impact on Fare and Frequency**

## Future Improvements

- Integrate machine learning models to predict customer churn.
- Expand the dataset to include more attributes for analysis.
- Improve the Superset dashboard with more detailed metrics.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



