import requests
import time
import os
from bs4 import BeautifulSoup

cookie_value = "PUT YOUR COOKIE HERE"

# Create headers with the cookie value
headers = {
    "Cookie": f".ROBLOSECURITY={cookie_value}"
}

# Make a GET request to the website
url = "https://www.syntax.eco/catalog/?sort=3&catergory=5"

while True:
    time.sleep(1)
    table = []
    table.clear()

    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        print("[!] Sending request to the website...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all elements with class "col-md-2 col-3 p-1"
        elements = soup.find_all(class_="col-md-2 col-3 p-1")

        # Extract the links from the elements and strip the IDs
        links = [element.a["href"].split("/")[2] for element in elements]

        # Add each ID to the table
        for link in links:
            table.append(link)

        # Print the table
        print(f"Autosearch: {table}")

        # Check if the table is not empty
        if table:
            # Open the file in write mode and clear its contents
            with open("current.txt", "w") as file:
                # Write the first element of the table to the file
                file.write(table[0])
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        print("Waiting for internet connection...")
        time.sleep(10)  # Wait for 10 seconds before retrying
