import os
import time
import gspread
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from oauth2client.service_account import ServiceAccountCredentials

# Load credentials
load_dotenv()
AMAZON_EMAIL = os.getenv("AMAZON_EMAIL")
AMAZON_PASSWORD = os.getenv("AMAZON_PASSWORD")

# Google Sheets Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("AmazonOrders").sheet1
rows = sheet.get_all_records()

# Selenium Setup
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Login to Amazon
def login_amazon():
    driver.get("https://www.amazon.com")
    time.sleep(2)
    driver.find_element(By.ID, "nav-link-accountList").click()
    time.sleep(2)
    driver.find_element(By.ID, "ap_email").send_keys(AMAZON_EMAIL)
    driver.find_element(By.ID, "continue").click()
    time.sleep(1)
    driver.find_element(By.ID, "ap_password").send_keys(AMAZON_PASSWORD)
    driver.find_element(By.ID, "signInSubmit").click()
    time.sleep(5)

# Add product to cart
def add_to_cart(url):
    driver.get(url)
    time.sleep(3)
    try:
        driver.find_element(By.ID, "add-to-cart-button").click()
        time.sleep(3)
        print(f"Added to cart: {url}")
    except Exception as e:
        print(f"Failed to add {url}: {e}")

# Main bot execution
login_amazon()

for row in rows:
    add_to_cart(row["ProductURL"])

driver.quit()
