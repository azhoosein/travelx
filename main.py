import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
import time

ADDRESS = ""
CITY = ""
ZIP = ""

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(), logging.FileHandler('process.log')])

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# Load numbers from file
def load_numbers_from_file(filename):
    """Load SIM numbers from a file."""
    try:
        with open(filename, 'r') as file:
            numbers = file.read().splitlines()
        logging.info(f"Loaded {len(numbers)} numbers from {filename}")
        return numbers
    except FileNotFoundError:
        logging.error(f"{filename} not found. Please ensure the file exists.")
        return []


# Load IMEIs from file
def load_imeis_from_file(filename):
    """Load IMEI numbers from a file."""
    try:
        with open(filename, 'r') as file:
            imeis = file.read().splitlines()
        logging.info(f"Loaded {len(imeis)} IMEIs from {filename}")
        return imeis
    except FileNotFoundError:
        logging.error(f"{filename} not found. Please ensure the file exists.")
        return []


chrome_options = Options()
chrome_options.add_argument("--disable-usb")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--force-device-scale-factor=0.6")


def start_browser():
    """Initialize the WebDriver and open the login page."""
    logging.info('Initializing WebDriver...')
    driver = webdriver.Chrome(options=chrome_options)
    time.sleep(1)
    driver.get('https://dealers.prepaidiq.com/login')
    return driver


def login(driver):
    """Log in to the website using the provided credentials."""
    logging.info('Logging in with provided credentials...')
    email_field = driver.find_element(By.NAME, 'email')
    email_field.send_keys(EMAIL)
    time.sleep(1)

    password_field = driver.find_element(By.NAME, 'password')
    password_field.send_keys(PASSWORD)
    time.sleep(1)

    sign_in_button = driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div/div/div/div[2]/form/div[5]/button')
    sign_in_button.click()
    time.sleep(1)


def navigate_to_activation_page(driver):
    """Navigate through the pages to the activation page."""
    logging.info('Navigating to the activation page...')
    activate_button = driver.find_element(By.XPATH, '/html/body/main/div[1]/div[3]/div/div[2]/div/div[1]/a/img')
    activate_button.click()
    time.sleep(1)

    travel_button = driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div[13]/div/div/a/img')
    travel_button.click()
    time.sleep(1)


def fill_out_form(driver, sim, imei):
    """Fill out the user information in the activation form."""
    logging.info(f'Filling out form for SIM: {sim} with IMEI: {imei}...')

    plan_field = driver.find_element(By.ID, 'plan')
    plan_field.click()
    time.sleep(0.5)

    aaa_field = driver.find_element(By.XPATH, '//*[@id="plan"]/option[2]')
    aaa_field.click()
    time.sleep(0.5)

    imei_field = driver.find_element(By.ID, 'imei_0')
    imei_field.send_keys(imei)
    time.sleep(0.5)

    logging.info(f'Entering SIM: {sim}...')
    sim_field = driver.find_element(By.ID, 'eid_sim_0')
    sim_field.send_keys(sim)
    time.sleep(0.5)

    fname_field = driver.find_element(By.ID, 'first_name')
    fname_field.send_keys("TIM")
    time.sleep(0.5)

    lname_field = driver.find_element(By.ID, 'last_name')
    lname_field.send_keys("JOHN")
    time.sleep(0.5)

    emailid_field = driver.find_element(By.ID, 'email')
    emailid_field.send_keys("TIM@GMAIL.COM")
    time.sleep(0.5)

    address_field = driver.find_element(By.ID, 'address')
    address_field.send_keys("1537 CAMBRIA ST")
    time.sleep(0.5)

    city_field = driver.find_element(By.ID, 'city')
    city_field.send_keys("LOS ANGELES")
    time.sleep(0.5)

    driver.execute_script("document.getElementById('state').click()")
    time.sleep(0.5)

    ny_field = driver.find_element(By.XPATH, '//*[@id="choices--state-item-choice-5"]') # for NY, change number after choice- to 33, for CA, change number to 5
    ny_field.click()
    time.sleep(0.5)

    zip_field = driver.find_element(By.NAME, 'zipcode[0]')
    zip_field.send_keys('90017')
    time.sleep(0.5)

    logging.info(f'Form filling complete for {sim}.')


def submit_form(driver):
    """Submit the form to complete the SIM activation."""
    logging.info('Submitting the form...')
    submit_button = driver.find_element(By.ID, 'submitBtn')
    submit_button.click()
    time.sleep(2.25)

def process_numbers(driver, numbers, imeis):
    """Process each number and activate it."""
    imei_usage_counter = 0
    imei_index = 0
    total_numbers = len(numbers)
    total_imeis = len(imeis)

    for i, number in enumerate(numbers):
        sim = number
        imei = imeis[imei_index]
        imei_usage_counter += 1

        fill_out_form(driver, sim, imei)  # Fill out the form first
        submit_form(driver)  # Submit the form after it's filled

        print(f"Processing SIM {i + 1}/{total_numbers} - Remaining SIMs: {total_numbers - (i + 1)}")

        # Reset IMEI counter after 4 activations
        if imei_usage_counter == 4:
            imei_usage_counter = 0
            imei_index += 1
            if imei_index >= len(imeis):  # Exit if we run out of IMEIs
                logging.info('No more IMEIs available to process.')
                break


def main():
    """Main function to run the script."""
    logging.info('Starting the process...')

    # Load numbers and IMEIs from files
    numbers = load_numbers_from_file('sim_numbers.txt')
    imeis = load_imeis_from_file('imeis.txt')

    if not numbers or not imeis:
        logging.error('No numbers or IMEIs to process. Exiting...')
        return

    # Start the browser and log in
    driver = start_browser()
    login(driver)
    navigate_to_activation_page(driver)

    # Process the numbers for activation
    process_numbers(driver, numbers, imeis)

    logging.info('Process completed.')
    driver.quit()


main()
