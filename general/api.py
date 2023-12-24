import requests
import pandas as pd
import os

from general.logger import logger


def get_enrichment_data_to_csv(yellow_pages_csv_file, endpoint, headers):
    for page_num in range(0, 500, 50):
        parameters = {'location': 'Los Angeles',
                      'term': 'restaurants',
                      'limit': 50,
                      'offset': page_num
                      }

        response = requests.get(url=endpoint, params=parameters, headers=headers)
        data = response.json()

        current_page_df = pd.json_normalize(data.get('businesses', []))

        # Append / write to the CSV file
        if os.path.exists(yellow_pages_csv_file):
            existing_data = pd.read_csv(yellow_pages_csv_file)
            updated_data = pd.concat([existing_data, current_page_df], ignore_index=True)
            updated_data.to_csv(yellow_pages_csv_file, index=False, encoding='utf-8')
        else:
            current_page_df.to_csv(yellow_pages_csv_file, index=False, encoding='utf-8', header=True)

    print(f"Data appended to the CSV file '{yellow_pages_csv_file}' successfully.")
    logger.info("Yelp restaurant's data has retrieved and converted to a CSV file.")
