# -*- coding: utf-8 -*-
# @Time    : 2024-07-28 23:22
# @Author  : sun bo
# @File    : krr.py
# @Software: PyCharm
import random

import pandas as pd
import numpy as np
import math
from collections import Counter
from frequency.LDPprotocol import LDPProtocol

class KRR(LDPProtocol):
    def __init__(self, epsilon=1):
        super().__init__(epsilon)
        self.p = None
        self.q = None
        self.d = 0  # size of domain


    def load_data(self, file_path):
        dataframe = pd.read_excel(file_path)
        self.domain = np.sort(dataframe['Word'].dropna().unique())
        self.d = len(self.domain)
        self.p = math.e**self.epsilon / (self.d - 1 + math.e**self.epsilon)
        self.q = 1 / (self.d - 1 + math.e**self.epsilon)
        return dataframe

    def encode(self, raw_item):
        return raw_item

    def perturb(self, encoded_value):
        sample = np.random.random()
        # print("Type of encoded_value:", type(encoded_value))
        filter_domain = []
        for x in self.domain:
            if x != encoded_value:
                filter_domain.append(x)
        return encoded_value if sample <= self.p else random.choice(filter_domain)

    def aggregate(self, perturbed_values):
        counts = Counter(perturbed_values)
        frequencies = counts.copy()     # frequency
        n = len(perturbed_values)
        for num in frequencies:
            frequencies[num] = ( (1 / n) * counts[num] - self.q) / (self.p - self.q)
        return frequencies   # the return type is Counter (Iterable Container)


    def run(self, file_path):
        dataframe = self.load_data(file_path)
        perturbed_values = [self.perturb(self.encode(r)) for r in dataframe['Word']]
        return self.aggregate(perturbed_values)

if __name__ == "__main__":
    krr = KRR()
    item_frequencies = krr.run('D:\LDP\data\synthetic_dataset.xlsx')

    item_frequencies = [(k,v) for k,v in item_frequencies.items()]

    # write the frequency result to file
    df_frequencies = pd.DataFrame(item_frequencies, columns=['Word', 'Frequency Estimation'])
    output_file_path = r'D:\LDP\result\Frequency estimation of krr for synthetic dataset.xlsx'
    df_frequencies.to_excel(output_file_path, index=False)

    print(f"Results written to {output_file_path}")