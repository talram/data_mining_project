import requests
# from bs4 import dependencies
from bs4 import BeautifulSoup
import argparse
import sys
import csv
import json


def load_config():
    try:
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            config_data = json.load(config_file)
            return config_data
    except FileNotFoundError:
        print(f"config file '{CONFIG_FILE_PATH}' not found.")
    except json.JSONDecodeError:
        print(f"error decoding JSON in the config file '{CONFIG_FILE_PATH}'.")
    except KeyError as e:
        print(f"keyError: {e} not found in the configuration file.")


def print_all(print_dict_categories):
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
    CSV_FILE_PATH = CONFIG.get('CSV_FILE_PATH')

    with open(CSV_FILE_PATH, 'w', newline='', encoding='utf-8') as csv_file:
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

    print(f'CSV file created: {CSV_FILE_PATH}')


def find_rating(listing):
    RATING_CLASSES = CONFIG.get('RATING_CLASSES', {})
    try:
        for class_name, rating_value in RATING_CLASSES.items():
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


def search(restaurant_listings):
    dict_categories = {}
    for index, listing in enumerate(restaurant_listings, start=1):
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
    parser.add_argument('-ex', '--import-excel', action='store_true',
                        help='optional, import the data to csv file')
    args = parser.parse_args()
    print("you should scrape to get relevant information,\n -h help\n -sc for scrape") \
        if not args.scrape_everything else ""
    print("nothing will be shown, try adding -sh to see on terminal") if not args.show_everything else ""
    print("nothing will be exported, try adding -ex to export to excel") if not args.import_excel else ""
    return args.scrape_everything, args.show_everything, args.import_excel


def main():
    main_dict_categories = {}
    flag_scrape, flag_show, flag_excel = parse()
    if flag_scrape:
        url = 'https://www.yellowpages.com/los-angeles-ca/restaurants'
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            restaurant_listings = soup.find_all('div', class_='info')
            main_dict_categories = search(restaurant_listings)
        except requests.RequestException as req_error:
            print(f"Request error (is the website address correct?): {req_error}")
        except Exception as main_error:
            print(f"An unexpected error occurred : {main_error}")
    else:
        print("to use the program choose -sc, -h or --help for help")
    if flag_show:
        print_all(main_dict_categories)
    if flag_excel:
        export_all(main_dict_categories)


if __name__ == '__main__':
    CONFIG_FILE_PATH = 'config.json'
    CONFIG = load_config()
    if CONFIG is None:
        sys.exit("CONFIG is not loaded, goodbye everybody I got to go and find the json file ")
    main()
