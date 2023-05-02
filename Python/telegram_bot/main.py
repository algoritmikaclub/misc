from telebot import TeleBot, types
from credentials import TOKEN
from apis import get_random_duck, ask_chat_gpt
from hangman import HangmanGame
from wiki import search_wiki, wiki_page
from text_to_speech import text_to_speech, speech_to_text

bot = TeleBot(TOKEN)
hg = HangmanGame()


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


@bot.callback_query_handler(func=lambda call: call.data)
def answer(call):
    title, summery, url = wiki_page(call.data)
    bot.send_message(call.message.chat.id, text=title)
    bot.send_message(call.message.chat.id, text=summery)
    bot.send_message(call.message.chat.id, text=url)


@bot.message_handler(commands=['wiki'])
def duck(message):
    text = ' '.join(message.text.split(' ')[1:])
    results = search_wiki(text)
    markup = types.InlineKeyboardMarkup()
    for res in results:
        markup.add(types.InlineKeyboardButton(res, callback_data=res))
    bot.send_message(
        message.chat.id, text='Смотри что я нашел!', reply_markup=markup)


@bot.message_handler(commands=['speech'])
def duck(message):
    text = ' '.join(message.text.split(' ')[1:])
    text_to_speech(text)
    with open('text_to_speech.mp3', 'rb') as f:
        bot.send_audio(message.chat.id, f)


@bot.message_handler(content_types=['voice'])
def duck(message):
    file = bot.get_file(message.voice.file_id)
    bytes = bot.download_file(file.file_path)
    with open('voice.ogg', 'wb') as f:
        f.write(bytes)
    text = speech_to_text()
    bot.send_message(message.chat.id, text=text)


@bot.message_handler()
def on_message(message):
    if hg.game_on:
        if len(message.text) > 1:
            bot.send_message(
                message.chat.id, text='Вводить можно только буквы!')
            return
        msg = hg.game_step(message.text)
        bot.send_message(message.chat.id, text=msg)
        return
    if message.text == 'виселица':
        hg.start()
        text = f'Добро пожаловать в игру. Попробуй отгадать слово \n {hg.info()}'
        bot.send_message(message.chat.id, text=text)


if __name__ == '__main__':
    bot.polling(non_stop=True)
