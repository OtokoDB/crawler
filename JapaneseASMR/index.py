import requests
from bs4 import BeautifulSoup

date_target = "2023-02-28"

status = True
s = requests.Session()
f = open("url-download.txt", "w+")
page_num = 1
while status == True:
    url = "https://japaneseasmr.com/page/" + str(page_num)
    print("Processing page: " + str(page_num))
    page = s.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    items = soup.find_all("div", class_="entry-preview-wrapper")
    for item in items:
        item_date = item.find_all("time")[0]["datetime"]
        if item_date == date_target:
            status = False
            print("Task completed.")
            break
        else:
            item_url = item.find_all(
                "h2", class_="entry-title")[0].find_all("a")[0]["href"]
        print("Processing item: " + item_url[25:-1])
        item_page = s.get(item_url)
        item_soup = BeautifulSoup(item_page.text, "html.parser")
        item_dl_list = item_soup.find_all("p", id="downloadlink")
        for item_dl in item_dl_list:
            item_dl_url = item_dl.find_all("a")[0]["href"]
            if "dla.php" in item_dl_url:
                continue
            else:
                f.write(item_dl_url + "\n")
    page_num += 1
f.close()
