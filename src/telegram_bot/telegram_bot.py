from os import stat
import telebot

bot = telebot.TeleBot('5437081176:AAH2QeGKLbiYgn2i8S1LtM0Zs8x5EOBb6Q4')

main_chapters = ['Окружение', 'Основы Python', 'Алгоритмы и структуры данных', 'БД', 'HTTP протокол', 'полезные ссылки']
subchapters = ['числа', 'знаки', 'питон']
thirdLevelChapters = ['базовые числа']
state1 = True

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я на связи \n Правила пользования ботом: \n Бот воспринимает только письменные запросы. Поиск информации происходит по разделам. Чтобы выбрать раздел, отправьте боту его название')
    bot.send_message(m.chat.id, 'Доступные разделы:')
    state1 = True
    for mchapter in main_chapters:
        bot.send_message(m.chat.id, mchapter)
    

@bot.message_handler(content_types=["text"])
def handle_text(message):
    global state1
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

@bot.message_handler(content_types=["text"])
def subchapters_handler(mes):
    if mes.text in subchapters:
        bot.send_message(mes.chat.id, '2В подразделе ' + mes.text + ' доступны следующие темы:')
        for theme in thirdLevelChapters:
            bot.send_message(mes.chat.id, theme)
    else:
        bot.send_message(mes.chat.id, '2Извините, раздел ' + mes.text + ' не найден')

bot.polling(none_stop=True, interval=0)