import json
import telebot


API_TOKEN = '1232811909:AAHPQH7f-_A2dLxLVH0-UKe8XML2OgSWfLc'
bot = telebot.TeleBot(API_TOKEN)


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


if __name__ == '__main__':
    bot.polling()
