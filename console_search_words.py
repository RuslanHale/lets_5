import words_file
import search_words


words = words_file.data

if __name__ == '__main__':
    word = str(input())
    while word != 'stop':
        print(word)
        alphabet = search_words.alphabet_selection(word)
        words = search_words.word_selection(alphabet, words)
        print(words)
        word = input('Введите новое слово: ')



# +П-А-Л-А-Ч
# -В-Е+П+Р-Ь
# -И=П=Р-И-Т
# -О=П=Р=О=С
