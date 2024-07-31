import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math

sns.set(style="darkgrid")

# Relationship between overall gain (G) and proportion of fake users (beta)

def G_RPA(beta, r=1, d = 1024, fT=0.01):
    return beta * (r / d - fT)

def NG_RPA(beta, r=1, d=1024, fT=0.01):
    return (G_RPA(beta) + fT) / fT

def G_RIA(beta, fT=0.01):
    return beta * (1 - fT)


# Normalizied overall gain

def NG_RIA(beta, fT=0.01):
    return (G_RIA(beta) + fT) / fT

def G_MGA(beta, fT=0.01, d=1024, r=1, epsilon=1):
    return beta * (1 - fT) + (beta * (d-r)) / (math.e**epsilon - 1)

def NG_MGA(beta, fT=0.01, d=1024, r=1, epsilon=1):
    return (G_MGA(beta) + fT) / fT

# Relationship between overall gain (G) and the number of target items (r)

def G_RPA_r(r, beta=0.05, d=1024, fT=0.01):
    return beta * (r / d - fT)

def G_RIA_r(r, beta=0.05, fT=0.01):
    return beta * (1- fT)

def G_MGA_r(r, fT=0.01, d=1024, beta=0.05, epsilon=1):
    return beta * (1 - fT) + (beta * (d-r)) / (math.e**epsilon - 1)

# Normalizied overall gain

def NG_RPA_r(r, beta=0.05, d=1024, fT=0.01):
    return (G_RPA_r(r) + fT) / fT

def NG_RIA_r(r, beta=0.05, fT=0.01):
    return (G_RIA_r(r) + fT) /fT

def NG_MGA_r(r, fT=0.01, d=1024, beta=0.05, epsilon=1):
    return (G_MGA_r(r) + fT) / fT

# Relationship between overall gain (G) and the true frequency (fT)

def G_RPA_fT(fT, beta=0.05, d=1024, r=1):
    return beta * (r / d - fT)

def G_RIA_fT(fT, beta=0.05):
    return beta * (1 - fT)

def G_MGA_fT(fT, beta=0.05, d=1024, r=1, epsilon=1):
    return beta * (1 - fT) + (beta * (d-r)) / (math.e**epsilon - 1)

# Normalizied overall gain

def NG_RPA_fT(fT, beta=0.05, d=1024, r=1):
    return (G_RPA_fT(fT) + fT) / fT

def NG_RIA_fT(fT, beta=0.05):
    return (G_RIA_fT(fT) + fT) /fT

def NG_MGA_fT(fT, d=1024, beta=0.05, epsilon=1):
    return (G_MGA_fT(fT) + fT) / fT

# Relationship between overall gain (G) and privacy budget (epsilon)

def G_RPA_ep(fT=0.01, beta=0.05, d=1024, r=1):
    return beta * (r / d - fT)

def G_RIA_ep(fT=0.01, beta=0.05):
    return beta * (1 - fT)

def G_MGA_ep(epsilon, beta=0.05, d=1024, r=1, fT=0.01):
    return beta * (1 - fT) + (beta * (d-r)) / (math.e**epsilon - 1)


# Normalizied overall gain

def NG_RPA_ep(fT=0.01, beta=0.05, d=1024, r=1):
    return (G_RPA_ep() + fT) / fT

def NG_RIA_ep(fT=0.01, beta=0.05):
    return (G_RIA_ep() + fT) /fT

def NG_MGA_ep(epsilon, fT=0.01, d=1024, beta=0.05):
    return (G_MGA_ep(epsilon) + fT) / fT

# Relationship between overall gain (G) and domian size (d)

def G_RPA_d(d, beta=0.05, r=1, fT=0.01):
    return beta * (r / d - fT)

def G_RIA_d(fT=0.01, beta=0.05):
    return beta * (1 - fT)

def G_MGA_d(d, epsilon=1, beta=0.05, r=1, fT=0.01):
    return beta * (1 - fT) + (beta * (d-r)) / (math.e**epsilon - 1)


def NG_RPA_d(d, fT=0.01, beta=0.05, r=1):
    return (G_RPA_d(d) + fT) / fT

def NG_RIA_d(fT=0.01, beta=0.05):
    return (G_RIA_d() + fT) /fT

def NG_MGA_d(d, epsilon=1, fT=0.01, beta=0.05):
    return (G_MGA_d(d) + fT) / fT

