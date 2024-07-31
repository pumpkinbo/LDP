# -*- coding: utf-8 -*-
# @Time    : 2024-07-29 15:25
# @Author  : sun bo
# @File    : ria.py
# @Software: PyCharm

import random
from collections import Counter
import numpy as np
import pandas as pd

from frequency.LDPprotocol import LDPProtocol
from frequency.oue_v2 import OUE
from frequency.krr import KRR
from frequency.olh import OLH

class RIA():
    def __init__(self, protocol : LDPProtocol, r=1, beta=0.05):
        """
        Initialize RIA
        :param protocol: Type of LDP protocol used
        :param r: number of target items
        :param beta: Proportion of fake users
        """
        self.r = r
        self.protocol = protocol
        self.beta = beta
        self.target_items = []  # target items selected by the attacker

    def select_target_items(self):
        self.target_items = random.sample(list(self.protocol.domain), self.r)

    def generate_fake_users(self, file_path):
        fake_items = []
        df = self.protocol.load_data(file_path)
        n = df['Word'].count()
        num_fake_users = int(n * self.beta)  # number of fake users
        for i in range(num_fake_users):
            target_item = random.choice(self.target_items)
            fake_items.append(target_item)
        return fake_items


    def cal_original_fre(self, file_path):
        """
        calculate the estimated frequency of all items before attack
        :param file_path: path of dataset
        :return: dictionary, key: Unique item   value: Estimated frequency
        """
        df = self.protocol.load_data(file_path)
        # performe LDP before RIA
        original_fre = self.protocol.aggregate([self.protocol.perturb(self.protocol.encode(r)) for r in df['Word']])

        # different LDP returns different types. OUE: list  OLH: dict   kRR: Counter
        if isinstance(original_fre, list):
            original_fre_dict = dict(zip(self.protocol.domain, original_fre))
        elif isinstance(original_fre, dict):
            original_fre_dict = original_fre
        elif isinstance(original_fre, Counter):
            original_fre_dict = dict(original_fre)
        else:
            raise TypeError("Unsupported return type from aggregate function")
        return original_fre_dict

    def cal_attacked_fre(self, file_path):
        """
        calculate the estimated frequency after the RIA attack
        :param file_path: path of original dataset
        :return: dictionary, key: Unique item   value: Estimated frequency
        """
        df = self.protocol.load_data(file_path)
        self.select_target_items()
        fake_data = self.generate_fake_users(file_path)
        combined_data = list(df['Word']) + fake_data
        attacked_fre = self.protocol.aggregate([self.protocol.perturb(self.protocol.encode(r)) for r in combined_data])
        if isinstance(attacked_fre, list):
            attacked_fre_dict = dict(zip(self.protocol.domain, attacked_fre))
        elif isinstance(attacked_fre, dict):
            attacked_fre_dict = attacked_fre
        elif isinstance(attacked_fre, Counter):
            attacked_fre_dict = dict(attacked_fre)
        else:
            raise TypeError("Unsupported return type from aggregate function")
        return attacked_fre_dict

    def run_ria(self, file_path):
        original_fre_dict = self.cal_original_fre(file_path)
        attacked_fre_dict = self.cal_attacked_fre(file_path)

        # calculate frequency gains and overall gain
        frequency_gains = {}
        overall_gain = 0
        for item in self.target_items:
            gain = attacked_fre_dict.get(item, 0) - original_fre_dict.get(item, 0)
            frequency_gains[item] = gain
            overall_gain += gain
        return frequency_gains, overall_gain

if __name__ == "__main__":

    # protocol = OUE()
    protocol = OLH()
    # protocol = KRR()

    ria = RIA(protocol=protocol)
    frequency_gains, overall_gain = ria.run_ria('D:\LDP\data\synthetic_dataset.xlsx')

    output_file_path = r'D:\LDP\result\frequency gains and overall gain of RIA for OLH.xlsx'
    df_gains = pd.DataFrame(list(frequency_gains.items()), columns=['target item', 'frequency gain'])
    df_overall = pd.DataFrame({'overall gain': [overall_gain]})
    df_combined = pd.concat([df_gains, df_overall], axis=1)
    df_combined.to_excel(output_file_path, index=False)