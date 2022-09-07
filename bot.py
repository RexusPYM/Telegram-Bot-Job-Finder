import telebot
import os
import parser
from dotenv import load_dotenv


def main():
    load_dotenv('keys.env')
    bot = telebot.TeleBot(os.getenv('TOKEN_TELEGRAM_BOT'))

    @bot.message_handler(commands=["start"])
    def start(m, res=False):
        bot.send_message(m.chat.id,
                         "Приветствую тебя сыщик. Что-бы начать поиск легких или не очень денег введи запрос")

    @bot.message_handler(content_types=['text'])
    def handle_text(message):

        freelanceru = parser.FreelanceRu(message.text)
        print(message.text)

        tasks = freelanceru.run()
        if tasks:
            for task in tasks:
                bot.send_message(message.chat.id, '\n'.join(task))
        else:
            bot.send_message(message.chat.id, 'По данному запросу, работы не найдено')

    print('Bot enabled')
    bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    main()
