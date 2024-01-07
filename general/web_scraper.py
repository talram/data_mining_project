import requests
from bs4 import BeautifulSoup

# from general.utilities import load_constants
from general.utilities import load_constants


def find_rating(listing):
    rating_classes = {
        'result-rating five': 5,
        'result-rating four half': 4.5,
        'result-rating four': 4,
        'result-rating three half': 3.5,
        'result-rating three': 3,
        'result-rating two half': 2.5,
        'result-rating two': 2,
        'result-rating one half': 1.5,
        'result-rating one': 1
    }
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


def scrape(config_base_url):
    main_dict_categories = {}
    for page_number in range(1, 3):  # Change the range accordingly, above 101 Irrelevant
        base_url = config_base_url
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

    return main_dict_categories
