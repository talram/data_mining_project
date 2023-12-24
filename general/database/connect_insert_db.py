import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

from general.logger import logger


def insert_data_to_restaurants_table(cursor, restaurant_info):
    try:
        # Insert data into the Restaurants table
        insert_query = """
            INSERT INTO Restaurants (Name, Phone, Address, Rating, Rating_Count)
            VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (
            restaurant_info['Name'],
            restaurant_info['Phone'],
            restaurant_info['Address'],
            restaurant_info['Rating'],
            restaurant_info['Rating Count']
        ))

        # Return the last inserted row id - Restaurant_Id
        return cursor.lastrowid
    except mysql.connector.Error as error:
        logger.error("Failed to insert data into Restaurants table: {}".format(error))
        raise


def insert_to_categories_table(cursor, category_name):
    try:
        # Check if the category already exists
        check_query = "SELECT Category_Id FROM Categories WHERE Category_Name = %s;"
        cursor.execute(check_query, (category_name,))
        result = cursor.fetchone()

        if not result:
            # Category doesn't exist, insert a new record
            insert_query = "INSERT INTO Categories (Category_Name) VALUES (%s);"
            cursor.execute(insert_query, (category_name,))

            # Return the last inserted row id - Category_Id
            return cursor.lastrowid
        else:
            # Category already exists, return the existing Category_Id
            return result[0]

    except mysql.connector.Error as error:
        logger.error("Failed to insert data into Categories table: {}".format(error))
        raise


def insert_to_restaurants_categories_table(cursor, restaurant_id, category_ids):
    try:
        # Insert data into the Restaurants_Categories table
        insert_query = """
            INSERT INTO Restaurants_Categories (Restaurant_Id, Category_Id)
            VALUES (%s, %s);
        """

        # Insert multiple rows for each restaurant_id and its associated category_ids
        for category_id in category_ids:
            cursor.execute(insert_query, (restaurant_id, category_id))

    except mysql.connector.Error as error:
        logger.error("Failed to insert data into Restaurants_Categories table: {}".format(error))
        raise


def insert_to_yelp_data_table(db_config):
    mysql_connection = mysql.connector.connect(**db_config)

    csv_file_path = 'only_matched_yelp.csv'

    table_name = 'yelp_data'

    df_yelp = pd.read_csv(csv_file_path)

    # Create a MySQL connection and insert data into the table
    engine = create_engine(
        f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}"
        f"@{db_config['host']}/{db_config['database']}")

    df_yelp.to_sql(table_name, engine, if_exists='replace', index=False)

    mysql_connection.close()

    print(f"Data from {csv_file_path} successfully loaded into {table_name} table.")


def insert_data(main_dict_categories, db_config):
    try:
        mysql_connection = mysql.connector.connect(**db_config)

        with mysql_connection as conn, conn.cursor() as cursor:
            for number, restaurant_info in main_dict_categories.items():
                # Insert into Restaurants table
                restaurant_id = insert_data_to_restaurants_table(cursor, restaurant_info)

                # Insert into Categories table
                categories = restaurant_info['Categories'].split(', ')
                category_ids = [insert_to_categories_table(cursor, category_name) for category_name in categories]

                # Insert into Restaurants_Categories table
                insert_to_restaurants_categories_table(cursor, restaurant_id, category_ids)

            logger.info("Data inserted into Categories table successfully.")
            logger.info("Data inserted into Restaurants table successfully.")
            logger.info("Data inserted into Restaurants_Categories table successfully.")

            conn.commit()

        insert_to_yelp_data_table(db_config)
        logger.info("Data inserted into Yelp_Data table successfully.")
        logger.info("All data inserted successfully.")

    except mysql.connector.Error as error:
        logger.error("Failed to insert data: {}".format(error))
