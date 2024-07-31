# -*- coding: utf-8 -*-
# @Author  : sun bo
# @File    : oue.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import math
from frequency.LDPprotocol import LDPProtocol

class OUE(LDPProtocol):
    def __init__(self, epsilon=5, p=0.5):
        super().__init__(epsilon)
        self.p = p
        self.q = 1 / (math.exp(epsilon) + 1)

    def load_data(self, file_path):
        dataframe = pd.read_excel(file_path)
        self.domain = np.sort(dataframe['Word'].dropna().unique())
        self.d = len(self.domain)
        return dataframe

    def encode(self, raw_item):
        return [1 if d == raw_item else 0 for d in self.domain]

    def perturb(self, encoded_value):
        return [self.perturb_bit(b) for b in encoded_value]

    def perturb_bit(self, bit):
        sample = np.random.random()
        if bit == 1:
            return 1 if sample <= self.p else 0
        else:
            return 1 if sample <= self.q else 0

    def aggregate(self, perturbed_values):
        sums = np.sum(perturbed_values, axis=0)
        n = len(perturbed_values)
        # counts = [(sum - n * self.q) / (self.p - self.q) for sum in sums]     # numbers
        frequencies = [((1 / n) * sum - self.q) / (self.p - self.q) for sum in sums]
        return frequencies

    def run(self, file_path):
        dataframe = self.load_data(file_path)
        perturbed_values = [self.perturb(self.encode(r)) for r in dataframe['Word']]
        frequencies = self.aggregate(perturbed_values)
        return list(zip(self.domain, frequencies))


if __name__ == "__main__":
    oue = OUE()
    item_frequencies = oue.run('D:\LDP\data\synthetic_dataset.xlsx')

    # write the frequency result to file
    df_frequencies = pd.DataFrame(item_frequencies, columns=['Word', 'Frequency Estimation'])
    output_file_path = r'D:\LDP\result\Frequency estimation of oue for synthetic dataset.xlsx'
    df_frequencies.to_excel(output_file_path, index=False)

    print(f"Results written to {output_file_path}")