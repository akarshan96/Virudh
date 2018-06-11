import requests
from bs4 import BeautifulSoup

response = requests.get("https://blog.feedspot.com/indian_news_websites/")
soup = BeautifulSoup(response.content, "html.parser")
a_tags = soup.findAll("a")
trusted_sources = {}
count = 0
for tag in a_tags:
    count += 1
    if count > 4:
        if tag.text == "Download Badge high resolution image":
            break
        if count % 2 != 0:
            name = tag.text
        else:
            trusted_sources[name] = tag.text
with open("trusted_sources" + ".txt", mode='w') as f:
    f.write(str(trusted_sources))
    f.close()
