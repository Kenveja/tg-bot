from telebot import formatter
import telebot
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot(...)

@bot.message_handler(content_types=['text'])

def get_text_masseges(masseg):
    photo = open('C:\/Users\/User\/Documents\/программы\/TG_BOT\/Погода.jpg', 'rb')
    text_start = 'Приветствуем вас и желаем приятно провести время! \nДля получения команд воспользуйтесь /commandlist'
    user_id = masseg.from_user.id
    if masseg.text == '/mydata':
        bot.send_message(masseg.from_user.id, user_id)
    elif masseg.text == '/commandlist': 
        bot.send_message(masseg.from_user.id, 'Список команд: /mydata, /weather')
    elif masseg.text == '/start':
        bot.send_photo(masseg.chat.id,photo,caption=text_start)
    elif masseg.text == '/weather':
        bot.send_message(masseg.from_user.id,'Введи город в котором хочешь узнать температуру:')
    elif masseg.text:
        rec = requests.get('https://rp5.ru/Погода_в_России')
        soup = BeautifulSoup(rec.text, 'html.parser')
        ol_links = soup.find_all('a',href = True)
        keys = {}
        for i in ol_links:
            if i.get_text() not in ['>>>']:
                keys[i.get_text()] = f'https://rp5.ru{i["href"]}'
        if masseg.text in keys:
            rec = requests.get(keys[masseg.text])
            soup = BeautifulSoup(rec.text, 'html.parser')
            ol_links = soup.find('div', id = 'ArchTemp').find('span', class_ = 't_0').get_text()
            bot.send_message(masseg.from_user.id, ol_links )
        else:
            bot.send_message(masseg.from_user.id,'Такого города в РФ не существует')
    else: 
        bot.send_message(masseg.from_user.id, 'Я не знаю такой команды. Напиши /help')

bot.polling(none_stop = True, interval=0)
