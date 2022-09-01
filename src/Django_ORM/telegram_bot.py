from email import message
from os import stat
import telebot
import os,django
from telebot import types

os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "Django_ORM.settings") 
django.setup()

from information.views import get_information, get_chapters, add_MainChapter

api_key = open('API_key.txt', 'r')
bot = telebot.TeleBot(api_key.read())
#information = get_information(1,2,3)
all_chapters = get_chapters()
main_chapters = ['Окружение', 'Основы Python', 'Алгоритмы и структуры данных', 'БД', 'HTTP протокол', 'полезные ссылки']
subchapters = ['числа', 'знаки', 'питон']
thirdLevelChapters = ['базовые числа']
state1, stateSearch, stateCreate, stateDelete = True, False, False, False


@bot.message_handler(commands=["start"])
def start(m, res=False):
    all_chapters = get_chapters()
    for chapter in all_chapters:
        bot.send_message(m.chat.id, chapter)
    bot.send_message(m.chat.id, 'Я на связи \n Правила пользования ботом: \n Бот воспринимает только письменные запросы. Поиск информации происходит по разделам. Чтобы выбрать раздел, отправьте боту его название')
    bot.send_message(m.chat.id, 'Доступные разделы:')
    global stateSearch, stateCreate
    stateSearch, stateCreate = True, False
    for mchapter in main_chapters:
        bot.send_message(m.chat.id, mchapter)
    

@bot.message_handler(commands = ["create"])
def createNewChapter(message):
    bot.send_message(message.chat.id,'Напишите название новой главы')
    global stateCreate, stateSearch
    stateCreate, stateSearch = True, False

@bot.message_handler(commands= ["delete"])
def deleteMChapter(message):
    bot.send_message(message.chat.id,'Напишите название главы, которую вы хотите удалить')
    global stateCreate, stateSearch, stateDelete
    stateCreate, stateSearch = False, False, True

@bot.message_handler(content_types=["text"])
def handle_text(message):
    global state1, stateSearch, stateCreate, stateDelete
    bot.send_message(message.chat.id, f'stateSearch: {stateSearch, stateCreate}')
    if stateSearch:
        bot.send_message(message.chat.id, 'Вы ищите:')
        if state1 == True:
            if message.text in main_chapters:
                bot.send_message(message.chat.id, '1В разделе ' + message.text + ' доступны следующие подразделы: ')
                for subchapter in subchapters:
                    bot.send_message(message.chat.id, subchapter)
                state1 = False 
            else:
                bot.send_message(message.chat.id, '1Извините, раздел ' + message.text + ' не найден')
        
        else:
            if message.text in subchapters:
                bot.send_message(message.chat.id, '2В подразделе ' + message.text + ' доступны следующие темы:')
                for theme in thirdLevelChapters:
                    bot.send_message(message.chat.id, theme)
            else:
                bot.send_message(message.chat.id, '2Извините, раздел ' + message.text + ' не найден')
        
    elif stateCreate:
        bot.send_message(message.chat.id, f'Вы добавили главу: {message.text}')
        add_MainChapter(message.text)
        bot.send_message(message.chat.id, f'Вы добавили главу: {message.text}')

    elif stateDelete:
        bot.send_message(message.chat.id, f'Глава {message.text} удалена')

bot.polling(none_stop=True, interval=0)