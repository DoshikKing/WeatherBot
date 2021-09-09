# -*- coding: utf-8 -*-
# About:
# WeatherBot v1
# This bot is for searching information
# about weather in your city.

import telebot;
from telebot import types
import random
import pyowm
from pyowm.utils import config as cfg

# токен API Tl
token='your_token'

language = 'ru'

bot = telebot.TeleBot(token);

# обработчики запросов клиента
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	global language
	# call.data это callback_data, которую мы указали при объявлении кнопки
	if call.data == "ru":
		language = "ru"
		bot.send_message(call.message.chat.id, 'Язык сменен на Русский!');
	elif call.data == "eng":
		language = "eng"
		bot.send_message(call.message.chat.id, 'Language changed to English!');

@bot.message_handler(commands=['start'])
def start_command(message):
	global language
	if(language == "eng"):
		bot.send_message(message.chat.id, "WeatherBot v1" + '\n' + "This bot is for searching information" + "\n" + "about weather in your city." + "\n" + "You just need to type your city name." + "\n " + "Write /help to learn more...")
	else:
		bot.send_message(message.chat.id, "WeatherBot v1" + '\n' + "Бот предазначен для поиска информации" + "\n" + "о погоде в вашем горде." + "\n" + "Чтобы узнать погоду напишите город." + "\n" + "Напишите /help чьобы узнать больше...")

@bot.message_handler(commands=['help'])
def help_command(message):
	global language
	if(language == "eng"):
		bot.send_message(message.from_user.id, "To find out the weather, just write the name of your city." + "\n " + "If you want to change the language, then write /settings")
	else:
		bot.send_message(message.from_user.id, "Чтобы узнать погоду достаточно написать название вашего города." + "\n" + "Если вы хотите сменить язык, то напишите /settings")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	global language
	if message.text == "/settings":
		# наша клавиатура
		keyboard = types.InlineKeyboardMarkup();
		key_ru = types.InlineKeyboardButton(text='Русский', callback_data='ru');
		keyboard.add(key_ru);
		key_eng= types.InlineKeyboardButton(text='Английский', callback_data='eng');
		keyboard.add(key_eng);
		question = 'Вы хотите сменить язык?';
		bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
	else:
		config = cfg.get_default_config()
		config['language'] = language

		# токен с https://home.openweathermap.org/api_keys
		owm = pyowm.OWM('your_token', config)

		print(message.text)
		print(language)
		city = message.text

		mgr = owm.weather_manager()

		try:
			observation = mgr.weather_at_place(city)
			weather = observation.weather
			# отвечаем
			if(language == "eng"):
				ans = 'Weather in ' + city.title() + " city" + ':' + "\n" + weather.detailed_status + "\n"
			else:
				ans = 'Погода в городе ' + city.title() + ':' + "\n" + weather.detailed_status + "\n"
			
			temperature = weather.temperature('celsius')['temp']

			# отвечаем
			if(language == "eng"):
				ans = ans + 'Temperature: ' + str(temperature) + ' °C' + "\n"
			else:
				ans = ans + 'Температура: ' + str(temperature) + ' °C' + "\n"
			
			pressure = weather.pressure
			humidity = weather.humidity

			# отвечаем
			if(language == "eng"):
				ans = ans + 'Pressure: ' + str(pressure['press']) + '; Humidity: ' + str(humidity) + ' %' + "\n"
			else:
				ans = ans + 'Давление: ' + str(pressure['press']) + '; Влажность: ' + str(humidity) + ' %' + "\n"
			wind = weather.wind()

			# отвечаем
			if(language == "eng"):
				ans = ans + 'Wind: ' + str(wind['deg']) + ' °;' + ' Speed: ' + str(wind['speed']) + ' м/s' + "\n"
			else:
				ans = ans + 'Ветер: ' + str(wind['deg']) + ' °;' + ' Скорость: ' + str(wind['speed']) + ' м/c' + "\n"
			bot.send_message(message.from_user.id, ans)
		except:
			if(language == "eng"):
				bot.send_message(message.from_user.id, "Mistake! There is no city with this name!")
			else:
				bot.send_message(message.from_user.id, "Ошибка! Города с таким именем не существует!")

bot.polling(none_stop=True, interval=0)
