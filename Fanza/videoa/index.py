import requests
from bs4 import BeautifulSoup

id_target = "btis00126"

f = open("data.csv", "w+")
s = requests.Session()
s.get("https://www.dmm.co.jp/age_check/=/declared=yes/?rurl=https%3A%2F%2Fwww.dmm.co.jp%2Ftop%2F")
status = True
page_num = 1
while status == True:
    page_url = "https://www.dmm.co.jp/digital/videoa/-/list/=/article=keyword/id=3036/sort=date/page=" + \
        str(page_num)
    print("Processing page: " + str(page_num))
    index_page = s.get(page_url)
    index_soup = BeautifulSoup(index_page.text, "html.parser")
    items = index_soup.find_all("p", class_="tmb")
    for item in items:
        url = item.find_all("a")[0]["href"]
        if id_target in url:
            status = False
            print("Task completed.")
            break
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
        f.write("Fanza|" + item_id + "|" + item_author + "|" + item_title + "|" + item_date + "\n")
    page_num += 1
f.close()
