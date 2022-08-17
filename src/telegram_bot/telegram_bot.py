import telebot

bot = telebot.TeleBot('5437081176:AAH2QeGKLbiYgn2i8S1LtM0Zs8x5EOBb6Q4')

main_chapters = ['Окружение', 'Основы Python', 'Алгоритмы и структуры данных', 'БД', 'HTTP протокол', 'полезные ссылки']
subchapters = []
thirdLevelChapters = []

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я на связи')
    bot.send_message(m.chat.id, 'Правила пользования ботом:')
    bot.send_message(m.chat.id, 'Бот воспринимает только письменные запросы. Поиск информации происходит по разделам. Чтобы выбрать раздел, отправьте боту его название')
    bot.send_message(m.chat.id, 'Доступные разделы:')
    for mchapter in main_chapters:
        bot.send_message(m.chat.id, mchapter)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    
    bot.send_message(message.chat.id, 'Вы написали: ' + message.text)

bot.polling(none_stop=True, interval=0)