# parameters settings and range
beta_values = [1e-3, 5e-3, 1e-2, 5e-2, 1e-1]
r_values = [1, 5, 10, 15, 20]
fT_values = [1e-3, 5e-3, 1e-2, 5e-2, 1e-1]
epsilon_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
d_values = [2**4, 2**5, 2**6, 2**7, 2**8, 2**9, 2**10, 2**11, 2**12]

# Custom vertical labels
yticks = [-10**-2, 0, 10**-2, 10**-1, 10**0, 10**1, 10**2]
yticklabels = [r'$-10^{-2}$', '0', r'$10^{-2}$', r'$10^{-1}$', r'$10^{0}$', r'$10^{1}$', r'$10^{2}$']


#Normalizied y labels
normal_yticks = [0, 10**0, 10**1, 10**2, 10**3, 10**4, 10**5]
normal_yticklabels = [r'$0$', r'$10^{0}$', r'$10^{1}$', r'$10^{2}$', r'$10^{3}$', r'$10^{4}$', r'$10^{5}$']

fig, axes = plt.subplots(2, 5, figsize=(25, 8))

# G vs. beta
axes[0][0].plot(beta_values, [G_RPA(b) for b in beta_values], 'o-', label='RPA')
axes[0][0].plot(beta_values, [G_RIA(b) for b in beta_values], 'x-', label='RIA')
axes[0][0].plot(beta_values, [G_MGA(b) for b in beta_values], 's-', label='MGA')
axes[0][0].set_xscale('log')
axes[0][0].set_yscale('symlog', linthresh = 0.01)
axes[0][0].set_xlabel(r'$\beta$')
axes[0][0].set_ylabel(r'$G$')
axes[0][0].set_yticks(yticks,yticklabels)
axes[0][0].legend()
axes[0][0].grid(True)


# G vs. r
axes[0][1].plot(r_values, [G_RPA_r(r) for r in r_values], 'o-', label='RPA')
axes[0][1].plot(r_values, [G_RIA_r(r) for r in r_values], 'x-', label='RIA')
axes[0][1].plot(r_values, [G_MGA_r(r) for r in r_values], 's-', label='MGA')
axes[0][1].set_yscale('linear')
axes[0][1].set_yscale('symlog', linthresh = 0.01)
axes[0][1].set_xlabel(r'$r$')
axes[0][1].set_ylabel(r'$G$')
axes[0][1].set_yticks(yticks,yticklabels)
axes[0][1].legend()
axes[0][1].grid(True)

# G vs. fT
axes[0][2].plot(fT_values, [G_RPA_fT(fT) for fT in fT_values], 'o-', label='RPA')
axes[0][2].plot(fT_values, [G_RIA_fT(fT) for fT in fT_values], 'x-', label='RIA')
axes[0][2].plot(fT_values, [G_MGA_fT(fT) for fT in fT_values], 's-', label='MGA')
axes[0][2].set_xscale('log')
axes[0][2].set_yscale('symlog', linthresh = 0.01)
axes[0][2].set_xlabel(r'$f_T$')
axes[0][2].set_ylabel(r'$G$')
axes[0][2].set_yticks(yticks,yticklabels)
axes[0][2].legend()
axes[0][2].grid(True)


# G vs. epsilon
axes[0][3].plot(epsilon_values, [G_RPA_ep() for e in epsilon_values], 'o-', label='RPA')
axes[0][3].plot(epsilon_values, [G_RIA_ep() for e in epsilon_values], 'x-', label='RIA')
axes[0][3].plot(epsilon_values, [G_MGA_ep(e) for e in epsilon_values], 's-', label='MGA')
axes[0][3].set_xscale('linear')
axes[0][3].set_yscale('symlog', linthresh = 0.01)
axes[0][3].set_xlabel(r'$\epsilon$')
axes[0][3].set_ylabel(r'$G$')
axes[0][3].set_yticks(yticks,yticklabels)
axes[0][3].legend()
axes[0][3].grid(True)

# G vs. d
axes[0][4].plot(d_values, [G_RPA_d(d) for d in d_values], 'o-', label='RPA')
axes[0][4].plot(d_values, [G_RIA_d() for d in d_values], 'x-', label='RIA')
axes[0][4].plot(d_values, [G_MGA_d(d) for d in d_values], 's-', label='MGA')
axes[0][4].set_xscale('log')
axes[0][4].set_yscale('symlog', linthresh = 0.01)
axes[0][4].set_xlabel(r'$d$')
exponents = np.arange(4, 13)
plt.xticks([2**i for i in exponents], [r'$2^{' + str(i) + '}$' for i in exponents])
axes[0][4].set_ylabel(r'$G$')
axes[0][4].set_yticks(yticks,yticklabels)
axes[0][4].legend()
axes[0][4].grid(True)


