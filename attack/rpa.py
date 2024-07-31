# -*- coding: utf-8 -*-
# @Time    : 2024-07-30 17:52
# @Author  : sun bo
# @File    : rpa.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import random
from frequency.LDPprotocol import LDPProtocol
from frequency.oue_v2 import OUE
from frequency.olh import OLH
from frequency.krr import KRR
from collections import Counter

class RPA():
    def __init__(self, protocol : LDPProtocol, beta=0.05):
        self.protocol = protocol
        self.fake_perturbed_values = []
        self.beta = beta

    def generate_fake_perturbed_val(self, file_path):
        df = self.protocol.load_data(file_path)
        if isinstance(self.protocol, OUE):
            return [random.choice([0,1]) for _ in range(len(self.protocol.domain))]
        elif isinstance(self.protocol, KRR):
            return random.choice(self.protocol.domain)
        elif isinstance(self.protocol, OLH):
            random_hash = random.choice(self.protocol.domain)   # randomly select a seed
            random_val = random.choice(self.protocol.domain_dot)
            return dict(hash_func=random_hash, hash_val=random_val)
        else:
            raise ValueError("Unsupported LDP protocol")

    def run_rpa(self, file_path):
        df = self.protocol.load_data(file_path)
        n = df['Word'].count()
        num_fake_users = int(n * self.beta)

        # calculate the original frequencies before RPA
        original_fre = self.protocol.aggregate([self.protocol.perturb(self.protocol.encode(r)) for r in df['Word']])

        # generate fake perturbed values for all fake users
        for _ in range(num_fake_users):
            self.fake_perturbed_values.append(self.generate_fake_perturbed_val(file_path))

        # aggregate original data with fake perturbed values
        combined_perturbed_values = [self.protocol.perturb(self.protocol.encode(r)) for r in df['Word']] + self.fake_perturbed_values
        attack_fre = self.protocol.aggregate(combined_perturbed_values)

        return original_fre, attack_fre

    def save_res(self, original_fre, attacked_fre):
        results = []
        if isinstance(original_fre, list) and isinstance(attacked_fre, list):  # OUE
            gain = [a - b for a, b in zip(original_fre,attacked_fre)]   # frequency gain
            results = list(zip(self.protocol.domain, original_fre, attacked_fre, gain))
        elif isinstance(original_fre, Counter) and isinstance(attacked_fre, Counter): # kRR
            results = [(i, original_fre.get(i,0), attacked_fre.get(i,0), attacked_fre.get(i,0) - original_fre.get(i,0)) for i in self.protocol.domain]
        elif isinstance(original_fre, dict) and isinstance(attacked_fre, dict):     # OLH
            results = [(i, original_fre.get(i,0), attacked_fre.get(i,0), attacked_fre.get(i,0) - original_fre.get(i,0)) for i in self.protocol.domain]

        # convert to dataframe
        df = pd.DataFrame(results, columns=['Word', 'Original Frequency', 'Attacked Frequency', 'Frequency Gain'])

        df_fake_perturbed_vals = pd.DataFrame(self.fake_perturbed_values, columns=['Fake Perturbed Value'])
        df = pd.concat([df, df_fake_perturbed_vals], axis=1)

        # write
        output_file_path = r'D:\LDP\result\frequency gains of RPA for OUE.xlsx'
        df.to_excel(output_file_path, index=False)
        print(f"Results written to {output_file_path}")

if __name__ == "__main__":
    protocol = OUE()
    rpa = RPA(protocol=protocol)
    original_fre, attacked_fre = rpa.run_rpa('D:\LDP\data\synthetic_dataset.xlsx')
    rpa.save_res(original_fre, attacked_fre)