
from os import stat
import telebot
import os,django
from telebot import types

os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "Django_ORM.settings") 
django.setup()

from information.views import *

api_key = open('API_key.txt', 'r')
bot = telebot.TeleBot(api_key.read())
devState = False #When True some inner program states will be shown

all_chapters = get_chapters()

states = {'state1': True, 'state2': True, 'stateSearch': False, 'stateCreate': False, 'stateSubCreate': False, 'stateTLCreate': False, 'stateCreateInfo': False, 'stateMChDelete': False, 'stateSChDelete': False, 'stateTLChDelete': False }
chosenMainChapter = 1
chosenSubChapter = 1
all_chapters = get_chapters()

def state_falser():
    global states
    for state in states:
        
        if state != 'state1' and state != 'state2':
            states[state] = False
    return states

#================================================================================================================


@bot.message_handler(commands=["start"])
def start(m, res=False):
    global devState, states
    all_chapters = get_chapters()
    if devState:
        bot.send_message(m.chat.id, f'{all_chapters}')

    bot.send_message(m.chat.id, 'Доступные команды: /start /create /delete')
    bot.send_message(m.chat.id, 'Я на связи \n Правила пользования ботом: \n Бот воспринимает только письменные запросы. Поиск информации происходит по разделам. Чтобы выбрать раздел, отправьте боту его название')
    bot.send_message(m.chat.id, 'Доступные разделы:')
    state_falser()
    states['stateSearch'] = True
    states['state1'] = True
    states['state2'] = True
    for key in all_chapters.keys():
        bot.send_message(m.chat.id, key)


#=========================================================================================CREATING==========================================================================


@bot.message_handler(commands = ["create"])
def create(message):
    bot.send_message(message.chat.id,'Чтобы создать новый раздел, выберете из следующих команд нужное:')
    bot.send_message(message.chat.id,'/create_Chapter - создать новую главу' )
    bot.send_message(message.chat.id,'/create_Subchapter - создать новую подглаву' )
    bot.send_message(message.chat.id,'/create_TLchapter - создать новую главу третьего уровня' )
    bot.send_message(message.chat.id,'/create_Info - добавить новую информацию в выбранный раздел')

@bot.message_handler(commands = ["create_Subchapter"])
def createNewSubchapter(message):
    bot.send_message(message.chat.id, 'Напишите название подглавы, которую вы хотите добавить и главы, в которую вы хотите добавить подглаву в формате: Глава, Подглава')
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


#=========================================================================================DELETE==========================================================================


@bot.message_handler(commands=["delete"])
def deleting(message):
    bot.send_message(message.chat.id,'Чтобы удалить один из разделов, выберете нужную команду:')
    bot.send_message(message.chat.id,'/delete_MChapter - Удаление глав')
    bot.send_message(message.chat.id,'/stateSChDelete - Удаление подглав')
    bot.send_message(message.chat.id,'/stateTLChDelete - Удаление глав третьего уровня')

@bot.message_handler(commands= ["delete_MChapter"])
def deletingMChapter(message):
    bot.send_message(message.chat.id,'Напишите название главы, которую вы хотите удалить')
    global states
    state_falser()
    states['stateMChDelete'] = True

@bot.message_handler(commands= ["stateSChDelete"])
def deletingSChapter(message):
    bot.send_message(message.chat.id,'Напишите название главы, в которой лежит подглава, которую вы хотите удалить в формате: Глава; Подглава')
    global states
    state_falser()
    states['stateSChDelete'] = True

@bot.message_handler(commands= ["stateTLChDelete"])
def deletingTLChapter(message):
    bot.send_message(message.chat.id,'Напишите название главы, подглавы и третьего уровня, которую вы хотите удалить в формате: Глава; Подглава; Глава третьего уровня')
    global states
    state_falser()
    states['stateTLChDelete'] = True




#=========================================================================================MESSAGE HANDLERS==========================================================================


