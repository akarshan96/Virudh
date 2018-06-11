import requests
from bs4 import BeautifulSoup


def scrape_link(news_text_list, url):
    match_count = 0
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    site_text = soup.get_text(strip=True)

    for word in news_text_list:
        if word in site_text:
            match_count += 1
    return match_count / len(news_text_list)


def news_source(link):
    # 1 -> trusted
    # 0 -> non-trusted

    with open("trusted_sources" + ".txt", mode='r') as f:
        trusted_sources = f.read()
        trusted_sources = eval(trusted_sources)
        for key in trusted_sources:
            if trusted_sources[key] in link:
                return key, 1
    return link, 0


special_character_dict = {
    "!": "%21",
    "#": "%23",
    "$": "%24",
    "&": "%26",
    "'": "%27",
    "(": "%28",
    ")": "%29",
    "*": "%2A",
    "+": "%2B",
    ",": "%2C",
    "-": "%2D",
    ".": "%2E",
    "/": "%2F",
    ":": "%3A",
    ";": "%3B",
    "<": "%3C",
    "=": "%3D",
    ">": "%3E",
    "?": "%3F",
    "@": "%40",
    "[": "%5B",
    "]": "%5D",
    "^": "%5E",
    "_": "%5F",
    "`": "%60",
    "{": "%7B",
    "|": "%7C",
    "}": "%7D",
    "~": "%7E",
}


def perform_hard_tests(news_text):
    link_list = []
    listt = []
    master_list = []
    news_text = news_text.replace("%", " %25 ")

    for character in news_text:
        if character in special_character_dict:
            news_text = news_text.replace(character, " " + special_character_dict[character])
    news_text = news_text.split(" ")
    url = 'https://www.google.co.in/search?q='
    for keyword in news_text:
        url = url + keyword + "+"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    a_tags = soup.findAll("a")

    for a_tag in a_tags:
        if a_tag['href'].startswith('/url?q=') and 'webcache.googleusercontent.com' not in a_tag['href']:
            link = a_tag['href'].split('/url?q=')[1].split('&')[0]
            if link not in link_list:
                link_list.append(link)
                print(link_list)
                match_percentage = scrape_link(news_text, link)
                listt.append((link, match_percentage))

    listt = sorted(listt, key=lambda x: x[1], reverse=True)
    listt =listt[:3]
    for element in listt:
        source, status = news_source(element[0])
        master_list.append({"link": element[0], "match_percentage": element[1], "source": source, "source_status": status})
    return master_list

#a = perform_hard_tests("""Congress president Rahul Gandhi on sunday said the government would be able to instil faith among the young only by competing with China in creating jobs, and asserted the issue would be the central theme for India in the coming years.
#""")
#print(a)