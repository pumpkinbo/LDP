# -*- coding: utf-8 -*-
# @Time    : 2024-07-30 17:52
# @Author  : sun bo
# @File    : rpa.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import math
import random
from frequency.LDPprotocol import LDPProtocol
from frequency.oue_v2 import OUE
from frequency.olh import OLH
from frequency.krr import KRR
from collections import Counter
from Attack import Attack

class RPA(Attack):
    def __init__(self, protocol : LDPProtocol, r=10, beta=0.05):
        super().__init__(protocol, r, beta)
    
    def generate_fake_perturbed_val(self):
        if isinstance(self.protocol, OUE):
            return [random.choice([0,1]) for _ in range(len(self.protocol.domain))]
        elif isinstance(self.protocol, KRR):
            return random.choice(self.protocol.domain)
        elif isinstance(self.protocol, OLH):
            random_hash = random.randint(1, self.protocol.hash_count)   # randomly select a seed
            random_val = random.choice(self.protocol.domain_dot)
            return dict(hash_func=random_hash, hash_val=random_val)
        else:
            raise ValueError("Unsupported LDP protocol")

    def generate_fake_users(self, num_fake_users):
        fake_perturbed_values = []
        for _ in range(num_fake_users):
            fake_perturbed_values.append(self.generate_fake_perturbed_val())
        return fake_perturbed_values

    def run_rpa(self, file_path):
        df = self.protocol.load_data(file_path)
        n = df['Word'].count()

        genuine_ueser_perturbed_values = [self.protocol.perturb(self.protocol.encode(r)) for r in df['Word']]
        self.select_target_items()
        original_fre = self.cal_frequencies(genuine_ueser_perturbed_values)

        num_fake_users = math.ceil(n * (self.beta / (1 - self.beta)))
        fake_perturbed_values = self.generate_fake_users(num_fake_users)

        combined_perturbed_values = genuine_ueser_perturbed_values + fake_perturbed_values
        attacked_fre = self.cal_frequencies(combined_perturbed_values)

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

        return overall_gain, original_fre_dic, attacked_fre_dic


if __name__ == "__main__":
    # protocol = OUE(epsilon=1)
    # protocol = KRR(epsilon=1)
    protocol = OLH(epsilon=1)
    rpa = RPA(protocol=protocol)
    overall_gain, _, _ = rpa.run_rpa('D:\LDP\data\small_synthetic_dataset.xlsx')
    print(overall_gain)