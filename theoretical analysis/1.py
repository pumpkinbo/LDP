# import matplotlib.pyplot as plt
# import numpy as np
#
#
# yticks = [0, 10**-2, 10**-1,10**0, 10**1]
# # yticks = np.linspace(min(yticks), max(yticks), 5)
# yticklabels=[r'$0$',r'$10^{-2}$',r'$10^{-1}$',r'$10^{0}$',r'$10^{1}$']
# def plot_results(beta_vals, G_no, G_norm, G_detect,yticks=yticks,yticklabels=yticklabels):
#     fig, ax = plt.subplots(figsize=(8,6))
#     ax.plot(beta_vals, G_no, 'o-', label='No')
#     ax.plot(beta_vals, G_norm, 'x-', label='Norm')
#     ax.plot(beta_vals, G_detect, 's-', label='Detect')
#     ax.set_xscale('log')
#     ax.set_yscale('symlog', linthresh=0.01)
#     ax.set_xlabel(r'$\beta$')
#     ax.set_ylabel(r'$G$')
#     ax.set_yticks(yticks, yticklabels)
#     ax.legend()
#     ax.grid(True)
#
# beta_vals = [1e-3, 5e-3, 1e-2, 5e-2, 1e-1]
# G_no=[2.6, 0.2, 0.4, 1.5, 6]
# G_nor=[0.03, 0.09, 0.2, 0.7, 0.9]
# G_detect=[0.06, 1e-14, 2e-17, 7e-17, 2e-16]
#
#
#
# plot_results(beta_vals, G_no, G_nor, G_detect)
# plt.show()

from mlxtend.frequent_patterns import fpgrowth
import pandas as pd
from pyfpgrowth import find_frequent_patterns
p = [
    [1,0,0,1,1,0,1],
    [1,0,1,1,0,1,1],
    [1,0,1,0,1,0,1],
    [1,0,0,0,0,0,1]
]
df = pd.DataFrame(p)

# fp = fpgrowth(df,1, use_colnames=True)
fp = find_frequent_patterns(p, 4)

# fp['itemsets'] = fp['itemsets'].apply(lambda x: {i+1 for i in x})
print(fp)
# print(5000/95)
# print(52/1052)
# print(53/1053)

print(1000/9)
print(111/1111)
print(112/1112)
# max_length = fp['itemsets'].apply(len).max()
#
# # Filter itemsets with the maximum length
# longest_itemsets = fp[fp['itemsets'].apply(len) == max_length]
#
# print(longest_itemsets)

# z = len(itemset)
# support_count = fp.loc[fp['itemsets'] == itemset, 'support_count'].values[0]
# print(max_length_itemset)
# print(z,support_count)

from scipy.special import betainc
def cal_threshold( q, z, total_user, p):
    # calclate the threshold tau_z
    left = 0
    right = total_user + 1
    epsilon = 1  # 误差容限
    while left <= right:
        mid = (left + right) / 2
        value = betainc(q ** (z - 1), mid, total_user - mid + 1)
        if abs(value - p) < epsilon:
            return mid
        if value < p:
            left = mid + 1
        else:
            right = mid - 1
    return -1

q = 0.5
z = 2
p = 0.7
toto = 15
minx = cal_threshold(q,z,toto,p)
print(minx)
[1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0]
[1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0]
[1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0]