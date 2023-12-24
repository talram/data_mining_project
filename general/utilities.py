import json
import os
import argparse
from general.logger import logger


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')

    try:
        with open(config_path, 'r') as file:
            config_data = json.load(file)
        return config_data
    except FileNotFoundError:
        logger.error("config.json file not found.")
        return None
    except json.JSONDecodeError:
        logger.error("Error decoding JSON in config.json.")
        return None


def load_constants():
    config_data = load_config()
    if config_data is not None:
        logger.info("\n*** Constants files are loaded and ready to use. ***\n")
        return config_data.get('constants', {})
    else:
        return {}


def load_db_config():
    config_data = load_config()

    if config_data is not None:
        logger.info("\n*** Database configurations are loaded and ready to use. ***\n")
        return config_data.get('DB_CONFIG', {})
    else:
        return {}


def parse():
    parser = argparse.ArgumentParser(prog='yellow_pages_web_scraper', description="yellow pages web scraper",
                                     epilog='bon appetit')
    parser.add_argument('-sh', '--show-everything', action='store_true',
                        help='optional, show the relevant data')
    parser.add_argument('-csv', '--export-csv', action='store_true',
                        help='optional, import the data to csv file')
    parser.add_argument('-idb', '--insert-data-base', action='store_true',
                        help='optional, insert the data to mysql')
    args = parser.parse_args()
    print("nothing will be shown, try adding -sh to see on terminal") if not args.show_everything else ""
    print("nothing will be exported, try adding -csv to export to csv file") if not args.export_csv else ""
    print("nothing will be insert, try adding -idb to export to MySQL") if not args.insert_data_base else ""
    return args.show_everything, args.export_csv, args.insert_data_base


def flags(flag_show, flag_excel, flag_insert_data_base):
    flag_scrape = False
    list_flags = [flag_show, flag_excel, flag_insert_data_base]
    if any(list_flags):
        flag_scrape = True
    return flag_scrape
