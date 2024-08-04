# -*- coding: utf-8 -*-
# @Time    : 2024-08-04 16:41
# @Author  : sun bo
# @File    : Attack.py
# @Software: PyCharm
import random

from frequency.LDPprotocol import LDPProtocol

class Attack():

    def __init__(self, protocol : LDPProtocol, r=10, beta=0.05):
        self.protocol = protocol
        self.r = r  # number of target items
        self.beta = beta
        self.target_items = []

    def select_target_items(self):
        self.target_items = random.sample(list(self.protocol.domain), self.r)

    def cal_frequencies(self, perturbed_values):
        return self.protocol.aggregate(perturbed_values)

    def generate_fake_users(self, num_fake_users):
        pass