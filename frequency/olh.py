# -*- coding: utf-8 -*-
# @Time    : 2024-07-28 23:22
# @Author  : sun bo
# @File    : olh.py
# @Software: PyCharm
import random

import numpy as np
import pandas as pd
import math
import xxhash
from frequency.LDPprotocol import LDPProtocol

SIZE_OF_HASH_FUNCTION = 1000

class OLH(LDPProtocol):
    def __init__(self, epsilon = 5):
        super().__init__(epsilon)
        self.p = None
        self.q = None
        self.d = 0  # size of domain
        self.d_dot = int(math.e**self.epsilon + 1) + 1  # achieve the best performance
        self.domain_dot = [i for i in range(self.d_dot)]    # reduced domin size after the hash function

        # overall probability parameters for OLH
        self.p_ = self.p
        self.q_ = 1 / self.d_dot

    def load_data(self, file_path):
        dataframe = pd.read_excel(file_path)
        self.domain = np.sort(dataframe['Word'].dropna().unique())
        self.d = len(self.domain)
        self.p = (math.e**self.epsilon) / (math.e**self.epsilon + self.d_dot - 1)
        self.q = 1 / (math.e**self.epsilon + self.d_dot - 1)
        self.p_ = self.p
        return dataframe

    def encode(self, raw_item):
        seed = raw_item
        # hash_func = xxhash.xxh32(seed=seed) # let the seed represent the hash function
        # hash_func.update(str(raw_item))
        hash_val = xxhash.xxh32(str(raw_item), seed=seed).intdigest() % self.d_dot
        return dict(hash_func=seed, hash_val=hash_val)


    def perturb(self, encoded_value):
        sample = np.random.random()
        filter_domain_dot = []
        for x in self.domain_dot:
            if x != encoded_value['hash_val']:
                filter_domain_dot.append(x)
        perturbed_hash_val = encoded_value['hash_val'] if sample <= self.p else random.choice(filter_domain_dot)
        return dict(hash_func=encoded_value['hash_func'], hash_val=perturbed_hash_val)

    def aggregate(self, perturbed_values):
        counts = {unique_item : 0 for unique_item in self.domain}  # dictionary.  key: item   value: estimated count
        frequencies = counts.copy()
        n = len(perturbed_values)   # number of users(perturbed_values)
        for ui in self.domain:
            for pv in perturbed_values:
                seed = pv['hash_func']
                if pv['hash_val'] == (xxhash.xxh32(str(ui), seed=seed).intdigest() % self.d_dot):
                    counts[ui] += 1

        # estimated count
        for ui in frequencies:
            frequencies[ui] = ( (1 / n) * counts[ui] - self.q_) / (self.p_ - self.q_)
        return frequencies      # the return type is the dictionary

    def run(self, file_path):
        dataframe = self.load_data(file_path)
        perturbed_values = [self.perturb(self.encode(r)) for r in dataframe['Word']]
        return self.aggregate(perturbed_values)

if __name__ == "__main__":
    olh = OLH()
    item_frequencies = olh.run('D:\LDP\data\synthetic_dataset.xlsx')

    item_frequencies = [(k,v) for k,v in item_frequencies.items()]

    df_frequencies = pd.DataFrame(item_frequencies, columns=['Word', 'Frequency Estimation'])
    output_file_path = r'D:\LDP\result\Frequency estimation of olh for synthetic dataset.xlsx'
    df_frequencies.to_excel(output_file_path, index=False)

    print(f"Results written to {output_file_path}")