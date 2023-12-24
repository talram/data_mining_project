import requests
import pandas as pd
import os

API_KEY = "B9mEEpxDvVaE2hvFuomBnu2Q2rWcpP34uWfeN1rHkjVK9CNZ6tlRN_oBtn3qvpCcA_nxaQeBpymLyj1F2iszjCE0utVmmwDFBbhP2OCwsLlE3Mb7WAG8vZce8WKHZXYx"
ENDPOINT = "https://api.yelp.com/v3/businesses/search"
HEADERS = {'Authorization': 'bearer %s' % API_KEY}

csv_file_path = 'yelp_retrieved_restaurants.csv'


for page_num in range(0, 500, 50):
    PARAMETERS = {'location': 'Los Angeles',
                  'term': 'restaurants',
                  'limit': 50,
                  'offset': page_num
                  }

    response = requests.get(url=ENDPOINT, params=PARAMETERS, headers=HEADERS)
    data = response.json()

    current_page_df = pd.json_normalize(data.get('businesses', []))

    # Append / write to the CSV file
    if os.path.exists(csv_file_path):
        existing_data = pd.read_csv(csv_file_path)
        updated_data = pd.concat([existing_data, current_page_df], ignore_index=True)
        updated_data.to_csv(csv_file_path, index=False, encoding='utf-8')
    else:
        current_page_df.to_csv(csv_file_path, index=False, encoding='utf-8', header=True)

print(f"Data appended to the CSV file '{csv_file_path}' successfully.")
