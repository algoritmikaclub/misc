from telebot import TeleBot

TOKEN = '6275999824:AAHN4qstpUwsOO1Rk2EQ0K3jeyTXqITd18k'
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    answer = f'<b>Привет!</b> <u>{message.from_user.first_name}</u> <u>{message.from_user.last_name}</u>'
    bot.send_message(message.chat.id, text=answer, parse_mode='html')


@bot.message_handler()
def on_message(message):
    bot.send_message(message.chat.id, text=message.text)



if __name__ == '__main__':
    bot.polling(non_stop=True)