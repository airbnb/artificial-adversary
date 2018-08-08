import pickle
from itertools import chain, combinations


def polite_printer(s, verbose=False):
    if verbose:
        print(s)


def pickle_to_file(fname, obj, output=None):
    if output is not None:
        with open(output + fname, 'wb') as f:
            pickle.dump(obj, f)


def flatten_unique(l):
    l_flat = []
    for l_i in l:
        for l_ij in l_i:
            l_flat.append(l_ij)
    return list(set(l_flat))


def combinations_of_len(l, k):
    return list(chain.from_iterable(combinations(l, r) for r in range(1, k + 1)))


def fancy_titles(cols):
    return [' '.join([c_w.title() for c_w in c.split('_')]) for c in cols]
