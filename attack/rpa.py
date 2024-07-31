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

class RIA():
    def __init__(self, protocol : LDPProtocol, beta=0.05):
        self.protocol = protocol
        self.fake_perturbed_values = []

    def generate_fake_perturbed_val(self, file_path):
        df = self.protocol.load_data(file_path)

        if isinstance(self.protocol, OUE):
            return [random.choice([0,1]) for _ in range(len(self.domain))]
        elif isinstance(self.protocol, KRR):

