import json
import threading
import time
import requests
import bs4
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '1232811909:AAHPQH7f-_A2dLxLVH0-UKe8XML2OgSWfLc'
bot = telebot.TeleBot(API_TOKEN)

# data = {
#     "last_cars_id": "",
#     "path": "",
#     "id": ""
# }

with open('data/data.bruh', 'r', encoding='UTF-8') as file:
    data = json.load(file)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    with open('data/data.bruh', 'w', encoding='UTF-8') as f:
        data["id"] = message.chat.id
        json.dump(data, f)
    bot.reply_to(message, 'Добрый денб, посетитель этого никому не нужного бота!\n'
                          'Здесь ты будешь получать уведомления о новых объявлениях на сайте Avito.ru, а позже, '
                          'возможно, и с других сайтов.\n\n'
                          'У тебя есть возможность узнать или изменить текущий путь поиска по CUMандам /path и '
                          '/new_path соответственно')


@bot.message_handler(commands=['path'])
def get_path(message):
    bot.reply_to(message, "Текущий путь: " + data["path"])


@bot.message_handler(commands=['new_path'])
def set_path(message):
    if len(message.text) > 10:
        with open('data/data.bruh', 'w', encoding='UTF-8') as f:
            data["path"] = message.text[10:]
            json.dump(data, f)
            bot.reply_to(message, 'Сменил пути на ' + data["path"])
    else:
        bot.reply_to(message, 'Ты бы путь написал...')


def searcher():
    global data
    last_time = 0

    while True:
        if time.time() - last_time > 30:
            last_time = time.time()

            headers = {
                'User-Agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)''' 
                '''Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.275 '''
            }

            tmp_data = data
            check = False
            while not check:
                print('try')
                try:
                    html = requests.get(url=data['path'], headers=headers)
                    items = bs4.BeautifulSoup(html.text, "html.parser").find_all("div", {"data-marker": "item"})
                    for item in items:
                        try:
                            image_link = str(item.find("img", {"itemprop": "image"})['srcset']).split(',')[-1][:-5]
                            car_info = str(item.find("img", {"itemprop": "image"})['alt'])
                            car_link = 'https://www.avito.ru' + str(item.find("a", {"itemprop": "url"})['href'])
                            if car_link.split('_')[-1] not in data['last_cars_id']:
                                data['last_cars_id'].append(car_link.split('_')[-1])
                                markup = InlineKeyboardMarkup()
                                markup.row_width = 1
                                markup.add(InlineKeyboardButton("Открыть на авито", url=car_link))
                                bot.send_photo(data['id'], image_link, caption=car_info, reply_markup=markup)
                                with open('data/data.bruh', 'w', encoding='UTF-8') as f:
                                    json.dump(data, f)
                                    print('save')
                        except:
                            pass
                    check = True
                    print('success')
                except:
                    print('error')
                    data = tmp_data
                    with open('data/data.bruh', 'w', encoding='UTF-8') as f:
                        json.dump(data, f)
                        print('save')


if __name__ == '__main__':
    searcher_thread = threading.Thread(target=searcher, args=())
    searcher_thread.start()
    bot.polling()
