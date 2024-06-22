import telebot
from telebot import types
from find_words import find_words

with open(r'D:\py_projects\bot_tokens.txt', 'r', encoding='utf-8') as file:
    token = file.readline()

bot = telebot.TeleBot(token)


session_started = False
word = ""
letters = dict()


@bot.message_handler(commands=['start'])
def start(message):
    global session_started
    session_started = True
    bot.send_message(message.chat.id, "Добро пожаловать! Напишите слово из 5 букв.")


@bot.message_handler(func=lambda message: session_started)
def handle_word(message):
    global word
    if len(message.text) == 5 and message.text.isalpha():
        word = message.text.upper()
        show_inline_keyboard(message.chat.id)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, введите слово из 5 букв.")


def show_inline_keyboard(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    symbols = {"=": "🟨", "+": "⬜", "-": "⬛"}
    for key, val in symbols.items():
        i = 0
        temp_array = list()
        for letter in word:
            temp_array.append(types.InlineKeyboardButton(val, callback_data=str(i)+key+letter))
            i += 1
        keyboard.row(*temp_array)

    keyboard.row(
        types.InlineKeyboardButton('Подтвердить', callback_data='confirm'),
        types.InlineKeyboardButton('Отмена', callback_data='cancel')
    )
    bot.send_message(chat_id, f"Выберите состояние букв слова {word}:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_inline_callback(call):

    global letters

    if (call.data[2] in word) and (call.data[0].isdigit()) and (call.data[1] in '=+-'):
        letter = call.data[1:]
        index = int(call.data[0])
        letters[index] = letter

    if call.data == 'confirm':
        if len(letters) == 5:
            find_words(word)
        else:
            five_numbers = set(range(5))
            five_numbers.difference_update(set(letters.keys()))
            difference_letters = ',  '.join([f"{word[i]}({i+1})" for i in list(five_numbers)])
            bot.send_message(call.message.chat.id, f"Вы не назначили состояние буквам: {difference_letters}")

    if call.data == 'cancel':
        bot.send_message(call.message.chat.id, "Слово отменено и удалено.")


bot.polling()
