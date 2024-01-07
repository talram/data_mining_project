from general.export import print_the_scraping_data, scraped_yellow_page_data_to_csv
from general.api import get_enrichment_data_to_csv
from general.database import create_db
from general.database.connect_insert_db import insert_data
from general.database.create_db import create_tables
from general.preprocess_data_for_enrichment import preprocess_yellow_pages_an_yelp
from general.web_scraper import scrape
from general.utilities import load_constants, load_db_config
import argparse


def main():
    parser = argparse.ArgumentParser(description="Web Scraper of Yellow Pages")
    parser.add_argument("-sc", "--scrape", action="store_true", help="Scrape Yellow Pages website")
    parser.add_argument("-p", "--print", action="store_true", help="Print the scraped data")
    args = parser.parse_args()

    print("It might take 2-3 minutes because we scrape 100 pages, thanks for your patience")

    if args.scrape:
        scraped_dict = scrape(load_constants().get('BASE_URL'))

        if args.print:
            print_the_scraping_data(scraped_dict)

        scraped_yellow_page_data_to_csv(scraped_dict, load_constants().get('YELLOW_PAGES_CSV_FILE'))

        # API_KEY kept in SECRET,
        # so only_matched_yelp.csv and raw yelp files were uploaded to GitHub
        secret_api = False  # False by default
        if secret_api:
            get_enrichment_data_to_csv(load_constants().get('YELLOW_PAGES_CSV_FILE'),
                                       load_constants().get('ENDPOINT'),
                                       load_constants().get('HEADERS'))

        create_db.build_database(load_db_config().get("database"), load_db_config().get("host"),
                                 load_db_config().get("user"), load_db_config().get("password"),
                                 create_tables())

        preprocess_yellow_pages_an_yelp(load_constants().get('YELP_RAW_CSV_FILE'),
                                        load_constants().get('YELLOW_PAGES_CSV_FILE'))

        print("+++ Inserting the scraped data into the database +++")
        insert_data(scraped_dict, load_db_config())

    else:
        print("No action specified. Use -sc to scrape Yellow Pages website.")


if __name__ == "__main__":
    main()
