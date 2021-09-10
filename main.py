import telebot
import requests
import json


Token = open("token.txt", "r").read()
Api_key = open("apikey.txt", "r").read()

bot = telebot.TeleBot(Token)


def weather(text):
    resp = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?q='+text+'&lang=ru&appid='+Api_key)
    if resp.status_code == 200:
        data = json.loads(resp.content.decode('UTF-8'))
        name = 'Погода в городе '+data['name']+'\n\n'
        temp = 'Температура: '+str(int(round(data['main']['temp']-273)))+'°C\n'
        state = 'Состояние: '+data['weather'][0]['description']+'\n'
        wind = 'Ветер: '+str(data['wind']['speed'])+' м/с\n'
        return name+temp+state+wind
    else:
        return 'Не могу найти город '+text


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, напиши мне название города на английском и я найду прогноз погоды.')


@bot.message_handler(func=lambda n: True)
def fun(message):
    bot.send_message(message.chat.id, weather(message.text))

try:
    bot.polling(none_stop=True, timeout=50)
except:
    pass
