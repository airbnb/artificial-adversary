from Adversary.utils import *

def test_flatten_unique():
    l = [[1, 2], [1, 3, 4], [5]]
    assert(flatten_unique(l) == [1, 2, 3, 4, 5])

def test_combinations_of_len():
    l = [1, 2, 3]
    assert(combinations_of_len(l, 2) == [(1,), (2,), (3,), (1, 2), (1, 3), (2, 3)])

def test_fancy_titles():
    cols = ['change_case', 'insert_duplicate_characters', 'synonym']
    assert(fancy_titles(cols) == ['Change Case', 'Insert Duplicate Characters', 'Synonym'])
