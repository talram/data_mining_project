## **data_mining_project:**
​
## Yellow Pages Restaurants Web Scraper
​

## Table of Contents
1. [Introduction](#introduction)
2. [Used By](#used-by)
3. [Run Locally](#run-locally)
    - [Running Tests](#running-tests)
        - [Unix/Linux](#unixlinux)
        - [Windows](#windows)
        - [PyCharm](#pycharm)
4. [Tech Stack](#tech-stack)
5. [Roadmap](#roadmap)
6. [Database Documentation](#database-documentation)
    - [Schema Installation](#schema-installation)
    - [Database Schema](#database-schema)
    - [ERD Diagram](#erd-diagram)
    - [Usage](#usage)
7. [Support](#support)
8. [License](#license)
9. [Lessons Learned](#lessons-learned)
10. [Feedback](#feedback)
11. [Authors](#authors)
12. [Acknowledgements](#acknowledgements)


## Introduction
Scrape through the real yellow pages and tripadvisor for restaurants by URL and provide a list of Restaurant Number, Name, Categories, Phone, Address, Rating, and Rating Count.

## Used By

Every willing user/consumer that searches restaurants in the United States.

## Run Locally

To run the scraper locally, follow these steps
Clone the repository:
git clone https://github.com/your-username/yellow-pages-scraper.git

## Running Tests

To run tests, follow the steps below:
<span style="color: red;">update at the end of milestone3.</span>

### Unix/Linux
### bash
```
#simply go to file folder with the script and JSON file inside. 
cd ./folder
chmod +x web_scraper_yellow_pages.py
#than you can run web_scraper_yellow_pages.py
#default values for -sc, -sh and -ex are all False
#write 
web_scraper_yellow_pages.py -example_letter_1 -example_letter_2 -example_letter_3 
-h for help
-sc for scrape
-sh for showing result at terminal
-ex for export to csv file at local file of the script
#make sure to add -sc with every -sh or -ex, without it will not scan values.
```
### windows
## CMD
``` 
#simply go to file folder with the script and JSON file inside. 
cd ./folder
#default values for -sc, -sh and -ex are all False
#write 
web_scraper_yellow_pages.py -example_letter_1 -example_letter_2 -example_letter_3 
-h for help
-sc for scrape
-sh for showing result at terminal
-ex for export to csv file at local file of the script
#make sure to add -sc with every -sh or -ex, without it will not scan values.

```
### pycharm
```
#open the script at folder with script and the JSON file
#right mouse click on script name, than modify configutation beofre run
#at empty cell of change parametes right the parametere you want to enter:
-h for help
-sc for scrape
-sh for showing result at terminal
-ex for export to csv file at local file of the script
#make sure to add -sc with every -sh or -ex, without it will not scan values.
#or change the json file address at yellow_pages_web_scraper.py
if __name__ == '__main__':
    CONFIG_FILE_PATH = 'config.json'
```
run will print the standard location.
to change locations, take different url from the website.
change the  url='website_address' at config.json
for example: 
url='https://www.yellowpages.com/los-angeles-ca/restaurants?page=1'  
make sure to take address with number at the end
​
​
<span style="color: red;">update at the end of milestone3.</span>
will look like:
\web_scraper_yellow_pages.py -sc -sh
(-sc -sh is for scrape and show, further explanation at running test section)

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
**Python interpreter 3.12+
requests  
bs4
​
## Run Locally
​
Clone the project
​
bash

<span style="color: red;">update at the end of milestone3.</span>

```bash
--cd ./folder
--git clone https://github.com/talram/data_mining_project.git
--make sure JSON file is also at the file 
or change the json file address at yellow_pages_web_scraper.py
if __name__ == '__main__':
    CONFIG_FILE_PATH = 'config.json'
```
​
```bash
  python
  pip install requests
  pip install bs4
```
​
first run create_db  
Start the web_scraper_yellow_pages.py
​
run it to get standard text or open and change url at def main function
​
​
## Roadmap
​
the desire to simplify the way of comparing restaurants for consumers that live in the United States.
the program made of search method of web scraper that store the information in a dictionary and prints them.
the search function was parted for simplification of ease and mutability.
​
​

# Database Documentation
​
### Schema Installation

​
Set up the database schema:
​

Run Database Setup Script: python create_db.py
​
### Database Schema
Our database consists of the following tables:
to update 
<span style="color: red;">update at the end of milestone3.</span>
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
<span style="color: red;">update at the end of milestone3.</span>

![The Erd Diagram](https://github.com/talram/data_mining_project/blob/master/ERD_Diagram.png)

### Usage
To insert data into the database, use  (at least) the command:  
python scraper.py -sc
## Support
​
​
orgewe@gmail.com
​
​
## License
​
Copyright (c) [2023] Tal & Or
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
<span style="color: red;">update at the end of milestone3.</span>

python bs4 methods and python requests with use of collecting the information to dictionary,
which the elements are listed by enumerate.
classes which collected from changing website with different elements of HTML Classes.
connecting files to appending JSON file.
scanning values from user.
analyzing and moving data and creating databases 
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
Tal Ramon [Linkin link](https://www.linkedin.com/in/talramon/)
  
​
Or gewelber [Linkin link](https://www.linkedin.com/in/or-gewelber/)
 
​
​
## Acknowledgements
​
ITC - Israel Tech Challenge

![image](data:image/jpeg;base64,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)

Feel free to modify or expand upon any section based on your project's specifics.
This enhanced README provides a more detailed and organized structure for users, 
contributors, and maintainers of the project.

