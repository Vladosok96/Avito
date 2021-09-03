import json
import requests
import bs4
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


if __name__ == '__main__':
    API_TOKEN = '1232811909:AAHPQH7f-_A2dLxLVH0-UKe8XML2OgSWfLc'
    bot = telebot.TeleBot(API_TOKEN)

    with open('data/data.bruh', 'r', encoding='UTF-8') as file:
        data = json.load(file)

    headers = {
        'User-Agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'''
                      '''Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.275 '''
    }

    items = 0
    check = False
    while not check:
        try:
            print('try')
            html = requests.get(url=data['path'], headers=headers)
            items = bs4.BeautifulSoup(html.text, "html.parser").find_all("div", {"data-marker": "item"})
            check = True
        except:
            pass
    for item in items:
        tmp_data = data
        try:
            image_link = str(item.find("img", {"itemprop": "image"})['srcset']).split(',')[-1][:-5]
            car_info = str(item.find("img", {"itemprop": "image"})['alt']) + "\n" + str(
                item.find("div", {"data-marker": "item-specific-params"}).text)
            car_link = 'https://www.avito.ru' + str(item.find("a", {"itemprop": "url"})['href'])
            print(car_info)
            if car_link.split('_')[-1] not in data['last_cars_id']:
                try:
                    data['last_cars_id'].append(car_link.split('_')[-1])
                    markup = InlineKeyboardMarkup()
                    markup.row_width = 1
                    markup.add(InlineKeyboardButton("Открыть на авито", url=car_link))
                    bot.send_photo(data['id'], image_link, caption=car_info, reply_markup=markup)
                    print(car_link)
                    with open('data/data.bruh', 'w', encoding='UTF-8') as f:
                        json.dump(data, f)
                        print('save')
                except:
                    print('error')
                    data = tmp_data
                    with open('data/data.bruh', 'w', encoding='UTF-8') as f:
                        json.dump(data, f)
                        print('save')
        except:
            pass
    print('success')