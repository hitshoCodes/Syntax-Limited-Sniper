import requests
import time
import os
from bs4 import BeautifulSoup

cookie_value = "chy0WsrbmGHJBdYaUTIGRz9h4SyYPuaCPImdYulrrfRwtdU6TbEf6mBJwTy3wrDMp6l24VLczxdY8jC0YsRcq0WXk0sBb6AWZTmnmV4WxfbgEFsb5BaxUg0VdD6x7EwEmU55GE3PTDsZQpjhSIPueYdCRSwSlm1yFOlCn8JDjMJYE6l3YSDdi7HZJYfi1sO1jEvCy6RmjCU2bVgsDYMT4x8izvlwpQ7Ohd23UJrNlH9yxFjzsVxmZK1opFg5JqNDnSG7GE0djgdAVzA5v5ioikK2JDLP5Gjkr13HtlU8XJBwj1Lt9WcUKbvUudl0Sn1HUPZfKbrGtm8raYg1RLjUgnsCV7AbwiwdyBL4cbsgHeJ5FwrFzCI7Jb5totwHTY08fwnYdYkoyIaKaFyYhCVcwcyECNiwAtfS02LyvqrzjkLqXWLZj9K9fVaMq0ghpErz79pMSxrlKMlNJPloncJS0Ah6IwBmFt7BkiVWb9BgaxLYiVWRtOTIxxrpm1TSh03n"

headers = {
    "Cookie": f".ROBLOSECURITY={cookie_value}"
}

url = "https://www.syntax.eco/catalog/?sort=3&catergory=5"

while True:
    table = []
    table.clear()

    os.system('cls' if os.name == 'nt' else 'clear')

    print("[!] Sending request to the website...")
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    elements = soup.find_all(class_="col-md-2 col-3 p-1")

    links = [element.a["href"].split("/")[2] for element in elements]

    for link in links:
        table.append(link)

    print(f"Autosearch: {table}")

    if table:
        with open("current.txt", "w") as file:
            file.write(table[0])

    time.sleep(5)