@bot.message_handler(content_types=["text"])
def handle_text(message):
    global states, devState
    if devState:
        bot.send_message(message.chat.id, f"stateSearch: {states['stateSearch']}")
    #bot.send_message(message.chat.id, f'state1: {states[state1]}')
    if states['stateSearch'] == True:
        
        all_chapters = get_chapters()
        #bot.send_message(message.chat.id, 'Вы ищите:')
        if states['state1'] == True:
            if message.text in all_chapters.keys():
                bot.send_message(message.chat.id, 'В главе ' + message.text + ' доступны следующие подглавы: ')
                global chosenMainChapter 
                chosenMainChapter = message.text
                for subchapter in all_chapters[message.text]:
                    bot.send_message(message.chat.id, subchapter)
                states['state1'] = False 
            else:
                bot.send_message(message.chat.id, 'Извините, раздел ' + message.text + ' не найден')
        
        elif states['state2']:
            
            if message.text in all_chapters[chosenMainChapter]:
                bot.send_message(message.chat.id, 'В подразделе ' + message.text + ' доступны следующие темы:')
                global chosenSubChapter
                chosenSubChapter = message.text
                for theme in all_chapters[chosenMainChapter][message.text]:
                    bot.send_message(message.chat.id, theme)
                states['state2'] = False
            else:
                bot.send_message(message.chat.id, 'Извините, подраздел ' + message.text + ' не найден')
        
        else:
            if message.text in all_chapters[chosenMainChapter][chosenSubChapter]:
                bot.send_message(message.chat.id, 'В главе третьего уровня ' + message.text + ' найдена следующая информация:')
                bot.send_message(message.chat.id, get_information(chosenMainChapter, chosenSubChapter, message.text))
                #get_information(chosenMainChapter, chosenSubChapter, message.text)
            else:
                bot.send_message(message.chat.id, 'Извините, глава третьего уровня ' + message.text + ' не найдена')

    elif states['stateCreate']:
        
        add_MainChapter(message.text)
        bot.send_message(message.chat.id, f'Вы добавили главу: {message.text}')

    elif states['stateSubCreate']:
        messageText = message.text.split(', ')
        subChapter = messageText[1]
        chapter = messageText[0]
        bot.send_message(message.chat.id, f"Вы хотите создать подглавуглаву: {subChapter} в главе: {chapter}")
        add_SubChapter(subChapter, chapter)
        bot.send_message(message.chat.id, 'Подглава добавлена')

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
        if chapter in all_chapters:
            if subChapter in all_chapters[chapter]: 
                if tlChapter in all_chapters[chapter][subChapter]:
                    bot.send_message(message.chat.id, f'Вы хотите добавить следующую информацию: "{inform}" в главу третьего уровня: {tlChapter} в подглаву: {subChapter} в главе: {chapter}')
                    insert_information(inform, chapter, subChapter, tlChapter)
                    bot.send_message(message.chat.id, 'Информация добавлена!')
                else:
                    bot.send_message(message.chat.id, 'Такая глава третьего уровня не найдена')
            else:
                bot.send_message(message.chat.id, 'Такая подглава не найдена')
        else:
            bot.send_message(message.chat.id, 'Такая глава не найдена')

    elif states['stateMChDelete']:
        all_chapters = get_chapters()
        if message.text in all_chapters:
            name = message.text
            bot.send_message(message.chat.id, f'Глава {name} удаляется...')
            a = deleteMChapter(message.text)
            bot.send_message(message.chat.id, f'{a}')
            bot.send_message(message.chat.id, f'Глава удалена')
        else:
            bot.send_message(message.chat.id, 'Данной главы не существует')

    elif states['stateSChDelete']:
        all_chapters = get_chapters()
        messageText = message.text.split('; ')
        chapter = messageText[0]
        subChapter = messageText[1]
        
        if chapter in all_chapters:
            if subChapter in all_chapters[chapter]:
                a = deleteSChapter(chapter, subChapter)
                bot.send_message(message.chat.id, f'{a}')
            else:
                bot.send_message(message.chat.id, 'Данной подглавы не существует')
        else:
            bot.send_message(message.chat.id, 'Данной главы не существует')    

    elif states['stateTLChDelete']:
        all_chapters = get_chapters()
        messageText = message.text.split('; ')
        chapter = messageText[0]
        subChapter = messageText[1]
        tlChapter = messageText[2]
        
        if chapter in all_chapters:
            if subChapter in all_chapters[chapter]:
                if tlChapter in all_chapters[chapter][subChapter]:
                    a = deleteTLChapter(chapter, subChapter, tlChapter)
                    bot.send_message(message.chat.id, f'{a}')
                else:
                   bot.send_message(message.chat.id, 'Данной главы третьего уровня не существует') 
            else:
                bot.send_message(message.chat.id, 'Данной подглавы не существует')
        else:
            bot.send_message(message.chat.id, 'Данной главы не существует') 

bot.polling(none_stop=True, interval=0)


#Добавить добавление глав второго уровня