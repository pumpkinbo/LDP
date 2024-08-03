# -*- coding: utf-8 -*-
# @Time    : 2024-08-01 13:46
# @Author  : sun bo
# @File    : fake_detect.py
# @Software: PyCharm
import math
from collections import defaultdict, Counter
from itertools import combinations

import pandas as pd

from frequency.LDPprotocol import LDPProtocol
from defense import DefenseMethod
from mlxtend.frequent_patterns import fpgrowth

# 探测异常的扰动值（假用户），将异常的扰动值剔除后执行aggregate

class FakeDetect():
    def __init__(self, protocol :LDPProtocol):
        self.protocol = protocol

    def frequent_itemset_mining(self, perturbed_values, min_support):
        """
        Find frequent itemsets that are all 1's in at least a certain number of users
        :param perturbed_values: list of perturbed binary vectors (OUE)
        :param min_support: 0 < min_support < 1
        :return: dataframe with frequent itemsets and their support count
        """
        df = pd.DataFrame(perturbed_values)

        frequent_itemsets = fpgrowth(df, min_support=min_support, use_colnames=True)
        frequent_itemsets['support_count'] = frequent_itemsets['support'] * len(perturbed_values)

        # index should begin from 1
        # frequent_itemsets['itemsets'] = frequent_itemsets['itemsets'].apply(lambda x: {i+1 for i in x})

        # return frequent_itemsets
        # select the longest itemsets (avoid unnecessary computation)
        max_length = frequent_itemsets['itemsets'].apply(len).max()
        return frequent_itemsets[frequent_itemsets['itemsets'].apply(len) == max_length]

    def detect_fake_users(self, perturbed_values, frequent_itemsets):
        """
        Detect fake users by identifuing abnormal itemsets
        :param perturbed_values: perturbed binary vectors (OUE)
        :param frequent_itemsets:
        :return: list of indices of detected fake perturbed values (fake users)
        """
        num_users = len(perturbed_values)   # number of all users (geniue and fake users)
        fake_user_indices = set()

        for _, row in frequent_itemsets.iterrows():
            itemset = row['itemsets']
            z = len(itemset)
            support_count = row['support_count']
            tau_z = math.ceil(num_users * self.protocol.p * (self.protocol.q**(z-1)))
            if support_count >= tau_z:
                for idx, vector in enumerate(perturbed_values):
                    if all(vector[i] == 1 for i in itemset):
                        fake_user_indices.add(idx)

        return fake_user_indices


    def remove_fake_users(self, data, fake_user_indices):
        """
        remove fake users from the dataset
        :param data: dataset before remove
        :param fake_user_indices: list of indices of detected fake users
        :return: data after removing fake users
        """
        real_data = [data[i] for i in range(len(data)) if i not in fake_user_indices]
        return real_data

    def cal_over_gain(self, perturbed_values, minsupport, original_fre : dict, target_items : list):
        overall_gain = 0
        frequent_itemsets = self.frequent_itemset_mining(perturbed_values, minsupport)
        fake_user_indices = self.detect_fake_users(perturbed_values, frequent_itemsets)

        real_perturbed_vals = self.remove_fake_users(perturbed_values, fake_user_indices)

        fre_after_detect = self.protocol.aggregate(real_perturbed_vals)

        if isinstance(fre_after_detect, list):
            fre_after_detect_dic = dict(zip(self.protocol.domain, fre_after_detect))
        elif isinstance(fre_after_detect, dict):
            fre_after_detect_dic = fre_after_detect
        else:
            raise ValueError("Unsupport LDP protocol")

        for item in target_items:
            gain = fre_after_detect_dic.get(item,0) - original_fre.get(item, 0)
            overall_gain += gain

        return overall_gain