import re
import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    head = {

            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers = head)
    if not response.ok:
        print(f'Code: {response.status_code}, url: {url}')
    return response.text


def get_games(html):
    soup = BeautifulSoup(html, 'lxml')
    web = r'^https://store.steampowered.com/app/'
    games = soup.find_all('a', href=re.compile(web))
    return games

def write_csv(data):
    with open('./result_3_tags.csv', 'a', encoding="utf-8", newline='') as f:
        fields = [
            'title',
            'platforms',
            'reviews',
            'players',
            'positives',
            'review_summary',
            'released',
            'price',
            'discount',
            'final_price',
            'main_tag',
            'url',
            'all_tags'
        ]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writerow(data)

def get_hover_data(id):
    url = f'https://store.steampowered.com/apphoverpublic/{id}'
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    try:
        title = soup.find('h4', class_='hover_title').text.strip()
    except:
        title = ''

    try:
        released = soup.find('div', class_='hover_release').span.text.split(':')[-1].strip()
    except:
        released = ''

    try:
        reviews_raw = soup.find('div', class_='hover_review_summary').text
    except:
        reviews = ''
    else:
        pattern = r'\d+'
        reviews = int(''.join(re.findall(pattern, reviews_raw)))

    try:
        tags_raw = soup.find_all('div', class_='app_tag')
    except:
        all_tags = ''
        main_tag = ''
    else:
        tags_text = [tag.text for tag in tags_raw]
        if tags_text:
            main_tag = tags_text[0]
            all_tags = ', '.join(tags_text[0:3])
        else:
            main_tag = ''
            all_tags = ''

    data = {
        'title': title,
        'released': released,
        'reviews': reviews,
        'main_tag': main_tag,
        'all_tags': all_tags
    }

    return data

def scrape_game_data(game):

    ## review and positives
    try:
        tooltip_raw = game.find('span', class_='search_review_summary positive').get('data-tooltip-html')
    except:
        review_summary = 'None'
        positives = 0
        players = 0
    else:
        # Very Positive&lt;br&gt;80% of the 719,415 user reviews for this game are positive.
        tr_splitted = tooltip_raw.split('<br>')
        review_summary = tr_splitted[0]
        positives_raw = tr_splitted[1]
        positives = int(positives_raw[:positives_raw.find('%')])
        players = positives_raw[positives_raw.find('the '):positives_raw.find(' user')].replace(',','').replace('the ','')


    ## platforms and titles
    try:
        platforms_raw = game.find('div', class_='col search_name ellipsis')
    except:
        platforms = 'None'
        title = 'None'
    else:
        platforms_os = [platform.get_attribute_list('class')[-1].title() for platform in platforms_raw.find_all('span', class_='platform_img')]
        title = platforms_raw.text.strip()

        platforms = ', '.join(platforms_os)

    ## prices and discounts
    try:
        data_price_raw = game.find('div', class_='col search_price_discount_combined responsive_secondrow').find('div', class_='col search_discount_and_price responsive_secondrow')
        data_discount = data_price_raw.find('div',class_='discount_block search_discount_block no_discount').get('data-discount')  
        data_discount_final_prices = data_price_raw.find('div',class_='discount_final_price').text.strip()
        

    except:
        final_price = 0
        discount = "None"
    else:

        final_price = data_discount_final_prices
        discount = data_discount


    try:
        data_price_raw = game.find('div', class_='col search_price_discount_combined responsive_secondrow').find('div', class_='col search_discount_and_price responsive_secondrow')
        data_discount_final_prices = data_price_raw.find('div',class_='discount_final_price').text.strip()
        data_orignal_prices = data_price_raw.find('div',class_='discount_original_price').text.strip()

    except:
        orignal_price = final_price
    else:
        orignal_price = data_orignal_prices

    try:
        url = game.get('href')
    except:
        url = ''

    data = {
        'review_summary': review_summary,
        'positives': positives,
        'players': players,
        'platforms': platforms,
        'price': orignal_price,
        'final_price': final_price,
        'discount': discount,
        'url': url
    }

    id = game.get('data-ds-appid')
    data.update(get_hover_data(id))

    write_csv(data)


def main():
    game_list = []
    start = 0

    url = f'https://store.steampowered.com/search/results/?query&start={start}&count=100&tags=9'

    while True:

        games = get_games(get_html(url))

        if games:
            game_list.extend(games)
            start += 100
            url = f'https://store.steampowered.com/search/results/?query&start={start}&count=100&tags=9'
        else:
            break

    for game in game_list:
        scrape_game_data(game)


# if __name__ == '__main__':
#     main()

main()