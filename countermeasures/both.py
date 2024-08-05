# -*- coding: utf-8 -*-
# @Time    : 2024-08-03 11:00
# @Author  : sun bo
# @File    : both.py
# @Software: PyCharm

from fake_detect import FakeDetect
from norm import Normalization
from frequency.LDPprotocol import LDPProtocol
from frequency.oue_v2 import OUE
from frequency.olh import OLH

# fake_users_detect + Normalization
class Both():
    def __init__(self, protocol :LDPProtocol):
        self.protocol = protocol
        self.fake_detect = FakeDetect(protocol)
        self.normalization = Normalization()

    def cal_overall_gain(self, perturbed_values, original_fre, target_items, min_support):
        # detect and remove fake users

        if isinstance(self.protocol, OLH):
            binary_vectors = self.fake_detect.craft_binary_vector(perturbed_values)
            frequent_itemsets = self.fake_detect.frequent_itemset_mining(binary_vectors, min_support)
            fake_user_indices = self.fake_detect.detect_fake_users(binary_vectors, frequent_itemsets)
        elif isinstance(self.protocol, OUE):
            frequent_itemsets = self.fake_detect.frequent_itemset_mining(perturbed_values, min_support)
            fake_user_indices = self.fake_detect.detect_fake_users(perturbed_values, frequent_itemsets)
        else:
            raise ValueError("Unsupported LDP Protocol")

        real_perturbed_vals = self.fake_detect.remove_fake_users(perturbed_values, fake_user_indices)

        # aggregate the remaining perturbed values
        fre_after_detect = self.protocol.aggregate(real_perturbed_vals)

        # convert frequencies to dict
        if isinstance(fre_after_detect, list):
            fre_after_detect_dic = dict(zip(self.protocol.domain, fre_after_detect))
        elif isinstance(fre_after_detect, dict):
            fre_after_detect_dic = fre_after_detect
        else:
            raise ValueError("Unsupported LDP protocol")

        # Normalization
        overall_gain = self.normalization.cal_overall_gain(original_fre, fre_after_detect_dic, target_items)
        return overall_gain