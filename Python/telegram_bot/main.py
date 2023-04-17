from telebot import TeleBot
from credentials import TOKEN
from apis import get_random_duck, ask_chat_gpt

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    answer = f'<b>Привет!</b> <u>{message.from_user.first_name}</u> <u>{message.from_user.last_name}</u>'
    bot.send_message(message.chat.id, text=answer, parse_mode='html')


@bot.message_handler(commands=['duck'])
def duck(message):
    url = get_random_duck()
    bot.send_message(message.chat.id, text=url)


@bot.message_handler(commands=['GPT'])
def duck(message):
    bot.send_message(message.chat.id, text='Подождите, генерирую ответ...')
    answer = ask_chat_gpt(message.text[4:])
    bot.send_message(message.chat.id, text=answer)


@bot.message_handler()
def on_message(message):
    bot.send_message(message.chat.id, text=message.text)


if __name__ == '__main__':
    bot.polling(non_stop=True)
