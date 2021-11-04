import json
import os
from random import choice, randint, sample, randrange
from string import punctuation

import spacy
from regex import search
from spacy import displacy

from constants import *

'''These act on a single text'''


def emojis_attack(text):
    text = text.lower()
    words = text.split()

    # get the emojis path
    script_dir = os.path.dirname(__file__)
    rel_path = "assets/emoji.json"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, 'r') as emojis:
        # load emojis as lists
        json_data = json.load(emojis)
        for emoji in json_data:
            # extract each emoji tags
            tags_list = emoji['tags'] + emoji['aliases'] + [emoji['description']]
            # check if there are any possible keywords in the text
            emojis_in_text = set(words) & set(tags_list)
            if len(emojis_in_text) > 0:
                # source https://stackoverflow.com/questions/15658187/replace-all-words-from-word-list-with-another-string-in-python
                big_regex = re.compile(r'\b%s\b' % r'\b|\b'.join(map(re.escape, emojis_in_text)))
                text = big_regex.sub(emoji['emoji'], str(text))

    return text


def advanced_emojis_attack(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text.lower())

    # get the emojis path
    script_dir = os.path.dirname(__file__)
    rel_path = "assets/emoji.json"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, 'r') as emojis:
        # load emojis as lists
        json_data = json.load(emojis)
        for emoji in json_data:
            # extract each emoji tags
            tags_list = emoji['tags'] + emoji['aliases'] + [emoji['description']]
            for token in doc:
                if (token.pos_ == "PROPN" or token.pos_ == "VERB"
                    or token.pos_ == "SYM" or token.pos_ == "NOUN") \
                        and token.text in tags_list:
                    # source https://stackoverflow.com/questions/15658187/replace-all-words-from-word-list-with-another-string-in-python
                    big_regex = re.compile(r'\b%s\b' % r'\b|\b'.join(map(re.escape, [token.text])))
                    text = big_regex.sub(emoji['emoji'], str(text.lower()))

    # uncomment to launch analysis in browser
    # displacy.serve(doc, style="dep")

    return text


def surrounding_chars(text):
    text = text.lower()

    # get the spam texts file path
    script_dir = os.path.dirname(__file__)
    rel_path = "assets/spam_data.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, 'r') as spam:
        spam_list = spam.read().split(",")
        spam_list_lowered = list(map(str.lower, spam_list))

        for spam_word in spam_list_lowered:
            # start surrounding to text if it is in spam
            if search(spam_word, text):
                # source https://stackoverflow.com/questions/15658187/replace-all-words-from-word-list-with-another-string-in-python
                big_regex = re.compile(r'\b%s\b' % r'\b|\b'.join(map(re.escape, [spam_word])))
                surround_char = ' '.join('("' + item + '")' for item in spam_word if item != " ")
                text = big_regex.sub(surround_char, str(text.lower()))

    return text


def homophones_chars(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text.lower())

    # get the spam texts file path
    script_dir = os.path.dirname(__file__)
    rel_path = "assets/homophones.json"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, 'r') as homophones:
        # load homophones as list
        json_data = json.load(homophones)

        for token in doc:
            if (token.pos_ == "PROPN" or token.pos_ == "VERB"
                or token.pos_ == "SYM" or token.pos_ == "NOUN") \
                    and token.text in json_data:
                # source https://stackoverflow.com/questions/15658187/replace-all-words-from-word-list-with-another-string-in-python
                big_regex = re.compile(r'\b%s\b' % r'\b|\b'.join(map(re.escape, [token.text])))
                text = big_regex.sub(json_data[token.text][0], str(text.lower()))

    return text


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
        'emoji_attack': emojis_attack,
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
