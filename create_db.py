import mysql.connector

from logger import logger

all_sql_tables = []

# Define the tables: Restaurants, Categories, and Restaurants_Categories
restaurants_table_query = """
CREATE TABLE IF NOT EXISTS Restaurants (
    Restaurant_Id INT AUTO_INCREMENT PRIMARY KEY,
    Name varchar(250) NOT NULL,
    Phone varchar(50),
    Address varchar(250),
    Rating varchar(50),
    Rating_Count int
);
"""
all_sql_tables.append(restaurants_table_query)

categories_table_query = """
CREATE TABLE IF NOT EXISTS Categories (
    Category_Id INT AUTO_INCREMENT PRIMARY KEY,
    Category_Name char(250) NOT NULL
);
"""
all_sql_tables.append(categories_table_query)

restaurants_categories_table_query = """
CREATE TABLE IF NOT EXISTS Restaurants_Categories (
    Restaurant_Id INT,
    Category_Id INT,
    FOREIGN KEY (Restaurant_Id) REFERENCES Restaurants(Restaurant_Id),
    FOREIGN KEY (Category_Id) REFERENCES Categories(Category_Id)
);
"""
all_sql_tables.append(restaurants_categories_table_query)


def build_database(db_name, host_name, user_name, password, all_sql_tables):
    my_db = None
    try:
        # Define the connection and the cursor that is used for executing the SQL commands
        my_db = mysql.connector.connect(host=host_name, user=user_name, passwd=password)
        cursor = my_db.cursor()

        # Create the database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(db_name))
        cursor.execute("USE {}".format(db_name))

        # Execute all SQL commands and commit them into the DB
        for sql_q in all_sql_tables:
            cursor.execute(sql_q)
        my_db.commit()
        logger.info("\n*** Database was created successfully. ***\n")  # log into a logs file

    except mysql.connector.Error as error:
        if my_db:
            my_db.rollback()  # rollback if any exception occurred
        logger.critical("Failed creating database {}.".format(error))  # log into a logs file

    finally:
        if my_db:
            if my_db.is_connected():
                cursor.close()
                my_db.close()
                logger.info("MySQL connection is closed.")
            else:
                logger.info("Connection to MySQL did not succeed.")


# Replace these values with your actual database credentials
build_database("restaurant_data_db", "localhost", "root", "12345", all_sql_tables)
