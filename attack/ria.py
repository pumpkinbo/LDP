# -*- coding: utf-8 -*-
# @Time    : 2024-07-29 15:25
# @Author  : sun bo
# @File    : ria.py
# @Software: PyCharm

import random
from collections import Counter
import numpy as np
import pandas as pd
import math
from frequency.LDPprotocol import LDPProtocol
from frequency.oue_v2 import OUE
from frequency.krr import KRR
from frequency.olh import OLH
from Attack import Attack

class RIA(Attack):
    def __init__(self, protocol : LDPProtocol, r=10, beta=0.05):
        """
        Initialize RIA
        :param protocol: Type of LDP protocol used
        :param r: number of target items
        :param beta: Proportion of fake users
        """
        super().__init__(protocol, r, beta)

    def generate_fake_users(self, num_fake_users):
        fake_items = []
        for _ in range(num_fake_users):
            target_item = random.choice(self.target_items)
            fake_items.append(target_item)
        return fake_items

    def run_ria(self, file_path):
        df = self.protocol.load_data(file_path)
        n = df['Word'].count()

        genuine_user_perturbed_values = [self.protocol.perturb(self.protocol.encode(r)) for r in df['Word']]
        self.select_target_items()
        original_fre = self.cal_frequencies(genuine_user_perturbed_values)

        num_fake_users = math.ceil(n * (self.beta / (1 - self.beta)))
        fake_items = self.generate_fake_users(num_fake_users)
        combined_items = list(df['Word']) + fake_items

        attacked_fre = self.cal_frequencies([self.protocol.perturb(self.protocol.encode(r)) for r in combined_items])

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
    protocol = OLH(epsilon=1)
    # protocol = KRR(epsilon=1)

    ria = RIA(protocol=protocol)
    overall_gain, _, _ = ria.run_ria(r'D:\LDP\data\small_synthetic_dataset.xlsx')

    print(overall_gain)
    # output_file_path = r'D:\LDP\result\frequency gains and overall gain of RIA for OLH.xlsx'
    # df_gains = pd.DataFrame(list(frequency_gains.items()), columns=['target item', 'frequency gain'])
    # df_overall = pd.DataFrame({'overall gain': [overall_gain]})
    # df_combined = pd.concat([df_gains, df_overall], axis=1)
    # df_combined.to_excel(output_file_path, index=False)