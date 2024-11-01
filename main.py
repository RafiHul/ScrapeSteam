from json.decoder import JSONDecodeError
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time
import requests

limit = int(input("Data Limit : ")) + 1
chrome_driver_path = r"chrome driver path"
main_url = "https://store.steampowered.com/search/?sort_by=_ASC&hidef2p=1&filter=topsellers&supportedlang=english"
json_name = "data.json"

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
driver.get(main_url)

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "search_result_row"))
    )
except:
    print("Halaman tidak termuat dengan sempurna.")
    driver.quit()


driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

find_links = soup.find_all("a", {"class": "search_result_row ds_collapse_flag"})
find_final_price = soup.find_all("div",{"class":"discount_final_price"})

n = 0
for i,j in zip(find_links, find_final_price):
    url: str = i.get("href")
    response = requests.get(url, headers={"UserAgents": UserAgent().chrome})
    soup = BeautifulSoup(response.text, "html.parser")
    get_title_from_url = url.split("/")[5]
    try:
        # get game details
        find_img = soup.find("img",{"class":"game_header_image_full"})
        find_title = soup.find("div", {"class": "apphub_AppName"})
        find_description = soup.find("div",{"class":"game_description_snippet"})
        find_realese_date = soup.find("div",{"class":"date"})
        img_url = find_img.get("src")

        price_fixed = j.text.replace("Rp","").replace(" ","")

        data = {
            "id": n,
            "title": find_title.text,
            "price": price_fixed,
            "short_desk": find_description.text.strip(),
            "date": find_realese_date.text,
            "img_src_name": get_title_from_url
        }

        #saving image
        with open(f"image\\{get_title_from_url}.jpg","wb") as file:
            response_img = requests.get(img_url)
            file.write(response_img.content)

        try:
            with open(json_name,"r",encoding="utf-8") as read_json:
                existing_data = json.load(read_json)
        except:
            existing_data = []

        #json dummy
        existing_data.append(data)

        with open(json_name,"w",encoding="utf-8") as write_json:
            json.dump(existing_data,write_json,ensure_ascii=False,indent=4)

        n += 1
        if n == limit:
            break

        print(f"Success {find_title.text}")

    except AttributeError:
        continue



