from copy import copy
from functools import partial
from random import random, seed

import pandas as pd
from textblob import TextBlob

from Adversary.attacks import *
from Adversary.utils import *


class Adversary:
    def __init__(self, verbose=False, output=None):
        """
        Initializes Adversary object that generates data-sets and conducts attacks.

        :param verbose: Determines amount of output to print -- False for none, True for all
        :type verbose: bool
        :param output: Directory of output folder with trailing slash
        :type output: Union[str, None]
        """
        self.save_output = partial(pickle_to_file, output=output)
        self.print_progress = partial(polite_printer, verbose=verbose)

    def generate(self, texts, text_sample_rate=1.0, word_sample_rate=0.3, attacks='all', max_attacks=2, random_seed=None, save=False):
        """
        Generates attacked set of texts based off of original texts.

        :param texts: List of original strings
        :type texts: list
        :param text_sample_rate: P(individual text is attacked) if in [0, 1], else, number of attacks per text
        :type text_sample_rate: Union[int, float]
        :param word_sample_rate: P(word_i is sampled in a given word attack | word's text is sampled)
        :type word_sample_rate: float
        :param attacks: Description of attack configuration
        :type attacks: Union[str, list, dict]
        :param max_attacks: Maximum number of attacks that can be applied to a single text
        :type max_attacks: int
        :param random_seed: Seed for calls to random module functions
        :type random_seed: int
        :param save: Whether the generated texts should be pickled as output
        :type save: bool
        :return: List of tuples of generated strings in format (attacked text, list of attacks, index of original text)
        :rtype: list
        """
        if random_seed:
            seed(random_seed)

        text_type = type(texts[0])

        text_attacks = list(ATTACK_MAP['text'].keys())
        word_attacks = list(ATTACK_MAP['word'].keys())
        config = self._read_config(attacks)

        if text_sample_rate > 1:
            num_iters = int(text_sample_rate)
        else:
            num_iters = 1
        total_num = num_iters * len(texts)

        # list of tuples containing (attacked text, list of attacks used, index of original text)
        generated = []
        original = copy(texts)
        for iter_no in range(num_iters):
            texts = copy(original)
            for i in range(len(texts)):
                if i % 100 == 0:
                    cur_num = iter_no * len(texts) + i
                    self.print_progress('Generating attacked version of string {} out of {}'.format(cur_num, total_num))
                if text_sample_rate >= random():
                    num_attacks = 0
                    used_attacks = []
                    sorted_attacks = sorted([tuple(c) for c in config.items()],
                                            key=lambda a: self._precendence(a[0], word_attacks, text_attacks))
                    for attack, pr in sorted_attacks:
                        if pr >= random():
                            num_attacks += 1
                            if num_attacks > max_attacks:
                                break
                            used_attacks.append(attack)
                            if attack in text_attacks:
                                texts[i] = ATTACK_MAP['text'][attack](texts[i])
                            elif attack in word_attacks:
                                blob = TextBlob(texts[i]).tags
                                words_attacked = texts[i].split()
                                for j, word_with_tag in enumerate(blob):
                                    if self._should_attack_word(word_with_tag[1]) and word_sample_rate >= random():
                                        try:
                                            words_attacked[j] = ATTACK_MAP['word'][attack](word_with_tag[0])
                                        except IndexError:
                                            pass
                                texts[i] = ' '.join(words_attacked)
                    generated.append((text_type(texts[i]), used_attacks, i))
                else:
                    generated.append((text_type(texts[i]), [], i))

        if save:
            pickle_to_file('generated_text.pkl', generated)

        return generated

    def _read_config(self, attacks):
        if attacks == 'all':
            config = [(t_a, 1. / len(ATTACK_MAP['text'])) for t_a in ATTACK_MAP['text']] + \
                [(w_a, 1. / len(ATTACK_MAP['word'])) for w_a in ATTACK_MAP['word']]
            return dict(config)
        elif isinstance(attacks, list):
            selected_text_attacks = [t_a for t_a in attacks if t_a in ATTACK_MAP['text']]
            selected_word_attacks = [w_a for w_a in attacks if w_a in ATTACK_MAP['word']]
            config = [(t_a, 1. / len(selected_text_attacks)) for t_a in selected_text_attacks] + \
                [(w_a, 1. / len(selected_word_attacks)) for w_a in selected_word_attacks]
            return dict(config)
        elif isinstance(attacks, dict):
            return attacks

    def _precendence(self, attack, word_attacks, text_attacks):
        if attack in word_attacks:
            return 2
        elif attack == 'good_word_attack':
            return 1
        elif attack in text_attacks:
            return 0
        else:
            return None

    def _should_attack_word(self, tag):
        return tag[0] in ['N', 'V', 'J'] or tag == 'CD'

    def attack(self, texts_original, texts_generated, predict_function, save=False):
        """
        Given a list of generated texts, simulate attack and return performance metrics.

        :param texts_original: List of original texts
        :type texts_original: list
        :param texts_generated: List of generated texts (output of generate function)
        :type texts_generated: list
        :param predict_function: Function that maps strings to classification label (0 or 1)
        :type predict_function: (str) -> int
        :param save: Whether the generated metrics DataFrames should be pickled as output
        :type save: bool
        :return: Two DataFrames containing performance metrics
        :rtype: (pd.DataFrame, pd.DataFrame)
        """
        texts_original_flat = [texts_original[t_g[2]] for t_g in texts_generated]
        texts_generated_flat = [t_g[0] for t_g in texts_generated]
        attacks_applied = [t_g[1] for t_g in texts_generated]

        original_preds = [predict_function(t_o) for t_o in texts_original_flat]
        generated_preds = [predict_function(t_g) for t_g in texts_generated_flat]

        self.print_progress('Accuracy on original texts: {}'.format(1. * sum(original_preds) / len(original_preds)))
        self.print_progress('Accuracy on generated texts: {}'.format(1. * sum(generated_preds) / len(generated_preds)))

        misclassifications_single = self._get_misclassifications_single(original_preds, generated_preds, attacks_applied)
        misclassifications_group = self._get_misclassifications_group(original_preds, generated_preds, attacks_applied)

        if save:
            pickle_to_file('misclassifications_df_single.pkl', misclassifications_single)
            pickle_to_file('misclassifications_df_group.pkl', misclassifications_group)

        return misclassifications_single, misclassifications_group

    def _get_misclassifications_single(self, original_preds, generated_preds, attacks_applied):
        results = zip(original_preds, generated_preds, attacks_applied)
        misclassifications_single = dict([(att, 0) for att in flatten_unique(attacks_applied)])
        always_wrong_single = copy(misclassifications_single)
        never_wrong_single = copy(misclassifications_single)

        for i, res in enumerate(results):
            original, generated, applied = res[0], res[1], res[2]
            if original == 1 and generated == 0:
                for attack in applied:
                    misclassifications_single[attack] += 1
            elif original == 1 and generated == 1:
                for attack in applied:
                    always_wrong_single[attack] += 1
            elif original == 0 and generated == 0:
                for attack in applied:
                    never_wrong_single[attack] += 1

        index_fancy = fancy_titles(misclassifications_single.keys())
        return pd.DataFrame(
            list(zip(misclassifications_single.values(), always_wrong_single.values(), never_wrong_single.values())),
            index=index_fancy,
            columns=['Caused Misclassifications', 'Always Misclassified', 'Never Misclassified']
        ).rename_axis('Attack')

    def _get_misclassifications_group(self, original_preds, generated_preds, attacks_applied):
        results = list(zip(original_preds, generated_preds, attacks_applied))
        attacks_used = flatten_unique(attacks_applied)
        misclassifications_group = dict([(','.join(sorted(att)), 0) for att in attacks_applied])
        always_wrong_group = copy(misclassifications_group)
        never_wrong_group = copy(misclassifications_group)
        for i, res in enumerate(results):
            original, generated, applied = res[0], res[1], res[2]
            if original == 1 and generated == 0:
                misclassifications_group[','.join(sorted(applied))] += 1
            elif original == 1 and generated == 1:
                always_wrong_group[','.join(sorted(applied))] += 1
            elif original == 0 and generated == 0:
                never_wrong_group[','.join(sorted(applied))] += 1

        cols = sorted(attacks_used) + ['Caused Misclassifications', 'Always Misclassified', 'Never Misclassified']
        all_combos = combinations_of_len(attacks_used, max([len(res[2]) for res in results]))
        misclassifications_df_list = []
        for i, combo in enumerate(all_combos):
            row = [' '] * len(cols)
            for att in combo:
                row[cols.index(att)] = 'X'
            row[-3] = misclassifications_group.get(','.join(sorted(combo)), 0)
            row[-2] = never_wrong_group.get(','.join(sorted(combo)), 0)
            row[-1] = always_wrong_group.get(','.join(sorted(combo)), 0)
            misclassifications_df_list.append(row)
        misclassifications_df_list = sorted(misclassifications_df_list, key=lambda x: x[-3], reverse=True)

        cols_fancy = fancy_titles(cols)
        df = pd.DataFrame(misclassifications_df_list, columns=cols_fancy)
        return df
