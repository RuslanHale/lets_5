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


def word_selection(selected_alphabet, selected_words,  letter_positions):

    for key, val in selected_alphabet.items():
        for sym in val.keys():
            print(selected_alphabet[key][sym])
            if sym == '=':
                for index in selected_alphabet[key][sym]:
                    selected_words = list(filter(lambda x: x[index] == key, selected_words))
            elif sym == '+':
                for index in selected_alphabet[key][sym]:
                    selected_words = list(filter(lambda x: x[index] != key and len(selected_alphabet[key][sym]) == x.count(key), selected_words))
            elif sym == '-':
                for index in selected_alphabet[key][sym]:
                    selected_words = list(filter(lambda x: x[index] != key, selected_words))
    return selected_words


word = '-Д=А=М-Б+А'
alphabet = {chr(i): dict() for i in range(ord('а'), ord('а')+32)}
words = words_file.data
positions = list(range(5))


while word != 'stop':
    print(word)
    print(len(words))
    alphabet = alphabet_selection(word, alphabet)
    words = word_selection(alphabet, words, positions)
    print(words)
    print(len(words))
    word = input('Введите новое слово: ')

# Статус буквы заменятся в функции alphabet_selection. Имеет смысл сделать значением список и идти по списку
# например буква А: с '=' изменяется на '+'