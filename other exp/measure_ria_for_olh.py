# -*- coding: utf-8 -*-
# @Time    : 2024-07-31 20:49
# @Author  : sun bo
# @File    : measure_ria_for_olh.py
# @Software: PyCharm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 对比RIA对OLH的理论和实际对比

def cal_theo_val(beta=0.05, fT=0.01):
    theoretical_G = beta * (1 - fT)
    return theoretical_G


def obtain_prac_val(file_path):
    df = pd.read_excel(file_path)
    practical_G = df['overall gain'][0]
    return practical_G

file = r'/result/frequency gains and overall gain of RIA for OLH.xlsx'
dataset = ['Zipf']
theoretical_value = cal_theo_val()
practical_value = obtain_prac_val(file)

bar_width = 0.4  # 调整柱宽度的一半，使得两个柱状图可以分开显示
index = np.arange(len(dataset))

fig, ax = plt.subplots()

bar1 = ax.bar(index - 0.5 * bar_width, theoretical_value, bar_width, label='Theoretical', hatch='/', edgecolor='black', color='tab:blue')
bar2 = ax.bar(index + 0.5 * bar_width, practical_value, bar_width, label='Practical', hatch='-', edgecolor='black', color='tab:orange')

ax.set_xlabel('')
ax.set_ylabel('G')
ax.set_title('')
ax.set_xticks(index)
ax.set_xticklabels(dataset)

ax.legend()

plt.show()
fig.savefig(r'D:\LDP\other exp\theoretical vs. practical (RIA on OLH).png')