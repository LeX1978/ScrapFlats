import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

Pages = []
page_list = set()
url = "https://www.cian.ru/cat.php?currency=2&deal_type=sale&demolished_in_moscow_programm=0&engine_version=2&is_first_floor=0&maxprice=24000000&mintarea=80&object_type%5B0%5D=1&offer_type=flat&only_flat=1&p=1&region=1&room3=1"
stop_flag = False

# Установка соединения с сайтом
def setConnection(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.2.644 Yowser/2.5 Safari/537.36',
    	       'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
    session = requests.Session()
    try:
        response = session.get(url, headers = headers)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occured: {http_err}')
    except Exception as err:
        print(f'Other error occured: {err}')
    else:
        return response

def pageLinks(url):
    resp = setConnection(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    Pages = soup.findAll("a", {'class': '_93444fe79c--list-itemLink--BU9w6'})
    for p_link in Pages:
        page_num = p_link.text
        if 'href' in p_link.attrs:
            link = p_link.attrs['href']
            if "https://www.cian.ru" not in link:
                link = "https://www.cian.ru" + link
        if page_num == "..":
            url = link
        else:
            page_list.add(link)
    return url

# Поцедура получения информации о квартирах на странице
def getFlatInfo(url):
    cl = ''
    resp = setConnection(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    # Находим все блоки с информацией о квартире
    Blocks = soup.findAll("div", {'data-name': 'LinkArea'})
    for block in Blocks:
        # Определяем ссылку на конкретную квартиру
        linkflat = block.find('a', class_='_93444fe79c--link--eoxce')
        if linkflat is not None:
            if 'href' in linkflat.attrs:
                link = linkflat.attrs['href']
                print(link)
        # Ищем название ссылки
        link_spans = block.find("span", {'class': ''})
        link_text = link_spans.get_text().encode("utf8")
        link_text_decoded = link_text.decode('utf8')
        print(link_text_decoded)

        # Ищем метро
        metro_block = block.findAll("a", {'class': '_93444fe79c--link--BwwJO'})
        for metro in metro_block:
            metro_name = metro.find("div", {'class': ''})
            print(metro_name.text)
        # Ищем цену
        price_block = block.findAll("span", {'data-mark': 'MainPrice'})
        for price in price_block:
            if cl == '':
                price_num = price.find("span", {'class': cl})
            else:
                price_num = price.find("span", {'class': '_93444fe79c--highlighted--TzjBZ'}) _93444fe79c--highlighted--TzjBZ
            print(price_num.text)


while stop_flag is False:
    if url not in page_list:
        page_list.add(url)
        url = pageLinks(url)
    else:
        stop_flag = True

for link in page_list:
    getFlatInfo(link)