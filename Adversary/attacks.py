from random import choice, randint, sample, randrange
from string import punctuation

from constants import *

'''These act on a single text'''


def good_word_attack(text):
    if randint(1, 2) == 1:
        return text + ' ' + ' '.join(sample(NEUTRAL_WORDS, randint(5, 15)))
    else:
        return ' '.join(sample(NEUTRAL_WORDS, randint(2, 10))) + ' ' + text


def swap_words(text):
    words = text.split()
    if len(words) <= 3:
        return ' '.join(words)
    swapped = list(range(len(words)))
    idxs = sample(range(1, len(words) - 2), randint(1, min(3, len(words) // 2 - 1)))
    for i in idxs:
        swapped[i], swapped[i + 1] = swapped[i + 1], swapped[i]
    return ' '.join([words[i] for i in swapped])


def remove_spacing(text):
    chars = list(text)
    for i, c in enumerate(chars):
        if c == ' ' and randint(1, 3) == 1:
            chars[i] = choice(',.-'"`*")
    return ''.join(chars)


'''These act on a single word within a text'''


def synonym(word):
    return choice(SYNONYMS.get(word, [word]))


def letter_to_symbol(word):
    return ''.join([choice(HOMOGLPYH_MAP.get(c.lower(), [c])) for c in word])


def swap_letters(word):
    if len(word) < 4:
        return word
    swapped = list(range(len(word)))
    max_swap = randint(1, min(3, len(word) // 2 - 1))
    idxs = sample(range(1, len(word) - 2), max_swap)
    for i in idxs:
        swapped[i], swapped[i + 1] = swapped[i + 1], swapped[i]
    return ''.join([word[i] for i in swapped])


def insert_punctuation(word):
    word_with_punct = list(word)
    for _ in range(2):
        word_with_punct.insert(randrange(len(word_with_punct)), choice(punctuation))
    return ''.join(word_with_punct)


def insert_duplicate_characters(word):
    word_with_dupes = list(word)
    for _ in range(2):
        i = randrange(len(word_with_dupes))
        word_with_dupes.insert(i, word_with_dupes[i])
    return ''.join(word_with_dupes)


def delete_characters(word):
    if len(word) < 4:
        return word
    max_del = 1 if len(word) <= 5 else 2
    idxs_delete = sample(range(1, len(word) - 1), max_del)
    return ''.join([c for i, c in enumerate(
        list(word)) if i not in idxs_delete])


def change_case(word):
    word_with_changed_case = list(word)
    idx = sample(range(len(word)), randint(1, len(word)))
    for i in idx:
        c = word[i]
        word_with_changed_case[i] = c.upper() if c.lower() == c else c.lower()
    return ''.join(word_with_changed_case)


def num_to_word(word):
    return NUM_TO_WORD.get(word, word)


'''Keeps track of all attacks and their types'''

ATTACK_MAP = {
    'text': {
        'good_word_attack': good_word_attack,
        'swap_words': swap_words,
        'remove_spacing': remove_spacing,
    },
    'word': {
        'synonym': synonym,
        'letter_to_symbol': letter_to_symbol,
        'swap_letters': swap_letters,
        'insert_punctuation': insert_punctuation,
        'insert_duplicate_characters': insert_duplicate_characters,
        'delete_characters': delete_characters,
        'change_case': change_case,
        'num_to_word': num_to_word
    }
}
