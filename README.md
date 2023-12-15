# data_mining_project
​
# Yellow pages resturants web scraper
​
Scrape throught the real yellow pages resturants by url and give list of Restaurant Number, Name, Categories, Phone, Address, Rating and Rating Count. 
​
​
## Used By
​
Every willing user/consumer that searches restaurants at unitedd states.
​
​
## Running Tests
​
To run tests, run the following command
move to the current file folder
```bash
  web_scraper_yellow_pages.py
```
run will print the the standard location.
to change locations, take different url from the website.
change the  url='website_address' (at line 68)inside the file
for example: 
url='https://www.yellowpages.com/search?search_terms=restaurants&geo_location_terms=Los+Angeles%2C+CA'
to something you desire
​
​

will look like:
\web_scraper_yellow_pages.py" 


Restaurant Number: 1
Name: Palermo Ristorante Italiano
Categories: Restaurants, Pizza, Italian Restaurants
Phone: (323) 663-1178
Address: 1858 N Vermont Ave, Los Angeles, CA 90027
Rating: 4.5/5
Rating Count: (45)
​

Restaurant Number: 2
Name: Casa Bianca Pizza Pie
Categories: Restaurants, Pizza, Italian Restaurants
Phone: (323) 256-9617
Address: Los Angeles, CA 90041
Rating: 4.5/5
Rating Count: (35)
​

Restaurant Number: 3
Name: Oyabun Seafood
Categories: Restaurants, Seafood Restaurants, Asian Restaurants
Phone: (323) 716-4355
Address: 3060 W Olympic Blvd #150, Los Angeles, CA 90006
Rating: 4/5
Rating Count: (3)
...
​
## Tech Stack
​
Python interpreter 3.11+
pypi requests
pypi bs4

​
## Run Locally
​
Clone the project
​
```bash
  git clone https://link-to-project
  change to relevant
```
​
Go to the project directory
​
```bash
  cd my-project
```
​
```bash
  python
  pip install requests
  pip install bs4
```
​
Start the web_scraper_yellow_pages.py
​
run it to get standard text or open and cahnge url at line 68.
​
​
## Database Documentation
​
### Schema Installation

​
Set up the database schema:
​

Run Database Setup Script: python create_db.py
​
### Database Schema
Our database consists of the following tables:

#### Restaurants Table:

Restaurant_Id (Primary Key)
Name
Phone
Address
Rating
Rating_Count

#### Categories Table:

Category_Id (Primary Key)
Category_Name (Unique)

#### Restaurants_Categories Table
Restaurant_Id (Foreign Key)
Category_Id (Foreign Key)
​
​

### ERD Diagram


### Usage
To insert data into the database, use  (at least) the command:

python scraper.py -sc

## Roadmap
​
the desire to simplify the way of comparing resturants for consumers that live in the united states.
the program made of search method of web scraper that store the information in a dictionary and prints them.
the search function was parted for simplification of ease and mutability.
​
​
## Support
​
​
orgewe@gmail.com
​
​
## License
​
Copyright (c) [2023] [Tal & Or]
​
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
​
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
​
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
​
EVERY COMMERCIAL GAIN BELONG TO THE REAL YELLOW PAGES tm
​
## Lessons Learned
​
python bs4 methods and pytohn requests with use of collecting the information to dictionary which the elements are listed by enumerate and classeses which collecetd from changing website with differnt elements of HTML Classes.
​
​
## Feedback
​
If you have any feedback, please reach out to us at:
​
orgewe@gmail.com
​
​
## Authors
​
Tal Ramon
​
Or gewelber
​
​
## Acknowledgements
​
ITC - Israel Tech Challenge
