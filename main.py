import json
import requests
import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import datetime
import socket

with open('settings.json', 'r') as settings_file:
    settings = json.load(settings_file)

AUTOSEARCH_COOKIE = settings["AUTOSEARCH_COOKIE"]
BUY_COOKIE = settings["BUY_COOKIE"]
CHECK_TIME = settings["CHECK_TIME"]
ANONYMOUS = settings["HIDE_ACCOUNT_NAME"]
DISCORD_WEBHOOK = settings["DISCORD_WEBHOOK"]
bought = 0
checks = 0
errors = 0
account = "None"
autosearch_status = "Disconnected"
last_bought = "None"
last_detected = "None"

account_api = "https://www.syntax.eco/public-api/v1/users/my-profile"

def check_buyacc():
    global account
    requests_headers = {
        "Cookie": f".ROBLOSECURITY={BUY_COOKIE}"
    }
    try:
        response = requests.get(account_api, headers=requests_headers)
        response.raise_for_status()  # Check for request errors

        if response.status_code == 200:
            data = response.json()

            username = data.get("data", {}).get("username")
            if username:
                account = username
            else:
                account = "None"
    except requests.exceptions.RequestException as e:
        account = "None"

check_buyacc()

while ANONYMOUS == True:
    account = "Hidden"

def check_searchacc():
    global autosearch_status
    requests_headers = {
        "Cookie": f".ROBLOSECURITY={AUTOSEARCH_COOKIE}"
    }
    try:
        response = requests.get(account_api, headers=requests_headers)
        response.raise_for_status()  # Check for request errors

        if response.status_code == 200:
            data = response.json()

            username = data.get("data", {}).get("username")
            if username:
                autosearch_status = "Connected"
            else:
                autosearch_status = "Disconnected"
    except requests.exceptions.RequestException as e:
        autosearch_status = "Disconnected"

def update_autosearch():
    check_searchacc()
    time.sleep(600)

url = "https://www.syntax.eco/catalog/?sort=3&catergory=5"

logs = []
current_id = None

logs_file = open('logs.txt', 'w')

def log(message):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{message}"
    logs.append(log_entry)
    
    logs_file.write(current_time + log_entry + '\n')
    logs_file.flush()

