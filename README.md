# Poisoning Attacks and Countermeasures on LDP Protocols

## Introduction

The repository contains *code reproduction* of the paper **[Data Poisoning Attacks to Local Differential Privacy Protocols](https://www.usenix.org/system/files/sec21-cao-xiaoyu.pdf).**

The code implementation includes:

- Three LDP protocols for frequency estimation: **k-ary Randomized Response (kRR)**, **Optimized Unary Encoding (OUE)** and **Optimized Local Hashing (OLH)**.  (paper: [Locally Differentially Private Protocols for Frequency Estimation](https://www.usenix.org/system/files/conference/usenixsecurity17/sec17-wang-tianhao.pdf))
- Three poisoning attacks on LDP: **Random Item Attack (RIA)**, **Random Perturbed-value Attack (RPA)** and **Maximal Gain Attack (MGA)**.
- Theoretical analysis: impact of different parameters on the **overall gains** and **normalized overall gains** (measurement of the effectiveness of the attack).
- Defense mechanisms against poisoning attacks: **normalization**, **fake user detecting** and their combination.
- Comparison of defenses: impact of **$$\beta$$  (proportion of fake users)** and **$r$ (number of target items)** on the different countermeasures against MGA.
- Other experiment: 
  - theoretical and practical overall gains of **RIA for OLH**. 
  - **overall gain vs. number of xxhash** functions sampled in the MGA.

## Dataset

The `data` folder contains synthetic dataset and real-word datasets. Currently the experiments have been performed on the Zipf dataset.

- **Zipf**: The `data/syn_dataset_gen.py` generates a number of values that follow the zipf distribution.
  - `data/synthetic_dataset.xlsx`: $1000000$ users and $1024$ items.
  - `data/tiny_synthetic_dataset.xlsx`: $1000$ users and $128$ items.
- **Fire**: `Fire_Department_and_Emergency_Medical_Services_Dispatched_Calls_for_Service_20240726.csv`. http://bit.ly/336sddL.

## Environment

- Python 3.10
- numpy 2.0.1
- mlxtend 0.23.1
- xxhash 3.4.1

## LDP Protocol

The `frequency` includes three LDP protocols for the task of frequency estimation. `frequency/LDPprotocol.py` defines base class `LDPProtocol`, which contains *load_data*, *encode*, *perturb*, *aggregate* method. Using inheritance and polymorphism, `krr.py`,`oue_v2.py` and `olh.py`  implement the kRR, OUE and OLH protocol, respectively. All these programs runs on the  `synthetic_dataset.xlsx`. Running these three files can obtain the ***count/ frequency estimation result*** in `result`. 

## Theoretical Analysis