# NG vs. beta
axes[1][0].plot(beta_values, [NG_RPA(b) for b in beta_values], 'o-', label='RPA')
axes[1][0].plot(beta_values, [NG_RIA(b) for b in beta_values], 'x-', label='RIA')
axes[1][0].plot(beta_values, [NG_MGA(b) for b in beta_values], 's-', label='MGA')
axes[1][0].set_xscale('log')
axes[1][0].set_yscale('symlog', linthresh = 1)
axes[1][0].set_xlabel(r'$\beta$')
axes[1][0].set_ylabel(r'$Normalized\  G$')
axes[1][0].set_yticks(normal_yticks, normal_yticklabels)
axes[1][0].legend()
axes[1][0].grid(True)



# NG vs. r
axes[1][1].plot(r_values, [NG_RPA_r(r) for r in r_values], 'o-', label='RPA')
axes[1][1].plot(r_values, [NG_RIA_r(r) for r in r_values], 'x-', label='RIA')
axes[1][1].plot(r_values, [NG_MGA_r(r) for r in r_values], 's-', label='MGA')
axes[1][1].set_yscale('linear')
axes[1][1].set_yscale('symlog', linthresh = 1)
axes[1][1].set_xlabel(r'$r$')
axes[1][1].set_ylabel(r'$Normalized\  G$')
axes[1][1].set_yticks(normal_yticks, normal_yticklabels)
axes[1][1].legend()
axes[1][1].grid(True)

# NG vs. fT
axes[1][2].plot(fT_values, [NG_RPA_fT(fT) for fT in fT_values], 'o-', label='RPA')
axes[1][2].plot(fT_values, [NG_RIA_fT(fT) for fT in fT_values], 'x-', label='RIA')
axes[1][2].plot(fT_values, [NG_MGA_fT(fT) for fT in fT_values], 's-', label='MGA')
axes[1][2].set_xscale('log')
axes[1][2].set_yscale('symlog', linthresh = 1)
axes[1][2].set_xlabel(r'$f_T$')
axes[1][2].set_ylabel(r'$Normalized\  G$')
axes[1][2].set_yticks(normal_yticks, normal_yticklabels)
axes[1][2].legend()
axes[1][2].grid(True)


# NG vs. epsilon
axes[1][3].plot(epsilon_values, [NG_RPA_ep() for e in epsilon_values], 'o-', label='RPA')
axes[1][3].plot(epsilon_values, [NG_RIA_ep() for e in epsilon_values], 'x-', label='RIA')
axes[1][3].plot(epsilon_values, [NG_MGA_ep(e) for e in epsilon_values], 's-', label='MGA')
axes[1][3].set_xscale('linear')
axes[1][3].set_yscale('symlog', linthresh = 1)
axes[1][3].set_xlabel(r'$\epsilon$')
axes[1][3].set_ylabel(r'$Normalized\  G$')
axes[1][3].set_yticks(normal_yticks,normal_yticklabels)
axes[1][3].legend()
axes[1][3].grid(True)

# NG vs. d
axes[1][4].plot(d_values, [NG_RPA_d(d) for d in d_values], 'o-', label='RPA')
axes[1][4].plot(d_values, [NG_RIA_d() for d in d_values], 'x-', label='RIA')
axes[1][4].plot(d_values, [NG_MGA_d(d) for d in d_values], 's-', label='MGA')
axes[1][4].set_xscale('log')
axes[1][4].set_yscale('symlog', linthresh = 1)
axes[1][4].set_xlabel(r'$d$')
exponents = np.arange(4, 13)
plt.xticks([2**i for i in exponents], [r'$2^{' + str(i) + '}$' for i in exponents])
axes[1][4].set_ylabel(r'$Normalized\  G$')
axes[1][4].set_yticks(normal_yticks,normal_yticklabels)
axes[1][4].legend()
axes[1][4].grid(True)

fig.suptitle('Impact of different parameters on the overall gains and normalized overall gains (kRR).')

plt.tight_layout()
plt.show()

fig.savefig(r'D:\LDP\result\G and normalized G of kRR111.png')