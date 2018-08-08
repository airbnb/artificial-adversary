from Adversary.attacks import *

def test_num_to_word():
    assert(num_to_word('1') == 'one')
    assert(num_to_word('dog') == 'dog')
