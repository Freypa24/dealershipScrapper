from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import database
import time
import re

# Set up Chrome options (e.g., headless mode)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (without opening a browser window)

# Automatically download and use the correct version of chromedriver
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://philkotse.com/used-cars-for-sale")


soup = BeautifulSoup(driver.page_source, 'html.parser')
links = soup.find_all("div", class_="col-4")
main_url = "https://philkotse.com/used-cars-for-sale/p"
car_url = "https://philkotse.com/"
page_number = 2


def extract_car_details(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(url)
    #time.sleep(.2)
    car_details_div = soup.find("div", class_="parameter-info")
    if not car_details_div:
        print("Error occured for this listing")
        return

    price_tag = " "

    # This means that a price tag has been discounted.
    if soup.find("div", class_="new-total-pay"):
        price_tag = car_details_div.find("div", class_="price").text.strip()  # Find the first price element
    else:
        price_tag = car_details_div.find("span", class_="price").text.strip()  # Find the first price element
    print(price_tag)
    car_details = car_details_div.find("ul", class_="list")
    brand, model, year, status, color, transmission = "None", "None", "None", "None", "None", "None"

    for car in car_details:
        details = car_details.find_all("li")
        for i in range(len(details)):
            text = details[i].text.strip()

            brand = details[0].text.strip()
            model = details[1].text.strip()
            if year == "None" and re.match(r"\d{4}", text):
                year = text
            elif status == "None" and text == "Used" or text == "New":
                status = text
            elif color == "None" and text == "Beige" or text == "Black" or text == "Blue" or text == "Brightsilver" or text == "Brown" or text == "Cream" or text == "Golden" or text == "Grayblack" or text == "Green" or text == "Grey" or text == "Orange" or text == "Pearlwhite" or text == "Pink" or text == "Purple" or text == "Red" or text == "Silver" or text == "Skyblue" or text == "White"  or text == "Yellow" or text == "Other":
                color = text
            elif transmission == "None" and text == "Automatic" or text == "Manual":
                transmission = text
        print(f"Brand: {brand}, Model: {model}, Year: {year}, Status: {status}, Color: {color}, transmission: {transmission}")
        database.insert_car(brand, model, year, status, color, transmission, price_tag, url)
        break


# grab the first page's car listing
for div in links:
    a_tag = div.find("a")
    if a_tag and a_tag.get("href"):
        full_url = car_url + a_tag["href"]
        extract_car_details(full_url)


# This grabs every listing in the main page / used cars for sale page
while True:
    driver.get(f"{main_url}{page_number}")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #time.sleep(.2)
    links = soup.find_all("div", class_="col-4")
    for div in links:
        a_tag = div.find("a")
        if a_tag and a_tag.get("href"):
            full_url = car_url + a_tag["href"]
            extract_car_details(full_url)
    if not links:
        print(f"No more listings found on page {page_number}. Stopping.")
        break  # Exit loop if no listings found
    page_number += 1



driver.quit()
