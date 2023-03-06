import requests
import zippyshare_downloader
s = requests.Session()
f = open("url-download.txt", "r+")
g = open("url-failed.txt", "w+")
while True:
    url = f.readline().strip("\n")
    if url == "":
        break
    else:
        print("Processing item: " + url[35:])
    zippy_url = s.get(url).url
    if "japaneseasmr" in zippy_url:
        g.write(url + "\n")
        print("Failed.")
    else:
        try:
            zippyshare_downloader.download(zippy_url)
        except BaseException:
            g.write(url + "\n")
            print("Failed.")
        else:
            print("Success.")
f.close()
g.close()
print("Task completed.")
