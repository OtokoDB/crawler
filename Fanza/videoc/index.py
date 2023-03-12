import requests
from bs4 import BeautifulSoup
f = open("url.txt", "r+")
g = open("data.csv", "w+")
s = requests.Session()
s.get("https://www.dmm.co.jp/age_check/=/declared=yes/?rurl=https%3A%2F%2Fwww.dmm.co.jp%2Ftop%2F")
while True:
    url = f.readline().strip("\n")
    if url == "":
        print("Task completed.")
        break
    else:
        page = s.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    item_title = soup.find_all("h1")[0].text
    item_table = soup.find_all("td", class_="nw")
    for item_t in item_table:
        if item_t.text == "配信開始日：":
            item_date = item_t.parent.find_all(
                "td")[1].text.replace("\n", "").replace("/", "-")
        elif item_t.text == "レーベル：":
            item_author = item_t.parent.find_all("td")[1].text
        elif item_t.text == "品番：":
            item_id = item_t.parent.find_all("td")[1].text
            print("Processing item: " + item_id)
    g.write("Fanza|" + item_id + "|" + item_author + "|" + item_title + "|" + item_date + "\n")
f.close()
g.close()
