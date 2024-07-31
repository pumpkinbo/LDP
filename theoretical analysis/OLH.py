
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math

sns.set(style="darkgrid")

# Overall gain (G) and normalized gain (NG) functions
def G(beta, fT, d=1024, r=1, epsilon=1, attack_type='RPA'):
    if attack_type == 'RPA':
        return 0 - beta * fT
    elif attack_type == 'RIA':
        return beta * (1 - fT)
    elif attack_type == 'MGA':
        return beta * (2*r - fT) + (2 * beta * r) / (math.e**epsilon - 1)

def NG(beta, fT, d=1024, r=1, epsilon=1, attack_type='RPA'):
    return (G(beta, fT, d, r, epsilon, attack_type) + fT) / fT


# Parameters and ranges
beta_values = [1e-3, 5e-3, 1e-2, 5e-2, 1e-1]
r_values = [1, 5, 10, 15, 20]
fT_values = [1e-3, 5e-3, 1e-2, 5e-2, 1e-1]
epsilon_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
d_values = [2**4, 2**5, 2**6, 2**7, 2**8, 2**9, 2**10, 2**11, 2**12]

yticks = [-10**-2, 0, 10**-2, 10**-1, 10**0]
yticklabels = [r'$-10^{-2}$', r'$0$', r'$10^{-2}$', r'$10^{-1}$', r'$10^{0}$']
normal_yticks = [10**0, 10**1, 10**2]
normal_yticklabels = [r'$10^{0}$', r'$10^{1}$', r'$10^{2}$']

# Plot settings
fig, axes = plt.subplots(2, 5, figsize=(25, 8))


# Function to generate subplots
def plot_subplot(ax, x_values, y_values, x_label, y_label, attack_types, x_scale='linear', y_scale='symlog', y_ticks=yticks, y_ticklabels=yticklabels):
    markers = ['o-', 'x-', 's-']
    for i, attack_type in enumerate(attack_types):
        ax.plot(x_values, y_values[i], markers[i], label=attack_type)
    ax.set_xscale(x_scale)
    ax.set_yscale(y_scale, linthresh=0.01 if 'Normalized' not in y_label else 10)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_yticks(y_ticks, y_ticklabels)
    ax.legend()
    ax.grid(True)


# Overall gain (G) plots
G_values_beta = [
    [G(b, 0.01, attack_type=att) for b in beta_values] for att in ['RPA', 'RIA', 'MGA']
]
plot_subplot(axes[0][0], beta_values, G_values_beta, r'$\beta$', r'$G$', ['RPA', 'RIA', 'MGA'], x_scale='log')

G_values_r = [
    [G(0.05, 0.01, r=r, attack_type=att) for r in r_values] for att in ['RPA', 'RIA', 'MGA']
]
plot_subplot(axes[0][1], r_values, G_values_r, r'$r$', r'$G$', ['RPA', 'RIA', 'MGA'])

G_values_fT = [
    [G(0.05, fT, attack_type=att) for fT in fT_values] for att in ['RPA', 'RIA', 'MGA']
]
plot_subplot(axes[0][2], fT_values, G_values_fT, r'$f_T$', r'$G$', ['RPA', 'RIA', 'MGA'], x_scale='log')

G_values_ep = [
    [G(0.05, 0.01, epsilon=e, attack_type=att) for e in epsilon_values] for att in ['RPA', 'RIA', 'MGA']
]
plot_subplot(axes[0][3], epsilon_values, G_values_ep, r'$\epsilon$', r'$G$', ['RPA', 'RIA', 'MGA'])

G_values_d = [
    [G(0.05, 0.01, d=d, attack_type=att) for d in d_values] for att in ['RPA', 'RIA', 'MGA']
]
plot_subplot(axes[0][4], d_values, G_values_d, r'$d$', r'$G$', ['RPA', 'RIA', 'MGA'], x_scale='log')


# Normalized gain (NG) plots
NG_values_beta = [
    [NG(b, 0.01, attack_type=att) for b in beta_values] for att in ['RPA', 'RIA', 'MGA']
]
plot_subplot(axes[1][0], beta_values, NG_values_beta, r'$\beta$', r'$Normalized\ G$', ['RPA', 'RIA', 'MGA'], x_scale='log', y_ticks=normal_yticks, y_ticklabels=normal_yticklabels)

NG_values_r = [
    [NG(0.05, 0.01, r=r, attack_type=att) for r in r_values] for att in ['RPA', 'RIA', 'MGA']
]
plot_subplot(axes[1][1], r_values, NG_values_r, r'$r$', r'$Normalized\ G$', ['RPA', 'RIA', 'MGA'], y_ticks=normal_yticks, y_ticklabels=normal_yticklabels)

NG_values_fT = [
    [NG(0.05, fT, attack_type=att) for fT in fT_values] for att in ['RPA', 'RIA', 'MGA']
]
plot_subplot(axes[1][2], fT_values, NG_values_fT, r'$f_T$', r'$Normalized\ G$', ['RPA', 'RIA', 'MGA'], x_scale='log', y_ticks=normal_yticks, y_ticklabels=normal_yticklabels)

NG_values_ep = [
    [NG(0.05, 0.01, epsilon=e, attack_type=att) for e in epsilon_values] for att in ['RPA', 'RIA', 'MGA']
]
plot_subplot(axes[1][3], epsilon_values, NG_values_ep, r'$\epsilon$', r'$Normalized\ G$', ['RPA', 'RIA', 'MGA'], y_ticks=normal_yticks, y_ticklabels=normal_yticklabels)

NG_values_d = [
    [NG(0.05, 0.01, d=d, attack_type=att) for d in d_values] for att in ['RPA', 'RIA', 'MGA']
]
plot_subplot(axes[1][4], d_values, NG_values_d, r'$d$', r'$Normalized\ G$', ['RPA', 'RIA', 'MGA'], x_scale='log', y_ticks=normal_yticks, y_ticklabels=normal_yticklabels)

fig.suptitle('Impact of different parameters on the overall gains and normalized overall gains (OLH).')

plt.tight_layout()
plt.show()

fig.savefig(r'D:\LDP\result\G and Normalized G of OLH.png')
