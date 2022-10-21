import telebot
import os
import parser
import connection_db
import pretty_errors
from dotenv import load_dotenv
from telebot import types


def main():
    load_dotenv('keys.env')
    bot = telebot.TeleBot(os.getenv('TOKEN_TELEGRAM_BOT'))

    @bot.message_handler(commands=["start"])
    def start(m, res=False):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Меню")
        markup.add(item1)

        bot.send_message(m.chat.id,
                         "Приветствую тебя сыщик. Что-бы начать поиск легких или не очень денег введи запрос",
                         reply_markup=markup)
        bot.register_next_step_handler(m, find_job)

    @bot.message_handler(commands=["Настройки"])
    def settings(message, res=False):
        bot.send_message(message.chat.id, 'Какой размер выборки?')
        bot.register_next_step_handler(message, set_search_size)

    @bot.message_handler(commands=["Поиск"])
    def find(message, res=False):
        bot.send_message(message.chat.id, 'Введите запрос')
        bot.register_next_step_handler(message, find_job)

    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        if message.text == 'Меню':
            menu(message)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_worker(call):

        if call.data == 'search':
            find(call.message)
        elif call.data == 'settings':
            settings(call.message)

    def menu(message):
        # вызов меню
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Поиск", callback_data="search")
        item2 = types.InlineKeyboardButton(text="Настройки", callback_data="settings")
        markup.add(item1, item2)

        bot.send_message(message.chat.id,
                         "Выберите опцию",
                         reply_markup=markup)

    def find_job(message):

        if message.text == 'Меню':
            return menu(message)

        freelanceru = parser.FreelanceRu(message.text)
        print(message.text)

        tasks = freelanceru.run()
        if tasks:
            search_size = len(tasks)
            if connection_db.check_user(message.chat.id):
                search_size = connection_db.get_info_search_size(message.chat.id)

            for i in range(search_size):
                bot.send_message(message.chat.id, '\n'.join(tasks[i]))
        else:
            bot.send_message(message.chat.id, 'По данному запросу, работы не найдено')
        menu(message)

    def set_search_size(message):
        # connection_db.add_info_search_size_test(message.chat.id, int(message.text))
        if connection_db.check_user(message.chat.id):
            connection_db.update_search_size(message.chat.id, int(message.text))
        else:
            connection_db.add_search_size(message.chat.id, int(message.text))

    print('Bot enabled')
    bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    main()
