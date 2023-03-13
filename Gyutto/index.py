import re
import requests
import time
from bs4 import BeautifulSoup

# Please run twice with different page_url!
id_target = "260629"
# id_target = "3193671"

f = open("data.csv", "w+")
s = requests.Session()
s.get("http://gyutto.com/adult_check.php?_adult_check=yes&url=&ref_path=/KspotController.php")
status = True
page_num = 1
while status == True:
    list_url = "http://gyutto.com/search/search_list.php?genre_id=20738&category_id=10&set_category_flag=1&pageID=" + str(page_num)
    # list_url = "https://gyutto.com/search/search_list.php?genre_id=19560&category_id=10&set_category_flag=1&pageID=" + str(page_num)
    print("Processing page: " + str(page_num))
    time.sleep(0.2)
    list_page = s.get(list_url)
    list_soup = BeautifulSoup(list_page.text, "html.parser")
    item_list = list_soup.find_all("dd", class_="DefiPhotoName")
    for item in item_list:
        item_url = item.find_all("a")[0]["href"]
        if id_target in item_url:
            status = False
            break
        time.sleep(0.2)
        page = s.get(item_url)
        soup = BeautifulSoup(page.text, "html.parser")
        item_id = re.findall(r'item(.*)', item_url)[0]
        print("Processing Item: " + item_id)
        item_table = soup.find_all("div", class_="unit_DetailBasicInfo")[
            0].find_all("dt")
        for item_t in item_table:
            if item_t.text == "サークル":
                item_author = item_t.parent.find_all("dd")[0].find_all("a")[0].text
            elif item_t.text == "配信開始日":
                item_date = item_t.parent.find_all("dd")[0].text
        item_title = soup.find_all("h1")[0].text.replace("\xa0", "")
        f.write("Gyutto|" + item_id + "|" + item_author + "|" + item_title + "|" + item_date + "\n")
    page_num += 1
f.close()
