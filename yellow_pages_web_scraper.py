import requests
from bs4 import BeautifulSoup

dict_categories = {}


def print_all(dict_categories, index):
    print("Restaurant Number:", dict_categories[index]['Number'])
    print("Name:", dict_categories[index]['Name'])
    print("Categories:", dict_categories[index]['Categories'])
    print("Phone:", dict_categories[index]['Phone'])
    print("Address:", dict_categories[index]['Address'])
    print("Rating:", dict_categories[index]['Rating'])
    print("Rating Count:", dict_categories[index]['Rating Count'])
    print()


def find_rating(listing):
    ratings_element = listing.find('div', class_='result-rating five')
    if ratings_element:
        rating = 5
        return rating

    ratings_element = listing.find('div', class_='result-rating four half')
    if ratings_element:
        rating = 4.5
        return rating

    ratings_element = listing.find('div', class_='result-rating four')
    if ratings_element:
        rating = 4
        return rating

    ratings_element = listing.find('div', class_='result-rating three half')
    if ratings_element:
        rating = 3.5
        return rating

    ratings_element = listing.find('div', class_='result-rating three')
    if ratings_element:
        rating = 3
        return rating

    ratings_element = listing.find('div', class_='result-rating two half')
    if ratings_element:
        rating = 2.5
        return rating

    ratings_element = listing.find('div', class_='result-rating two')
    if ratings_element:
        rating = 2
        return rating

    ratings_element = listing.find('div', class_='result-rating one half')
    if ratings_element:
        rating = 1.5
        return rating

    ratings_element = listing.find('div', class_='result-rating one')
    if ratings_element:
        rating = 1
        return rating

    default_value = "Rating not available"
    return default_value


url = 'https://www.yellowpages.com/los-angeles-ca/restaurants'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

restaurant_listings = soup.find_all('div', class_='info')


def extract_categories(category_element):
    if category_element:
        categories = ', '.join(link.text.strip() for link in category_element.find_all('a'))
        return categories
    else:
        return 'Category not available'


def search(restaurant_listings):
    for index, listing in enumerate(restaurant_listings, start=1):
        number = index

        category_element = listing.find('div', class_='categories')
        category = extract_categories(category_element)

        name_element = listing.find('h2')
        if name_element:
            name = name_element.text.strip().split('. ', 1)[-1]
        else:
            name = 'Name not available'

        phone_element = listing.find('div', class_='phones phone primary')
        if phone_element:
            phone = phone_element.text.strip()
        else:
            phone = 'Phone number not available'

        address_element = listing.find('div', class_='street-address')
        locality_element = listing.find('div', class_='locality')
        if address_element and locality_element:
            address = address_element.text.strip() + ', ' + locality_element.text.strip()
        elif address_element:
            address = address_element.text.strip()
        elif locality_element:
            address = locality_element.text.strip()
        else:
            address = 'Address not available'

        rating = find_rating(listing)

        count_element = listing.find('span', class_='count')
        if count_element:
            rating_count = count_element.text.strip()
        else:
            rating_count = 'Review count not available'

        dict_categories[index] = {'Number': number,
                                  'Name': name,
                                  'Categories': category,
                                  'Phone': phone,
                                  'Address': address,
                                  'Rating': str(rating) + "/5",
                                  'Rating Count': rating_count}
        print_all(dict_categories, index)


search(restaurant_listings)
