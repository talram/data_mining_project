import pandas as pd
import requests

from bs4 import BeautifulSoup
import argparse
import sys
import csv
import json
import mysql.connector
from sqlalchemy import create_engine

from logger import logger


def load_config():
    try:
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            config_data = json.load(config_file)
            return config_data
    except FileNotFoundError:
        print(f"config file '{CONFIG_FILE_PATH}' not found.")
    except json.JSONDecodeError:
        print(f"error decoding JSON in the config file '{CONFIG_FILE_PATH}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


def print_all(print_dict_categories):
    if not print_dict_categories:
        print("No restaurant data to display.")
        return
    print()
    print("the restaurant list is:")
    for number in range(1, len(print_dict_categories) + 1):
        print("Restaurant Number:", print_dict_categories[number]['Number'])
        print("Name:", print_dict_categories[number]['Name'])
        print("Categories:", print_dict_categories[number]['Categories'])
        print("Phone:", print_dict_categories[number]['Phone'])
        print("Address:", print_dict_categories[number]['Address'])
        print("Rating:", print_dict_categories[number]['Rating'])
        print("Rating Count:", print_dict_categories[number]['Rating Count'])
        print()


def export_all(export_dict_categories):
    csv_file_path = CONFIG.get('CSV_FILE_PATH')

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = list(export_dict_categories.values())[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for number, restaurant_info in export_dict_categories.items():
            writer.writerow({
                'Number': restaurant_info['Number'],
                'Name': restaurant_info['Name'],
                'Categories': restaurant_info['Categories'],
                'Phone': restaurant_info['Phone'],
                'Address': restaurant_info['Address'],
                'Rating': restaurant_info['Rating'],
                'Rating Count': restaurant_info['Rating Count']
            })

    print(f'CSV file created: {csv_file_path}')


def find_rating(listing):
    rating_classes = CONFIG.get('RATING_CLASSES', {})
    try:
        for class_name, rating_value in rating_classes.items():
            ratings_element = listing.find('div', class_=class_name)
            if ratings_element:
                return rating_value
        else:
            return 'rating not available'
    except Exception as e:
        print(f"Error extracting rating: {e}")
        return 'rating extraction error'


def extract_categories(category_element):
    try:
        if category_element:
            categories = ', '.join(link.text.strip() for link in category_element.find_all('a'))
            return categories
        else:
            return 'Category not available'
    except Exception as e:
        print(f"Error extracting categories: {e}")
        return 'Category extraction error'


def extract_address(address_element, locality_element):
    try:
        if address_element and locality_element:
            address = address_element.text.strip() + ', ' + locality_element.text.strip()
            return address
        elif address_element:
            address = address_element.text.strip()
            return address
        elif locality_element:
            address = locality_element.text.strip()
            return address
        else:
            address = 'Address not available'
            return address
    except Exception as e:
        print(f"Error extracting categories: {e}")
        return 'Address extraction error'


def extract_rating_count(count_element):
    try:
        if count_element:
            rating_count = count_element.text.strip()
            return rating_count
        else:
            rating_count = 'Review count not available'
            return rating_count
    except Exception as e:
        print(f"Error extracting categories: {e}")
        return 'Rating count extraction error'


def extract_name(name_element):
    try:
        if name_element:
            name = name_element.text.strip().split('. ', 1)[-1]
            return name
        else:
            name = 'Name not available'
            return name
    except Exception as e:
        print(f"Error extracting categories: {e}")
        return 'name extraction error'


def extract_phone(phone_element):
    try:
        if phone_element:
            phone = phone_element.text.strip()
            return phone
        else:
            phone = 'Phone number not available'
            return phone
    except Exception as e:
        print(f"Error extracting categories: {e}")
        return 'phone extraction error'


def search(restaurant_listings, dict_categories):
    # dict_categories = {}
    if not dict_categories:
        start_index = 1
    else:
        start_index = max(dict_categories.keys()) + 1
    for index, listing in enumerate(restaurant_listings, start=start_index):
        try:
            number = index
            category_element = listing.find('div', class_='categories')
            category = extract_categories(category_element)

            name_element = listing.find('h2')
            name = extract_name(name_element)

            phone_element = listing.find('div', class_='phones phone primary')
            phone = extract_phone(phone_element)

            address_element = listing.find('div', class_='street-address')
            locality_element = listing.find('div', class_='locality')
            address = extract_address(address_element, locality_element)

            rating = find_rating(listing)

            count_element = listing.find('span', class_='count')
            rating_count = extract_rating_count(count_element)

            dict_categories[index] = {'Number': number,
                                      'Name': name,
                                      'Categories': category,
                                      'Phone': phone,
                                      'Address': address,
                                      'Rating': str(rating) + "/5",
                                      'Rating Count': rating_count}
        except Exception as e:
            print(f"Error processing listing (inside main search function) {index}: {e}")
    return dict_categories


def parse():
    parser = argparse.ArgumentParser(prog='yellow_pages_web_scraper', description="yellow pages web scraper",
                                     epilog='bon appetit')
    parser.add_argument('-sc', '--scrape-everything', action='store_true',
                        help='essential, scrape the relevant data')
    parser.add_argument('-sh', '--show-everything', action='store_true',
                        help='optional, show the relevant data')
    parser.add_argument('-csv', '--export-csv', action='store_true',
                        help='optional, import the data to csv file')
    parser.add_argument('-db', '--data-base', action='store_true',
                        help='optional, insert the data to mysql')
    args = parser.parse_args()
    print("you should scrape to get relevant information,\n -h help\n -sc for scrape") \
        if not args.scrape_everything else ""
    print("nothing will be shown, try adding -sh to see on terminal") if not args.show_everything else ""
    print("nothing will be exported, try adding -csv to export to csv file") if not args.export_csv else ""
    print("nothing will be insert, try adding -db to export to MySQL") if not args.data_base else ""
    return args.scrape_everything, args.show_everything, args.export_csv, args.data_base


def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="restaurant_data_db"
    )


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


def insert_to_yelp_data_table():
    mysql_config = {
        'user': 'root',
        'password': '12345',
        'host': 'localhost',
        'database': 'restaurant_data_db',
    }

    mysql_connection = mysql.connector.connect(**mysql_config)

    csv_file_path = 'only_matched_yelp.csv'

    table_name = 'yelp_data'

    df_yelp = pd.read_csv(csv_file_path)

    # Create a MySQL connection and insert data into the table
    engine = create_engine(
        f"mysql+mysqlconnector://{mysql_config['user']}:{mysql_config['password']}@{mysql_config['host']}/{mysql_config['database']}")

    df_yelp.to_sql(table_name, engine, if_exists='replace', index=False)

    mysql_connection.close()

    print(f"Data from {csv_file_path} successfully loaded into {table_name} table.")


def insert_data(main_dict_categories):
    try:
        with connect_to_database() as conn, conn.cursor() as cursor:
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

        insert_to_yelp_data_table()
        logger.info("Data inserted into Yelp_Data table successfully.")
        logger.info("All data inserted successfully.")

    except mysql.connector.Error as error:
        logger.error("Failed to insert data: {}".format(error))


def main():
    main_dict_categories = {}
    flag_scrape, flag_show, flag_excel, flag_data_base = parse()
    flag_scrape, flag_show, flag_excel, flag_data_base = True, True, False, True  # for testing, delete at the end
    if flag_scrape:
        # base_url = "https://www.yellowpages.com/los-angeles-ca/restaurants?page={}"
        base_url = CONFIG.get('BASE_URL')
        for page_number in range(1, 101):  # Change the range accordingly, above 101 Irrelevant
            url = base_url.format(page_number)
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                restaurant_listings = soup.find_all('div', class_='info')
                main_dict_categories = search(restaurant_listings, main_dict_categories)
            except requests.RequestException as req_error:
                print(f"Request error (is the website address correct?): {req_error}")
            except Exception as main_error:
                print(f"An unexpected error occurred: {main_error}")
    else:
        print("to use the program choose -sc, -h or --help for help")
    if flag_show:
        print_all(main_dict_categories)
    if flag_excel:
        export_all(main_dict_categories)
    if flag_data_base:
        # Insert this data into the database restaurants
        print("+++ Inserting the scraped data into the database +++")
        insert_data(main_dict_categories)


if __name__ == '__main__':
    # script_dir = os.path.dirname(os.path.abspath(__file__))  # overkill
    # CONFIG_FILE_PATH = os.path.join(script_dir, 'config.json')  # overkill
    CONFIG_FILE_PATH = 'config.json'  # make sure the json file is in the folder of the scraper
    # config_file_path = CONFIG.get('CONFIG_FILE_PATH')
    # from config import CONFIG_FILE_PATH
    CONFIG = load_config()
    if CONFIG is None:
        sys.exit("CONFIG is not loaded, goodbye everybody I got to go and find the json file ")
    main()
