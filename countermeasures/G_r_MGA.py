# -*- coding: utf-8 -*-
# @Time    : 2024-08-03 10:36
# @Author  : sun bo
# @File    : G_r_MGA.py
# @Software: PyCharm
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from norm import Normalization
from fake_detect import FakeDetect
from fake_detect_OLH import DetectFakeOLH
from frequency.olh import OLH
from attack.mga_v2 import MGA
from frequency.oue_v2 import OUE
from both import Both

sns.set(style="darkgrid")

yticks = [-10**-1, 0, 10**-1,10**0, 10**1]
yticklabels=[r'$-10^{-1}$',r'$0$',r'$10^{-1}$',r'$10^{0}$',r'$10^{1}$']

r_vals = [1,2,3,4,5,6,7,8,9,10]
# protocol = OUE(epsilon=1)
protocol = OLH(epsilon=1)
nor = Normalization()
detect = FakeDetect(protocol)
both = Both(protocol)
beta = 0.05

def run_exp_r(file_path):
    # relation between beta and G for different countmeasures against MGA
    G_no = []       # no defense
    G_norm = []     # normalization
    G_detect = []   # detect fake users
    G_both = []     # nomalization + detect

    for r in r_vals:
        mga = MGA(protocol, r=r, beta=beta)

        _, overall_gain, original_fre_dic, attacked_fre_dic, perturbed_vals = mga.run_mga(file_path)

        print("taget items:", mga.target_items)

        G_no.append(overall_gain)
        G_norm.append(nor.cal_overall_gain(original_fre_dic, attacked_fre_dic, mga.target_items))
        G_detect.append(detect.cal_over_gain(perturbed_vals, beta / 10, original_fre_dic, mga.target_items))     # OLH: min_support = b / 10,    OUE: min_support = b    same as "both"
        G_both.append(both.cal_overall_gain(perturbed_vals, original_fre_dic, mga.target_items, beta / 10))

    return G_no, G_norm, G_detect, G_both

def plot_results(beta_vals, G_no, G_norm, G_detect, G_both):
    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(r_vals, G_no, 'o-', label='No')
    ax.plot(r_vals, G_norm, 'x-', label='Norm')
    ax.plot(r_vals, G_detect, 's-', label='Detect')
    ax.plot(r_vals, G_both, '+-', label='Both')
    ax.set_xscale('linear')
    ax.set_yscale('symlog', linthresh=0.1)
    ax.set_xlabel(r'$r$')
    ax.set_ylabel(r'$G$')
    ax.set_yticks(yticks, yticklabels)
    ax.legend()
    ax.grid(True)


G_no, G_norm, G_detect, G_both = run_exp_r(r'D:\LDP\data\tiny_synthetic_dataset.xlsx')
plot_results(r_vals, G_no, G_norm, G_detect, G_both)
plt.show()