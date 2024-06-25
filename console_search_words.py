import words_file


def alphabet_selection(input_word):
    selected_alphabet = dict()
    input_word = input_word.lower()
    for i in range(0, len(input_word)-1, 2):
        sym = input_word[i]
        alpha = input_word[i+1]
        selected_alphabet.setdefault(alpha, dict())
        selected_alphabet[alpha].setdefault(sym, list()).append(i // 2)
    return selected_alphabet


def word_selection(selected_alphabet, selected_words):
    for key, val in selected_alphabet.items():
        for sym in val.keys():
            if sym == '=':
                for index in selected_alphabet[key][sym]:
                    selected_words = list(filter(lambda x: x[index] == key, selected_words))
            elif sym == '+':
                for index in selected_alphabet[key][sym]:
                    number_alpha = len(selected_alphabet[key][sym] + selected_alphabet[key].get('=', list()))
                    selected_words = (
                        list(filter(lambda x: x[index] != key and number_alpha == x.count(key), selected_words)))
            elif sym == '-':
                for index in selected_alphabet[key][sym]:
                    selected_words = (
                        list(filter(lambda x: x[index] != key and not (key in x and len(selected_alphabet[key]) == 1),
                                    selected_words)))
                if len(val.keys()) > 1:
                    number_alpha = len(selected_alphabet[key].get('+', []) + selected_alphabet[key].get('=', []))
                    selected_words = list(filter(lambda x: x.count(key) == number_alpha, selected_words))
    return selected_words


words = words_file.data
word = input()

while word != 'stop':
    print(word)
    alphabet = alphabet_selection(word)
    words = word_selection(alphabet, words)
    print(words)
    word = input('Введите новое слово: ')

# +П-А-Л-А-Ч
# -В-Е+П+Р-Ь
# -И=П=Р-И-Т
# -О=П=Р=О=С
