import words_file


def alphabet_selection(input_word, selected_alphabet):

    input_word = input_word.lower()
    for i in range(0, len(input_word)-1, 2):
        if input_word[i] == '=':
            selected_alphabet[input_word[i + 1]].setdefault('=', list()).append(i//2)
            # example: word 'ВАННА' selected_alphabet['а']['='] returns: [1, 4]
        elif input_word[i] == '+':
            selected_alphabet[input_word[i + 1]].setdefault('+', list()).append(i//2)
        elif input_word[i] == '-':
            selected_alphabet[input_word[i + 1]].setdefault('-', list()).append(i//2)
    return selected_alphabet


def word_selection(selected_alphabet, selected_words):
    for key, val in selected_alphabet.items():
        for sym in val.keys():
            if sym == '=':
                for index in selected_alphabet[key][sym]:
                    selected_words = list(filter(lambda x: x[index] == key, selected_words))
            elif sym == '+':
                for index in selected_alphabet[key][sym]:
                    selected_words = list(filter(lambda x: x[index] != key and len(selected_alphabet[key][sym] + selected_alphabet[key].get('=', list())) == x.count(key), selected_words))
            elif sym == '-':
                for index in selected_alphabet[key][sym]:
                    selected_words = list(filter(lambda x: x[index] != key and not (key in x and len(selected_alphabet[key]) == 1), selected_words))

    return selected_words


word = input('Введите новое слово: ')
alphabet = {chr(i): dict() for i in range(ord('а'), ord('а')+32)}
words = words_file.data


while word != 'stop':
    print(word)
    alphabet = alphabet_selection(word, alphabet)
    words = word_selection(alphabet, words)
    alphabet = {chr(i): dict() for i in range(ord('а'), ord('а')+32)}
    print(words)
    word = input('Введите новое слово: ')

# +П-А-Л-А-Ч
# -В-Е+П+Р-Ь
# -И=П=Р-И-Т
# -О=П=Р=О=С
# Нет смысла идти по всем 33 буквам алфавита. Можно переделать вообще не используя алфавит.