def scrape_item_links():
    requests_headers = {
        "Cookie": f".ROBLOSECURITY={AUTOSEARCH_COOKIE}"
    }
    try:
        response = requests.get(url, headers=requests_headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        elements = soup.find_all(class_="col-md-2 col-3 p-1")
        links = [element.a["href"].split("/")[2] for element in elements]

        return links
    except requests.exceptions.RequestException as e:
        log("    \033[0m[\033[31m!\033[0m] \033[38;5;69mInternet connection was lost")
        time.sleep(10)

def is_internet_available():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

def process_new_ids():
    global current_id, checks, CHECK_TIME, bought, errors, last_bought, last_detected, DISCORD_WEBHOOK

    while True:
        while not is_internet_available():
            print("No internet connection. Waiting for 1 minute before checking again...")
            time.sleep(60)
        
        time.sleep(CHECK_TIME)
        checks = checks + 1

        new_item_links = scrape_item_links()

        if new_item_links is not None:
            current_id = new_item_links[0]

            with open('bought.txt', 'r') as file:
                bought_ids = file.read().splitlines()

            new_item_ids = [id for id in new_item_links if id not in bought_ids]

            if new_item_ids:
                options = webdriver.ChromeOptions()
                options.add_argument("--start-maximized")
                options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36")

                driver = webdriver.Chrome(options=options)

                cookie_name = ".ROBLOSECURITY"

                driver.get("https://www.syntax.eco")

                driver.add_cookie({"name": cookie_name, "value": BUY_COOKIE})

                for id in new_item_ids:
                    url = f"https://www.syntax.eco/catalog/{id}/"
                    driver.get(url)

                try:
                    take_one_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.btn.btn-primary.fw-bold.w-100.btn-sm.purchase-button')))
                  
                    take_one_button.click()

                    log(f"    \033[0m[\033[31m!\033[0m] \033[38;5;69mAutosearch detected {id}")

                    time.sleep(1)

                    purchase_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'purchase-modal-btn')))

                    purchase_button.click()

                    log(f"    \033[0m[\033[32m+\033[0m] \033[38;5;69mSuccessfully bought {id}")
                    bought = bought + 1

                    last_bought = get_item_name(id)

                    webhook_url = DISCORD_WEBHOOK

                    embed = {
                        "title": "New Snipe!",
                        "description": f"Account: {account}\nPurchased: [{last_bought}](https://syntax.eco/catalog/{id}/hitshoCodes)",
                        "color": 7506394,
                        "footer": {
                            "text": f"hitshoCodes Syntax Sniper v{version}"
                        }
                    }

                    payload = {
                        "username": "Syntax Sniper",
                        "avatar_url": "https://i.ibb.co/ft4Ck3s/favicon-1.png",
                        "embeds": [embed]
                    }

                    if webhook_url:
                        response = requests.post(webhook_url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
                        if not response.status_code == 204:
                            log(f"    \033[0m[\033[31m!\033[0m] \033[38;5;69mFailed to send the webhook")

                    with open('bought.txt', 'a') as bought_file:
                        bought_file.write(id + '\n')

                except Exception as e:
                    log(f"    \033[0m[\033[37m?\033[0m] \033[38;5;69mUnable to purchase {id}")
                    errors = errors + 1
                    with open('bought.txt', 'a') as bought_file:
                        bought_file.write(id + '\n')

                last_detected = get_item_name(id)

                driver.quit()



def get_item_name(id):
    item_api = f"https://www.syntax.eco/public-api/v1/asset/{id}"
    requests_headers = {
        "Cookie": f".ROBLOSECURITY={AUTOSEARCH_COOKIE}"
    }
    try:
        response = requests.get(item_api, headers=requests_headers)
        response.raise_for_status()

        if response.status_code == 200:
            data = response.json()
            name = data.get("data", {}).get("name")
            return name
    except requests.exceptions.RequestException as e:
        return "Unknown"

def status_update():
    global logs, checks, bought, errors, account, autosearch_status, last_bought, last_detected
    build = "Beta"
    version = "2.0.0"

    while True:
        print("""\033[38;5;69m
                                                                                      d8,                          
                                       d8P                                            `8P                           
                                    d888888P                                                                        
         .d888b,?88   d8P   88bd88b   ?88'   d888b8b  ?88,  88P     .d888b,  88bd88b   88b?88,.d88b, d8888b  88bd88b
         ?8b,   d88   88    88P' ?8b  88P   d8P' ?88   `?8bd8P'     ?8b,     88P' ?8b  88P`?88'  ?88d8b_,dP  88P'  `
           `?8b ?8(  d88   d88   88P  88b   88b  ,88b  d8P?8b,        `?8b  d88   88P d88   88b  d8P88b     d88     
        `?888P' `?88P'?8b d88'   88b  `?8b  `?88P'`88bd8P' `?8b    `?888P' d88'   88bd88'   888888P'`?888P'd88'     
                       )88                                                                  88P'                    
                      ,d8P                                                                 d88                      
                   `?888P'                                                                 ?8P                      
""")
        print()
        print("\033[0m> Info:")
        print(f"    \033[0m> Account: \033[38;5;69m{account}")
        print(f"    \033[0m> Version: \033[38;5;69m{version}")
        print(f"    \033[0m> Build: \033[38;5;69m{build}")
        print()
        print("\033[0m> Autosearch:")
        print(f"\033[0m    > Status: \033[38;5;69m{autosearch_status}")
        print(f"\033[0m    > Last Detected: \033[38;5;69m{last_detected}")
        print(f"\033[0m    > Last Bought: \033[38;5;69m{last_bought}")
        print()
        print("\033[0m> Stats:")
        print(f"    > Checks: \033[38;5;69m{checks}\033[0m")
        print(f"    > Bought: \033[38;5;69m{bought}\033[0m")
        print(f"    > Errors: \033[38;5;69m{errors}\033[0m")
        print()
        print(f">> Logs: \033[38;5;69m\n" + "\n".join(log for log in logs[-10:]))

        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    process_thread = threading.Thread(target=process_new_ids)
    status_thread = threading.Thread(target=status_update)
    update_thread = threading.Thread(target=update_autosearch)
    

    process_thread.start()
    status_thread.start()
    update_thread.start()

    process_thread.join()
    status_thread.join()
    update_thread.join()
