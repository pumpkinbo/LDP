# -*- coding: utf-8 -*-
# @Author  : sun bo
# @File    : oue.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import math

dataframe = pd.read_excel('D:\LDP\data\synthetic_dataset.xlsx')
domain = dataframe['Word'].dropna().unique()
domain = np.sort(domain)
print(domain)

def Encode(raw_item):
    encoded_value = [1 if d == raw_item else 0 for d in domain]
    return encoded_value

def Perturb(encoded_value):
    perturbed_value = [Perturb_bit(b) for b in encoded_value]
    return perturbed_value

def Perturb_bit(bit):
    epsilon = 5
    p = 0.5
    q = 1 / (math.exp(epsilon) + 1)
    sample = np.random.random()

    if bit == 1:
        if sample <= p:
            return 1
        else:
            return 0
    elif bit == 0:
        if sample <= q:
            return 1
        else:
            return 0

def Aggregate(perturbed_values):
    epsilon = 5
    p = 0.5
    q = 1 / (math.exp(epsilon) + 1)

    sums = np.sum(perturbed_values,axis = 0)
    n = len(perturbed_values)

    counts = [(sum -  n*q) / (p - q) for sum in sums]
    return counts

perturbed_values = [Perturb(Encode(r)) for r in dataframe['Word']]

counts = Aggregate(perturbed_values)
item_counts = list(zip(domain, counts))

for ic in item_counts:
    print(ic)