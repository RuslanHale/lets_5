import telebot
from telebot import types
from search_words import find_words
import words_file
with open(r'D:\py_projects\bot_tokens.txt', 'r', encoding='utf-8') as file:
    token = file.readline()

bot = telebot.TeleBot(token)


session_started = False
word = ""
letters = dict()
words = words_file.data


@bot.message_handler(commands=['start'])
def start(message):
    global session_started
    global words
    global letters
    words = words_file.data
    letters = dict()
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


def show_inline_words_keyboard(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    for i in range(0, len(words), 2):
        if len(words) - (i+1) > 1:
            keyboard.row(types.InlineKeyboardButton(words[i].upper(), callback_data=words[i]),
                         types.InlineKeyboardButton(words[i+1].upper(), callback_data=words[i+1]))
        else:
            keyboard.row(types.InlineKeyboardButton(words[i].upper(), callback_data=words[i]))

    bot.send_message(chat_id, "Выберите слово:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_inline_callback(call):

    global letters
    global words

    if call.data in words:
        call.message.text = call.data
        handle_word(call.message)

    if (call.data[2] in word) and (call.data[0].isdigit()) and (call.data[1] in '=+-'):
        sym_letter = call.data[1:]
        index = int(call.data[0])
        letters[index] = sym_letter
        status = ''
        if sym_letter[0] == '=':
            status = 'есть, стоит на своём месте'
        elif sym_letter[0] == '+':
            status = 'есть, но стоит не на своём месте'
        elif sym_letter[0] == '-':
            status = 'отсутствует'
        bot.answer_callback_query(call.id, text=f'Буква {sym_letter[1]} {status}')

    if call.data == 'confirm':
        if len(letters) == 5:
            words = find_words(letters, words)
            show_inline_words_keyboard(call.message.chat.id)
            letters = dict()
        else:
            five_numbers = set(range(5))
            five_numbers.difference_update(set(letters.keys()))
            difference_letters = ',  '.join([f"{word[i]}({i+1})" for i in list(five_numbers)])
            bot.send_message(call.message.chat.id, f"Вы не назначили состояние буквам: {difference_letters}")

    if call.data == 'cancel':
        bot.send_message(call.message.chat.id, "Слово отменено и список слов обновлён до начального.\n"
                                               "Напишите /start чтобы начать разгадывать слово.")
        letters = dict()
        global session_started
        session_started = False


bot.polling()
