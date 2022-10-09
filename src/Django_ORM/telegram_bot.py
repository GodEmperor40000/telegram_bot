from email import message
from os import stat
import telebot
import os,django
from telebot import types

os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "Django_ORM.settings") 
django.setup()

from information.views import *

api_key = open('API_key.txt', 'r')
bot = telebot.TeleBot(api_key.read())
#information = get_information(1,2,3)
all_chapters = get_chapters()
main_chapters = ['Окружение', 'Основы Python', 'Алгоритмы и структуры данных', 'БД', 'HTTP протокол', 'полезные ссылки']
subchapters = ['числа', 'знаки', 'питон']
thirdLevelChapters = ['базовые числа']

#states = {state1: True, stateSearch: False, stateCreate: False, stateSubCreate: False, stateDelete: False}
state1, stateSearch, stateCreate, stateSubCreate, stateDelete, stateTLCreate, stateCreateInfo = True, False, False, False, False, False, False
states = {'state1': True, 'stateSearch': False, 'stateCreate': False, 'stateSubCreate': False, 'stateDelete': False, 'stateTLCreate': False, 'stateCreateInfo': False }
all_chapters = get_chapters()
def state_falser():
    global states
    for state in states:
        
        if state != 'state1':
            states[state] = False
    return states

#================================================================================================================


@bot.message_handler(commands=["start"])
def start(m, res=False):
    all_chapters = get_chapters()
    #for chapter in all_chapters:
    bot.send_message(m.chat.id, f'{all_chapters}')
    bot.send_message(m.chat.id, 'Я на связи \n Правила пользования ботом: \n Бот воспринимает только письменные запросы. Поиск информации происходит по разделам. Чтобы выбрать раздел, отправьте боту его название')
    bot.send_message(m.chat.id, 'Доступные разделы:')
    global states
    state_falser()
    states['stateSearch'] = True
    for mchapter in main_chapters:
        bot.send_message(m.chat.id, mchapter)
    

@bot.message_handler(commands = ["create"])
def create(message):
    bot.send_message(message.chat.id,'Чтобы создать новый раздел, выберете из следующих команд нужное:')
    bot.send_message(message.chat.id,'/create_Chapter - создать новую главу' )
    bot.send_message(message.chat.id,'/create_Subchapter - создать новую подглаву' )
    bot.send_message(message.chat.id,'/create_TLchapter - создать новую главу третьего уровня *пока не работает' )
    bot.send_message(message.chat.id,'/create_Info - добавить новую информацию в выбранный раздел *пока не работает')

@bot.message_handler(commands = ["create_Subchapter"])
def createNewSubchapter(message):
    bot.send_message(message.chat.id, 'Напишите название подглавы, которую вы хотите добавить и главы, в которую вы хотите добавить подглаву в формате: Глава Подглава')
    global states
    state_falser()
    states['stateSubCreate'] = True

@bot.message_handler(commands = ["create_Chapter"])
def createNewChapter(message):
    bot.send_message(message.chat.id,'Напишите название новой главы')
    global states
    state_falser()
    states['stateCreate'] = True

@bot.message_handler(commands = ["create_TLchapter"])
def createNewTLChapter(message):
    bot.send_message(message.chat.id, "Напишите название главы третьего уровня, которую вы хотите добавить, название главы и подглавы, в которые вы хотите добавить новую главу в формате: Глава, Подглава, Глава третьего уровня  ")
    global states
    state_falser()
    states['stateTLCreate'] = True

@bot.message_handler(commands = ["create_Info"])
def createNewInfo(message):
    bot.send_message(message.chat.id, 'Напишите информацию, которую вы хотите добавить в раздел в формате: Глава, Подглава, Глава третьего уровня, Информация. Всё, что будет написано после главы третьего уровня, будет добавлено в качестве информации')
    global states
    state_falser()
    states['stateCreateInfo'] = True


@bot.message_handler(commands= ["delete"])
def deletingMChapter(message):
    bot.send_message(message.chat.id,'Напишите название главы, которую вы хотите удалить')
    global states
    state_falser()
    states['stateDelete'] = True




