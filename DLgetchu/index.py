import requests
from bs4 import BeautifulSoup

date_target = "2023年02月28日"

status = True
page_num = 1
f = open("data.csv", "w+")
s = requests.Session()
s.get("https://dl.getchu.com/adult_check.php?_adult_check=yes&url=gcoslh%2F&ref_path=/")
while status == True:
    url = "https://dl.getchu.com/search/search_list.php?action=search&search_keyword=&perPage=50&search_all_genre_id%5B3%5D%5B159%5D=30223&remove_search_keyword=&btnSearch=%B8%A1%BA%F7&dojin=1&pageID=" + \
        str(page_num)
    page = s.get(url)
    print("Processing page: " + str(page_num))
    soup = BeautifulSoup(page.text, "html.parser")
    items = soup.find_all("table", {"width": 553})
    for item in items:
        item_date = item.find_all("td")[1].find_all("table")[0].find_all("tr")[
            2].find_all("td")[1].text.replace("\n", "")
        if item_date == date_target:
            status = False
            print("Task completed.")
            break
        else:
            item_url = item.find_all("td")[1].find_all("div")[
                0].find_all("a")[0]["href"]
        item_id = item_url[28:]
        print("Processing item: " + item_id)
        item_author = item.find_all("td")[1].find_all("div")[
            0].find_all("a")[1].text
        item_title = item.find_all("td")[1].find_all("div")[
            0].find_all("a")[0].text
        f.write("DLgetchu|" + item_id + "|" + item_author +
                "|" + item_title + "|" + item_date + "\n")
    page_num += 1
f.close()
