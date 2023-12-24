import numpy as np
import pandas as pd

YELP_RAW_CSV_FILE = 'yelp_retrieved_restaurants.csv'
YELLOW_PAGES_CSV_FILE = 'restaurants.csv'

yelp_raw_data = pd.read_csv(YELP_RAW_CSV_FILE)

# Dedup records
yelp_dedup_data = yelp_raw_data.drop_duplicates()

# Relevant Yelp's columns
selected_columns = ['name', 'rating', 'price', 'transactions']
yelp_processed_data = yelp_dedup_data[selected_columns]

# Modify Yelp's column: has or hasn't delivery
yelp_processed_data['transactions'] = np.where(yelp_processed_data['transactions'].str.contains('delivery'), 'Yes',
                                               'No')

# Match restaurants between 2 data sources:
# Yellow Pages (Web Scraper), and Yelp (Data Enrichment - via API)

df_yellow_pages = pd.read_csv(YELLOW_PAGES_CSV_FILE)
df_yellow_pages['lower_name'] = df_yellow_pages['Name'].str.lower()
df_yellow_pages.drop_duplicates(inplace=True)
yelp_processed_data['lower_name'] = yelp_processed_data['name'].str.lower()

# Check & remove missing values in the 'lower_name' column
if yelp_processed_data['lower_name'].isnull().any():
    yelp_processed_data = yelp_processed_data.dropna(subset=['lower_name'])

df_merged = pd.merge(df_yellow_pages, yelp_processed_data, on='lower_name')
df_merged_dedup = df_merged.drop_duplicates()
df_merged_dedup.drop_duplicates(subset=['Number'], inplace=True)

df_ready_for_enrichment = df_merged_dedup.drop(['lower_name', 'name'], axis=1)

# Rename Yelp's columns
# yelp_processed_data.rename

df_ready_for_enrichment.rename(columns={'price': 'Yelp_type_Pricing',
                                        'transactions': 'Yelp_has_delivery',
                                        'rating': 'Yelp_Rating'}, inplace=True)

df_only_matched_yelp = df_ready_for_enrichment[['Number', 'Yelp_has_delivery',
                                                'Yelp_type_Pricing', 'Yelp_Rating']]
df_only_matched_yelp.rename(columns={'Number': 'Restaurant_Id'}, inplace=True)

df_only_matched_yelp.to_csv('only_matched_yelp.csv', index=False)

df_ready_for_enrichment.to_csv('enriched_restaurants_data.csv', index=False)
