from Adversary.attacks import *

def test_num_to_word():
    assert(num_to_word('1') == 'one')
    assert(num_to_word('dog') == 'dog')

def test_remove_surrounding_characters():
    assert(remove_surrounding_characters('(b)(a)(n)(k)') == 'bank')
    assert(remove_surrounding_characters('[l]uigi') == 'luigi')
    assert(remove_surrounding_characters('mario') == 'mario')
