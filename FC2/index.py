import re
import requests
from bs4 import BeautifulSoup

# Please run twice with different page_url!
id_target = "3193671"
# id_target = "3193671"

f = open("data.csv", "w+")
s = requests.Session()
status = True
page_num = 1
while status == True:
    page_url = "https://adult.contents.fc2.com/search/?tag=%E7%94%B7%E3%81%AE%E5%A8%98&page=" + str(page_num)
    # page_url = "https://adult.contents.fc2.com/search/?tag=%E5%A5%B3%E8%A3%85&page=" + str(page_num)
    print("Processing page: " + str(page_num))
    page = s.get(page_url)
    page_soup = BeautifulSoup(page.text, "html.parser")
    url_list = page_soup.find_all("a", class_="c-cntCard-110-f_itemName")
    for url in url_list:
        if "?tag=" in url["href"]:
            continue
        elif id_target in url["href"]:
            status = False
            break
        else:
            url_fix = "https://adult.contents.fc2.com" + url["href"]
        item_page = s.get(url_fix)
        item_soup = BeautifulSoup(item_page.text, "html.parser")
        item_id = re.findall(r'article/(.*)/', url["href"])[0]
        print("Processing item: " + item_id)
        if "申し訳ありません" in item_soup.find_all("h3")[0].text:
            continue
        else:
            item_header = item_soup.find_all("div", class_="items_article_headerInfo")[0]
        item_author = item_header.find_all(
            "ul")[0].find_all("li")[-1].find_all("a")[0].text
        item_title = item_header.find_all("h3")[0].text
        item_date = item_soup.find_all("div", class_="items_article_Releasedate")[
            0].find_all("p")[0].text.replace("販売日 : ", "")
        f.write("FC2|" + item_id + "|" + item_author + "|" + item_title + "|" + item_date + "\n")
    page_num += 1
f.close()