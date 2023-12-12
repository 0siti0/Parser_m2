import requests
from bs4 import BeautifulSoup


def parse_html(url):  # Парсинг Html страницы(Потом понадобиться)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        parts = soup.find("body")
        textsite = []

        for part in parts:
            textsite.append(part.text.replace("\n", "").replace("\r", "").replace("\xa0", ""))
        textsite = [i for i in textsite if i]
        for i in textsite:
            print(i)
    else:
        print("Ошибка при получении страницы:", response.status_code)


def parse_links(url):  # Парсинг ссылок
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers)

    if response.status_code == 200:

        soup = BeautifulSoup(response.content, 'html.parser')
        parts = soup.find_all("a")
        htmltext = []
        for part in parts:
            attrLink = str(part).split("\"")
            i = 0
            while i < len(attrLink):
                if attrLink[i] == ' href=' or attrLink[i] == '<a href=':
                    if attrLink[i+1] != "/":
                        htmltext.append(attrLink[i+1])
                    break
                i+=1

        return htmltext
    else:
        return []


def cheсk_links(root_link, links):
    answer_links = []
    i = 0
    while i < len(links):
        if links[i][0] == '/':
            links[i] = root_link + links[i]
        if len(links[i].replace("/", " ").split(' ')) > 2:
            if links[i].split("/")[0] + "//" + links[i].replace("/", " ").split(' ')[2] == root_link:

                answer_links.append(links[i])
        i += 1
    return answer_links


def generate_links(root_link, links_set):
    answer_set = links_set.copy()
    for link in links_set:
        links = parse_links(link)
        if links != []:
            answer_set.update(cheсk_links(root_link, links))

    if len(links_set) == len(answer_set):
        return answer_set
    else:
        return generate_links(root_link, answer_set)


if __name__ == '__main__':
    links = open("domens.txt", "r")
    links_set = set()
    for link in links:
        root_link = link.split("/")[0] + "//" + link.replace("/", " ").split(' ')[2]
        if parse_links(root_link) != []:
            links_set.update(cheсk_links(root_link, parse_links(root_link)))
            links_set.update(generate_links(root_link, links_set))
        else:
            links_set.update(cheсk_links(root_link, parse_links(link)))
            links_set.update(generate_links(root_link,links_set))
    for link in links_set:
        print(link)
