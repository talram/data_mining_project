import csv
from general.logger import logger


def print_the_scraping_data(print_dict_categories):
    if not print_dict_categories:
        print("No restaurant data to display.")
        return
    print("---- The restaurant list is: ----")

    keys = ['Number', 'Name', 'Categories', 'Phone', 'Address', 'Rating', 'Rating Count']
    for number, dict_info in print_dict_categories.items():
        print('\n'.join(f"{key}: {dict_info.get(key, 'N/A')}" for key in keys))


def scraped_yellow_page_data_to_csv(export_dict_categories, yellow_pages_csv_file_path):
    with open(yellow_pages_csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
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

    print(f'CSV file created: {yellow_pages_csv_file_path}')
    logger.info("Yellow Pages scraped data is converted to a csv file.")
