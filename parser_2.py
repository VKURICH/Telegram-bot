import requests
from bs4 import BeautifulSoup

host = 'https://www.povarenok.ru/'
url = 'https://www.povarenok.ru/recipes/category/6/'

Headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 OPR/69.0.3686.95'
}

def get_html(url, page = 1, params=''):
    r = requests.get(url + str(page), headers=Headers, params = params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('article', class_ = 'item-bl')
    recipes = []
    for item in items:
        ingredients = item.find('span', class_='list').find_all('a')
        list = '🥐Ингредиенты:  '
        for i in range(len(ingredients) - 1):
            list += ingredients[i].get_text(strip=True) + ', '
        list += ingredients[len(ingredients) - 1].get_text(strip=True)
        recipes.append(
            {
                'caption': item.find('h2').get_text(strip=True),
                'link_product': item.find('div', class_='desktop-img').find('a').get('href'),
                'info-item': list,
                'dish_img': item.find('div', class_='desktop-img').find('img').get('src')
            }
        )
    return recipes

# Парсим страницу
def parser(url, pagenation):
    html = get_html(url)
    if html.status_code == 200:
        recipes = []
        list_titles = []
        for page in range(pagenation, pagenation+1):
            html = get_html(url,page, params= {'': page})
            recipes.extend(get_content(html.text))
            for i in range(len(recipes)):
                list_titles.append(recipes[i]['caption'])
        return list_titles, recipes
    else:
        print('Error')