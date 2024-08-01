# -*- coding: utf-8 -*-
# @Time    : 2024-07-29 20:43
# @Author  : sun bo
# @File    : mga.py
# @Software: PyCharm
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

NUM_OF_HASH_FUNC = 100

class MGA():
    def __init__(self, protocol : LDPProtocol, r=5, beta=0.05):
        self.protocol = protocol
        self.beta = beta
        self.r = r      # number of target items
        self.target_items = []

    def select_target_items(self):
        self.target_items = random.sample(list(self.protocol.domain), self.r)

    def craft_perturbed_value(self, file_path):
        """
        craft perturbed value for a fake user according to specific LDP protocol
        :param file_path: dataset
        :return: a perturbed_value, an item, a binary vector or (hash_func, hash_val)
        """
        df = self.protocol.load_data(file_path)
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
            # best_hash = None
            max_hash_count = 0
            best_perturbed_value = None
            for h in range(NUM_OF_HASH_FUNC):   # seed represents the hash function
                hash_vals = [xxhash.xxh32(str(item), seed=h).intdigest() % self.protocol.d_dot for item in self.target_items]
                most_common_hash_value = max(hash_vals, key=hash_vals.count)
                count = hash_vals.count(most_common_hash_value)
                if count > max_hash_count:
                    max_hash_count = count
                    best_perturbed_value = dict(hash_func=h, hash_val=most_common_hash_value)
            return best_perturbed_value

        else:
            raise ValueError("Unsupported LDP protocol")


    def generate_fake_users(self, file_path):
        fake_perturbed_values = []
        df = self.protocol.load_data(file_path)
        n = df['Word'].count()
        num_fake_users = int(n * self.beta)     # number of fake users
        for _ in range(num_fake_users):
            fake_perturbed_values.append(self.craft_perturbed_value(file_path))
        return fake_perturbed_values


    def cal_origianl_fre(self, file_path):
        # calculate estimated frequency of target items before MGA
        df = self.protocol.load_data(file_path)
        original_fre = self.protocol.aggregate([self.protocol.perturb(self.protocol.encode(r)) for r in df['Word']])
        return original_fre

    def cal_attacked_fre(self, file_path):
        # calculate estimated frequency of target items after MGA
        df  = self.protocol.load_data(file_path)
        self.select_target_items()
        fake_perturbed_values = self.generate_fake_users(file_path)
        combined_perturbed_vals = [self.protocol.perturb(self.protocol.encode(r)) for r in df['Word']] + fake_perturbed_values
        attacked_fre = self.protocol.aggregate(combined_perturbed_vals)
        return attacked_fre


    def run_mga(self, file_path):
        orinigal_fre = self.cal_origianl_fre(file_path)
        attacked_fre = self.cal_attacked_fre(file_path)

        orinigal_fre_dic = {}
        attacked_fre_dic = {}
        frequency_gains = {}
        overall_gain = 0

        # different LDP protocol's aggregate function returns different data type
        if isinstance(orinigal_fre, list) and isinstance(attacked_fre, list):   # OUE
            orinigal_fre_dic = dict(zip(self.protocol.domain, orinigal_fre))
            attacked_fre_dic = dict(zip(self.protocol.domain, attacked_fre))
        elif isinstance(orinigal_fre, Counter) and isinstance(attacked_fre, Counter):     # KRR
            orinigal_fre_dic = orinigal_fre
            attacked_fre_dic = attacked_fre
        elif isinstance(orinigal_fre, dict) and isinstance(attacked_fre, dict):     # OLH
            orinigal_fre_dic = orinigal_fre
            attacked_fre_dic = attacked_fre

        # calculate frequency gains and overall gain
        for item in self.target_items:
            gain = attacked_fre_dic.get(item, 0) - orinigal_fre_dic.get(item, 0)
            frequency_gains[item] = gain
            overall_gain += gain

        return frequency_gains, overall_gain

if __name__ == "__main__":
    protocol = OLH(epsilon=1)
    # protocol = KRR()
    # protocol = OUE()

    mga = MGA(protocol=protocol)
    frequency_gains, overall_gain = mga.run_mga('D:\LDP\data\small_synthetic_dataset.xlsx')

    output_file_path = r'D:\LDP\result\frequency gains and overall gain of MGA for OLH_small dataset).xlsx'
    df_gains = pd.DataFrame(list(frequency_gains.items()), columns=['target item', 'frequency gain'])
    df_overall = pd.DataFrame({'overall gain': [overall_gain]})
    df_combined = pd.concat([df_gains, df_overall], axis=1)
    df_combined.to_excel(output_file_path, index=False)