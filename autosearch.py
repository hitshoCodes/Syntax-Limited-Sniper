import requests
import time
import os
from bs4 import BeautifulSoup

cookie_value = "PUT YOUR COOKIE HERE"

headers = {
    "Cookie": f".ROBLOSECURITY={cookie_value}"
}

url = "https://www.syntax.eco/catalog/?sort=3&catergory=5"

while True:
    time.sleep(1)
    table = []
    table.clear()

    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        print("[!] Sending request to the website...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        elements = soup.find_all(class_="col-md-2 col-3 p-1")

        links = [element.a["href"].split("/")[2] for element in elements]

        for link in links:
            table.append(link)

        print(f"Autosearch: {table}")

        if table:
            with open("current.txt", "w") as file:
                file.write(table[0])
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        print("Waiting for internet connection...")
        time.sleep(10)
