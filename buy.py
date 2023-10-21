from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def process_new_ids():
    with open('current.txt', 'r') as file:
        item_ids = file.read().splitlines()

    with open('bought.txt', 'r') as file:
        bought_ids = file.read().splitlines()

    # Filter out the item IDs that are already in the 'bought' list
    new_item_ids = [id for id in item_ids if id not in bought_ids]

    if not new_item_ids:
        print("No new IDs to process.")
        return

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36")

    driver = webdriver.Chrome(options=options)

    cookie_name = ".ROBLOSECURITY"
    cookie_value = "chy0WsrbmGHJBdYaUTIGRz9h4SyYPuaCPImdYulrrfRwtdU6TbEf6mBJwTy3wrDMp6l24VLczxdY8jC0YsRcq0WXk0sBb6AWZTmnmV4WxfbgEFsb5BaxUg0VdD6x7EwEmU55GE3PTDsZQpjhSIPueYdCRSwSlm1yFOlCn8JDjMJYE6l3YSDdi7HZJYfi1sO1jEvCy6RmjCU2bVgsDYMT4x8izvlwpQ7Ohd23UJrNlH9yxFjzsVxmZK1opFg5JqNDnSG7GE0djgdAVzA5v5ioikK2JDLP5Gjkr13HtlU8XJBwj1Lt9WcUKbvUudl0Sn1HUPZfKbrGtm8raYg1RLjUgnsCV7AbwiwdyBL4cbsgHeJ5FwrFzCI7Jb5totwHTY08fwnYdYkoyIaKaFyYhCVcwcyECNiwAtfS02LyvqrzjkLqXWLZj9K9fVaMq0ghpErz79pMSxrlKMlNJPloncJS0Ah6IwBmFt7BkiVWb9BgaxLYiVWRtOTIxxrpm1TSh03n"

    driver.get("https://www.syntax.eco")

    driver.add_cookie({"name": cookie_name, "value": cookie_value})

    for id in new_item_ids:
        url = f"https://www.syntax.eco/catalog/{id}/"
        driver.get(url)

        try:
            take_one_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.btn.btn-primary.fw-bold.w-100.btn-sm.purchase-button')))
          
            take_one_button.click()

            print(f"Clicked 'Take One' button for ID: {id}")

            time.sleep(1)

            purchase_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'purchase-modal-btn')))

            purchase_button.click()

            print(f"Clicked 'Purchase' button for ID: {id}")

            with open('bought.txt', 'a') as bought_file:
                bought_file.write(id + '\n')

        except Exception as e:
            print(f"Error for ID {id}: {e}")
            print(f"Element not found or couldn't be clicked for ID: {id}")

    driver.quit()

while True:
    process_new_ids()
    time.sleep(1)