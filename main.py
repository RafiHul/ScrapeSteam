from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import requests

chrome_driver_path = r"C:\Users\rafih\Desktop\chromedriver-win64\chromedriver.exe"
main_url = "https://store.steampowered.com/search/?sort_by=_ASC&hidef2p=1&filter=topsellers&supportedlang=english"

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

for i,j in zip(find_links, find_final_price):
    response = requests.get(i.get("href"), headers={"UserAgents": UserAgent().chrome})
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        # get game details
        find_img = soup.find("img",{"class":"game_header_image_full"})
        find_title = soup.find("div", {"class": "apphub_AppName"})
        find_description = soup.find("div",{"class":"game_description_snippet"})
        find_realese_date = soup.find("div",{"class":"date"})
        img_url = find_img.get("src")

        price_fixed = j.text.replace("Rp","").replace(" ","")
        print(f"img = {img_url}\ntitle = {find_title.text}\nharga = {price_fixed}\ndeskripsi = {find_description.text.strip()}\ndate = {find_realese_date.text}\n============")

        with open(f"image\\{find_title.text.replace(" ","_").replace("™","")}.jpg","wb") as file:
            response_img = requests.get(img_url)
            file.write(response_img.content)

    except AttributeError:
        continue



