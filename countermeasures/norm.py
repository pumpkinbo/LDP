# -*- coding: utf-8 -*-
# @Time    : 2024-08-01 11:52
# @Author  : sun bo
# @File    : norm.py
# @Software: PyCharm


import pandas as pd
from defense import DefenseMethod
from frequency.LDPprotocol import LDPProtocol

class Normalization():
    def cal_overall_gain(self, original_fre : dict, attacked_fre : dict, target_items : list):
        """
        Apply normalization to the frequencies.
        :param original_fre: Dictionary of original frequencies
        :param attacked_fre:Dictionary of attacked frequencies
        :return: Dictionary of normalized frequencies
        """
        ori_min_fre = min(original_fre.values())
        att_min_fre = min(attacked_fre.values())
        ori_adjusted_fre = {k: v - ori_min_fre for k, v in original_fre.items()}
        att_adjusted_fre = {k: v - att_min_fre for k, v in attacked_fre.items()}
        total_ori_adj = sum(ori_adjusted_fre.values())
        total_att_adj = sum(att_adjusted_fre.values())
        ori_normalized_fre = {k: v / total_ori_adj for k,v in ori_adjusted_fre.items()}
        att_normalized_fre = {k: v / total_att_adj for k,v in att_adjusted_fre.items()}

        overall_gain = 0

        for item in target_items:
            gain = att_normalized_fre.get(item, 0) - ori_normalized_fre.get(item, 0)
            overall_gain += gain
        return overall_gain