# -*- coding: utf-8 -*-
# @Time    : 2024-08-01 9:05
# @Author  : sun bo
# @File    : mga_v2.py
# @Software: PyCharm

# Refacor of mga.py

import math

import pandas as pd
import numpy as np
import random
from collections import Counter

import xxhash

from frequency.LDPprotocol import LDPProtocol
from frequency.krr import KRR
from frequency.olh import OLH
from frequency.oue_v2 import OUE


class MGA():
    def __init__(self, protocol : LDPProtocol, r=5, beta=0.05, num_hash_funcs=100):
        self.protocol = protocol
        self.beta = beta
        self.r = r      # number of target items
        self.target_items = []
        self.num_hash_funcs = num_hash_funcs    # number of sampled hash functions for OLH

    def select_target_items(self):
        self.target_items = random.sample(list(self.protocol.domain), self.r)

    def craft_perturbed_value(self):
        """
        craft perturbed value for a fake user according to specific LDP protocol
        :param file_path: dataset
        :return: a perturbed_value, an item, a binary vector or (hash_func, hash_val)
        """
        if isinstance(self.protocol, OUE):
            binary_vector = [1 if item in self.target_items else 0 for item in self.protocol.domain]

            # non-target bits of the perturbed vector
            l = math.floor(self.protocol.p + (self.protocol.d - 1) * self.protocol.q - self.r)
            additional_ones_index = random.sample([i for i in range(len(self.protocol.domain)) if self.protocol.domain[i] not in self.target_items], l)
            for idx in additional_ones_index:
                binary_vector[idx] = 1
            return binary_vector

        elif isinstance(self.protocol, KRR):
            return random.choice(self.target_items)

        elif isinstance(self.protocol, OLH):
            max_hash_count = 0
            best_perturbed_value = None
            for h in range(self.num_hash_funcs):   # seed represents the hash function
                hash_vals = [xxhash.xxh32(str(item), seed=h).intdigest() % self.protocol.d_dot for item in self.target_items]
                most_common_hash_value = max(hash_vals, key=hash_vals.count)
                count = hash_vals.count(most_common_hash_value)
                if count > max_hash_count:
                    max_hash_count = count
                    best_perturbed_value = dict(hash_func=h, hash_val=most_common_hash_value)
            return best_perturbed_value

        else:
            raise ValueError("Unsupported LDP protocol")


    def generate_fake_users(self, num_fake_users):
        fake_perturbed_values = []
        for _ in range(num_fake_users):
            fake_perturbed_values.append(self.craft_perturbed_value())
        return fake_perturbed_values

    def cal_frequencies(self, perturbed_values):
        return self.protocol.aggregate(perturbed_values)


    def run_mga(self, file_path):
        df = self.protocol.load_data(file_path)
        n = df['Word'].count()

        genuine_user_perturbed_values = [self.protocol.perturb(self.protocol.encode(r)) for r in df['Word']]
        self.select_target_items()
        original_fre = self.cal_frequencies(genuine_user_perturbed_values)

        num_fake_users = int(n * self.beta)
        fake_perturbed_values = self.generate_fake_users(num_fake_users)

        combined_perturbed_vals = genuine_user_perturbed_values + fake_perturbed_values
        attacked_fre = self.cal_frequencies(combined_perturbed_vals)

        # convert frequencies to dictionaries
        if isinstance(original_fre, list):
            original_fre_dic = dict(zip(self.protocol.domain, original_fre))
            attacked_fre_dic = dict(zip(self.protocol.domain, attacked_fre))
        elif isinstance(original_fre, Counter):
            original_fre_dic = dict(original_fre)
            attacked_fre_dic = dict(attacked_fre)
        elif isinstance(original_fre, dict):
            original_fre_dic = original_fre
            attacked_fre_dic = attacked_fre
        else:
             raise ValueError("Unsupported aggregate result type")

        frequency_gains = {item: attacked_fre_dic.get(item,0) - original_fre_dic.get(item,0) for item in self.target_items}
        overall_gain = sum(frequency_gains.values())

        return frequency_gains, overall_gain

if __name__ == "__main__":
    protocol = OLH(epsilon=1)
    # protocol = KRR()
    # protocol = OUE()

    mga = MGA(protocol=protocol)
    frequency_gains, overall_gain = mga.run_mga('D:\LDP\data\small_synthetic_dataset.xlsx')

    output_file_path = r'D:\LDP\result\frequency gains and overall gain of MGA for OLH (small dataset).xlsx'
    df_gains = pd.DataFrame(list(frequency_gains.items()), columns=['target item', 'frequency gain'])
    df_overall = pd.DataFrame({'overall gain': [overall_gain]})
    df_combined = pd.concat([df_gains, df_overall], axis=1)
    df_combined.to_excel(output_file_path, index=False)