#============================================================================================================


@bot.message_handler(content_types=["text"])
def handle_text(message):
    global states
    bot.send_message(message.chat.id, f"stateSearch: {states['stateSearch']}")
    #bot.send_message(message.chat.id, f'state1: {states[state1]}')
    if states['stateSearch'] == True:
        bot.send_message(message.chat.id, 'Вы ищите:')
        if states['state1'] == True:
            if message.text in main_chapters:
                bot.send_message(message.chat.id, '1В разделе ' + message.text + ' доступны следующие подразделы: ')
                for subchapter in subchapters:
                    bot.send_message(message.chat.id, subchapter)
                states['state1'] = False 
            else:
                bot.send_message(message.chat.id, '1Извините, раздел ' + message.text + ' не найден')
        
        else:
            if message.text in subchapters:
                bot.send_message(message.chat.id, '2В подразделе ' + message.text + ' доступны следующие темы:')
                for theme in thirdLevelChapters:
                    bot.send_message(message.chat.id, theme)
            else:
                bot.send_message(message.chat.id, '2Извините, раздел ' + message.text + ' не найден')
        
    elif states['stateCreate']:
        
        add_MainChapter(message.text)
        bot.send_message(message.chat.id, f'Вы добавили главу: {message.text}')

    elif states['stateSubCreate']:
        messageText = message.text.split(' ')
        subChapter = messageText[1]
        chapter = messageText[0]
        bot.send_message(message.chat.id, f"Вы хотите создать подглавуглаву: {subChapter} в главе: {chapter}")
        add_SubChapter(subChapter, chapter)
        bot.send_message(message.chat.id, 'Подглава добавлена')

    elif states['stateDelete']:
        all_chapters = get_chapters()
        if message.text in all_chapters:
            name = message.text
            bot.send_message(message.chat.id, f'Глава {name} удаляется...')
            a = deleteMChapter(message.text)
            bot.send_message(message.chat.id, f'{a}')
            bot.send_message(message.chat.id, f'Глава удалена')
        else:
            bot.send_message(message.chat.id, 'Данной главы не существует')

    elif states['stateTLCreate']:
        all_chapters = get_chapters()
        messageText = message.text.split(', ')
        chapter = messageText[0]
        subChapter = messageText[1]
        tlChapter = messageText[2]
        bot.send_message(message.chat.id, f'Вы хотите добавить главу: {tlChapter} в подглаву: {subChapter} в главе: {chapter}')
        if chapter in all_chapters and subChapter in all_chapters[chapter]:
            bot.send_message(message.chat.id, 'Глава и подглава найдены')
            add_thirdLevelChapter(chapter, subChapter, tlChapter)
            bot.send_message(message.chat.id, 'Глава третьего уровня добавлена!')
        elif chapter in all_chapters and subChapter not in all_chapters[chapter]:
            bot.send_message(message.chat.id, 'В данной главе нет такой подглавы')
        elif chapter not in all_chapters:
            bot.send_message(message.chat.id, 'Нет такой главы')

    elif states['stateCreateInfo']:
        all_chapters = get_chapters()
        messageText = message.text.split(', ')
        chapter = messageText[0]
        subChapter = messageText[1]
        tlChapter = messageText[2]
        inform = messageText[3]
        bot.send_message(message.chat.id, f'Вы хотите добавить следующую информацию: "{inform}" в главу третьего уровня: {tlChapter} в подглаву: {subChapter} в главе: {chapter}')
        if chapter in all_chapters and subChapter in all_chapters[chapter]:
            bot.send_message(message.chat.id, 'Глава и подглава найдены')
        elif chapter in all_chapters and subChapter not in all_chapters[chapter]:
            bot.send_message(message.chat.id, 'В данной главе нет такой подглавы')
        elif chapter not in all_chapters:
            bot.send_message(message.chat.id, 'Нет такой главы')
        #bot.send_message(message.chat.id, f'тут пока ничего не работает')

        
        

bot.polling(none_stop=True, interval=0)


#Добавить добавление глав второго уровня