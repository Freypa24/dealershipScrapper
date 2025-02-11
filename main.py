from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import database
import time
import re

chrome_options = Options()
chrome_options.add_argument("--headless")                   # We don't want to see the window for the chrome driver

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://philkotse.com/used-cars-for-sale")


soup = BeautifulSoup(driver.page_source, 'html.parser')
links = soup.find_all("div", class_="col-4")
main_url = "https://philkotse.com/used-cars-for-sale/p"     # pagination links
car_url = "https://philkotse.com/"                          # car links
pageNumber = 2                                             # pagination number, 2 is next page after the main page


def convert_to_integer(num):
    newNum = num.replace("₱", "").replace(",", "").strip()

    try:
        return int(newNum)         # Return as an Integer
    except ValueError:
        return 0                # Failed to convert,

def extract_car_details(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(url)
    #time.sleep(.2)
    car_details_div = soup.find("div", class_="parameter-info")
    if not car_details_div:
        print("Error occured for this listing")
        return

    discountedPrice = ""
    originalPrice = ""

    # This means that a price tag has been discounted.
    if soup.find("div", class_="new-total-pay"):

        discountedPrice = car_details_div.find("div", class_="price").text.strip()  # the discounted value of a listing, if there are any
        originalPrice = car_details_div.find("span", class_="old-price").text.strip()

    else:

        originalPrice = car_details_div.find("span", class_="price").text.strip()   # the true value of the listing

    print(convert_to_integer(discountedPrice))
    print(convert_to_integer(originalPrice))
    car_details = car_details_div.find("ul", class_="list")

    brand, model, year, status, color, transmission = "None", "None", "None", "None", "Unknown", "None"
    for car in car_details:
        details = car_details.find_all("li")
        for i in range(len(details)):
            text = details[i].text.strip()

            brand = details[0].text.strip()
            model = details[1].text.strip()

            if year == "None" and re.match(r"\d{4}", text):
                year = int(text)
            elif status == "None" and text == "Used" or text == "New":
                status = text
            elif color == "Unknown" and text == "Beige" or text == "Black" or text == "Blue" or text == "Brightsilver" or text == "Brown" or text == "Cream" or text == "Golden" or text == "Grayblack" or text == "Green" or text == "Grey" or text == "Orange" or text == "Pearlwhite" or text == "Pink" or text == "Purple" or text == "Red" or text == "Silver" or text == "Skyblue" or text == "White"  or text == "Yellow" or text == "Other":
                color = text
            elif transmission == "None" and text == "Automatic" or text == "Manual":
                transmission = text

        print(f"Brand: {brand}, Model: {model}, Year: {year}, Status: {status}, Color: {color}, transmission: {transmission}")

        # Once all data regarding the car listing has been gathered, move onto the database.
        database.insert_car(brand, model, year, status, color, transmission, convert_to_integer(discountedPrice), convert_to_integer(originalPrice), url)
        break


# grab the first page's car listing.
for div in links:
    a_tag = div.find("a")
    if a_tag and a_tag.get("href"):
        full_url = car_url + a_tag["href"]
        extract_car_details(full_url)



# This grabs every listing in the used cars page until it reaches the end.
while True:
    driver.get(f"{main_url}{pageNumber}")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(.2)
    links = soup.find_all("div", class_="col-4")

    # Repeat that same process of grabbing all car listing for every available pages.
    for div in links:
        a_tag = div.find("a")
        if a_tag and a_tag.get("href"):
            full_url = car_url + a_tag["href"]
            extract_car_details(full_url)

    # THIS WILL END THE SYSTEM, USE THIS AS THE ENDPOINT
    if not links:
        print(f"No more listings found on page {pageNumber}.")
        break
    pageNumber += 1



driver.quit()
