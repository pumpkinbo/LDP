# -*- coding: utf-8 -*-
# @Time    : 2024-08-01 11:49
# @Author  : sun bo
# @File    : defense.py
# @Software: PyCharm
import pandas as pd
from abc import ABC, abstractmethod
from collections import Counter
from frequency.LDPprotocol import LDPProtocol

class DefenseMethod(ABC):
    @abstractmethod
    def apply_defense(self, protocol : LDPProtocol ,original_fre, attacked_fre):
        pass
