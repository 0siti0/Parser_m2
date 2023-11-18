import requests

from bs4 import BeautifulSoup


def scrape_hydraulic_parts(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        parts = soup.find("body")
        textsite = []

        for part in parts:
            textsite.append(part.text.replace("\n","").replace("\r","").replace("\xa0",""))
        textsite = [i for i in textsite if i]
        for i in textsite:
            print(i)
    else:
        print("Ошибка при получении страницы:", response.status_code)


if __name__ == '__main__':
    scrape_hydraulic_parts(
        "https://smgarant.by/index.pl?act=SUBJ&subj=zapchasti+gidronasosov+VOLVO&section=zapchasti+gidronasosov+VOLVO")
