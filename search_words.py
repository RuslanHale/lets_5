def dict_to_word(num_sym_letters):
    result_word = str()
    for key in range(5):
        result_word += num_sym_letters[key]
    return result_word


def alphabet_selection(input_word):
    selected_alphabet = dict()
    input_word = input_word.lower()
    for i in range(0, len(input_word)-1, 2):
        sym = input_word[i]
        alpha = input_word[i+1]
        selected_alphabet.setdefault(alpha, dict())
        selected_alphabet[alpha].setdefault(sym, list()).append(i // 2)
    return selected_alphabet


def word_selection(selected_alphabet, selected_words) -> list:
    for key, val in selected_alphabet.items():
        for sym in val.keys():
            if sym == '=':
                for index in selected_alphabet[key][sym]:
                    selected_words = list(filter(lambda x: x[index] == key, selected_words))
            elif sym == '+':
                for index in selected_alphabet[key][sym]:
                    number_alpha = len(selected_alphabet[key][sym] + selected_alphabet[key].get('=', list()))
                    selected_words = (
                        list(filter(lambda x: x[index] != key and number_alpha <= x.count(key), selected_words)))
            elif sym == '-':
                for index in selected_alphabet[key][sym]:
                    selected_words = (
                        list(filter(lambda x: x[index] != key and not (key in x and len(selected_alphabet[key]) == 1),
                                    selected_words)))
                if len(val.keys()) > 1:
                    number_alpha = len(selected_alphabet[key].get('+', []) + selected_alphabet[key].get('=', []))
                    selected_words = list(filter(lambda x: x.count(key) >= number_alpha, selected_words))
    return selected_words


def find_words(num_sym_letters: dict, words_base: list) -> list:
    input_word = dict_to_word(num_sym_letters)
    alphabet = alphabet_selection(input_word)
    output_words = word_selection(alphabet, words_base)
    return output_words
