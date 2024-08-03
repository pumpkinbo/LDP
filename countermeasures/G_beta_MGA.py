# -*- coding: utf-8 -*-
# @Time    : 2024-08-02 9:37
# @Author  : sun bo
# @File    : G_beta_MGA.py
# @Software: PyCharm

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from norm import Normalization
from fake_detect import FakeDetect
from both import Both
from attack.mga_v2 import MGA
from frequency.oue_v2 import OUE

sns.set(style="darkgrid")

yticks = [0, 10**-2, 10**-1,10**0, 10**1]
yticklabels=[r'$0$',r'$10^{-2}$',r'$10^{-1}$',r'$10^{0}$',r'$10^{1}$']

beta_vals = [1e-3, 5e-3, 1e-2, 5e-2, 1e-1]
protocol = OUE(epsilon=1)
nor = Normalization()
detect = FakeDetect(protocol)
both = Both(protocol)

def run_exp_beta(file_path):
    # relation between beta and G for different countmeasures against MGA
    G_no = []       # no defense
    G_norm = []     # normalization
    G_detect = []   # detect fake users
    G_both = []     # nomalization + detect

    for b in beta_vals:
        mga = MGA(protocol, r=10, beta=b)

        _, overall_gain, original_fre_dic, attacked_fre_dic, perturbed_vals = mga.run_mga(file_path)

        print("taget items:", mga.target_items)

        G_no.append(overall_gain)
        G_norm.append(nor.cal_overall_gain(original_fre_dic, attacked_fre_dic, mga.target_items))
        G_detect.append(detect.cal_over_gain(perturbed_vals, b, original_fre_dic, mga.target_items))
        G_both.append(both.cal_overall_gain(perturbed_vals, original_fre_dic, mga.target_items, b))

    return G_no, G_norm, G_detect, G_both

def plot_results(beta_vals, G_no, G_norm, G_detect, G_both):
    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(beta_vals, G_no, 'o-', label='No')
    ax.plot(beta_vals, G_norm, 'x-', label='Norm')
    ax.plot(beta_vals, G_detect, 's-', label='Detect')
    ax.plot(beta_vals, G_both , '+-', label='Both')
    ax.set_xscale('log')
    ax.set_yscale('symlog', linthresh=0.01)
    ax.set_xlabel(r'$\beta$')
    ax.set_ylabel(r'$G$')
    ax.set_yticks(yticks, yticklabels)
    ax.legend()
    ax.grid(True)


G_no, G_norm, G_detect, G_both = run_exp_beta(r'D:\LDP\data\tiny_synthetic_dataset.xlsx')
plot_results(beta_vals, G_no, G_norm, G_detect, G_both)
plt.show()