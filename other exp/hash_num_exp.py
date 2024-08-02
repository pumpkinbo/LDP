# -*- coding: utf-8 -*-
# @Time    : 2024-08-01 9:50
# @Author  : sun bo
# @File    : hash_num_exp.py
# @Software: PyCharm
import math

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from attack.mga_v2 import MGA
from frequency.olh import OLH
import seaborn as sns

sns.set(style="darkgrid")

def cal_theo_val(beta=0.05, r=5, fT=0.01, epsilon=1):
    return beta * (2 * r - fT) + (2 * beta * r) / (math.e**epsilon - 1)

def run_exp(file_path):
    hash_func_counts = [1,10,100,200,400]
    overall_gains = []

    for i in hash_func_counts:
        protocol = OLH(epsilon=1)
        mga = MGA(protocol=protocol, num_hash_funcs=i)
        _, overall_gain, _, _ = mga.run_mga(file_path)
        overall_gains.append(overall_gain)

    return hash_func_counts, overall_gains

def plot_results(hash_func_counts, overall_gains, theoretical_gains):
    plt.figure(figsize=(8,6))
    plt.plot(hash_func_counts, theoretical_gains, 'o-', label='Theoretical', linewidth=2, markersize=8)
    plt.plot(hash_func_counts, overall_gains, 'x--', label='Practical', linewidth=2, markersize=8)
    # plt.xscale('log')
    plt.xlabel('Number of sampled hash functions')
    plt.ylabel('G')
    plt.ylim(0,1)
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.title('Impact of Number of Hash Functions on Overall Gain in MGA')
    plt.show()

if __name__ == "__main__":
    file_path = r'D:\LDP\data\small_synthetic_dataset.xlsx'

    hash_func_counts, overall_gains = run_exp(file_path)
    theoretical_gains = [cal_theo_val() for _ in range(len(hash_func_counts))]
    plot_results(hash_func_counts, overall_gains, theoretical_gains)