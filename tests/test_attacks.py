from attacks import *


def test_num_to_word():
    assert (num_to_word('1') == 'one')
    assert (num_to_word('dog') == 'dog')


print(emojis_attack("please send me 10,000 US DOLLARS to bank of scamland"))
print(advanced_emojis_attack("please send me 10,000 US DOLLARS to bank of scamland"))
print(surrounding_chars("please wire me 10,000 US DOLLARS to the bank of baghdad"))
print(homophones_chars("please wire me 10,000 US DOLLARS to the bank of baghdad"))
