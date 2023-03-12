import re
import requests
from bs4 import BeautifulSoup
f = open("url.txt", "r+")
g = open("data.csv", "w+")
s = requests.Session()
while True:
    url = f.readline().strip("\n")
    if url == "":
        print("Task completed.")
        break
    else:
        page = s.get(url)
    print("Processing item: " + url)
    soup = BeautifulSoup(page.text, "html.parser")
    item_sou = soup.find_all("div", {"data-work_type": "SOU"})[0]
    item_title = item_sou["data-work_name"]
    item_id = item_sou["data-product_id"]
    item_author = soup.find_all("span", {"itemprop": "brand"})[
        0].find_all("a")[0].text
    item_table = soup.find_all("table", id="work_outline")[0].find_all("th")
    for item_t in item_table:
        if item_t.text == "販売日":
            item_date = item_t.parent.find_all("td")[0].find_all("a")[0].text
    g.write("DLsite|" + item_id + "|" + item_author + "|" + item_title + "|" + item_date + "\n")
f.close()
g.close()
