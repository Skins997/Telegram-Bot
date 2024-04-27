import requests
import random
import telebot
from bs4 import BeautifulSoup as b


URL = 'https://www.anekdot.ru/release/anekdot/year/2023/8' # ссылка на парсинг  
BOT =   '#токен бот'           # вставьте ваш токен
def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    anekdots = soup.find_all('div', class_='text')
    return [c.text for c in anekdots]

list_of_jokes = parser(URL)
random.shuffle(list_of_jokes)

bot = telebot.TeleBot(BOT)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, Я создан для того, чтобы придумывать для вас анекдоты. Для начала введите любую цифру!".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', )





@bot.message_handler(content_types=['text'])
def jokes(message):
    if message.text.lower() in '123456789':
        bot.send_message(message.chat.id, list_of_jokes[0])
        del list_of_jokes[0]
    else:
        bot.send_message(message.chat.id, 'Введите любую цифру:')



bot.polling()