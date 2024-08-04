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
  - `data/synthetic_dataset.xlsx`: 1000000 users and 1024 items.
  - `small_synthetic_dataset.xlsx`: 100000 users and 128 items.
  - `data/tiny_synthetic_dataset.xlsx`: 1000 users and 50 items.
- **Fire**: `Fire_Department_and_Emergency_Medical_Services_Dispatched_Calls_for_Service_20240726.csv`. http://bit.ly/336sddL.

## Environment

- Python 3.10
- numpy 2.0.1
- mlxtend 0.23.1
- xxhash 3.4.1

## LDP Protocol

The `frequency` includes three LDP protocols for the task of frequency estimation. `frequency/LDPprotocol.py` defines base class `LDPProtocol`, which contains *load_data*, *encode*, *perturb*, *aggregate* method. Using inheritance and polymorphism, `krr.py`,`oue_v2.py` and `olh.py`  implement the kRR, OUE and OLH protocol, respectively. All these programs runs on the  `synthetic_dataset.xlsx`. Running these three files can obtain the ***count/ frequency estimation result*** in `result`. 

## Attacks

The `attack`folder contains three poisoning attacks on LDP protocols: `rpa.py`, `ria.py` and `mga_v2.py` (`mga_v2.py` is the refactor of `mga.py`). Running these programs on `small_synthetic_dataset.xlsx` ($\beta=0.05, r=10, \epsilon=1$), we can obtain the overall gain ($G$) of different attacks for different LDP protocols. (The results were averaged over 8 experiments.)

Results:

|      |  kRR   |  OUE   |  OLH   |
| :--: | :----: | :----: | :----: |
| RIA  | 0.0418 | 0.0528 | 0.0599 |
| RPA  |  6e-5  | 0.4946 |  9e-3  |
| MGA  | 3.4813 | 1.5761 | 1.0277 |



## Theoretical Analysis

![image-20240804100936509](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20240804100936509.png)

According to the above table, files in `theoretical analysis` show the impact of different parameters on the overall gains and normalized overall gains.

|  parameters  |         significance         |
| :----------: | :--------------------------: |
|  $$\beta$$   |   Proportion of fake users   |
|    $r$     |  The number of target items  |
|   $$f_T$$    | Target items' true frequency |
| $$\epsilon$$ |        Privacy budget        |
|    $$d$$     |        Size of domain        |

Results:

- kRR:

![](https://github.com/pumpkinbo/LDP/blob/master/result/G%20and%20normalized%20G%20of%20kRR.png)

- OUE:

![](https://github.com/pumpkinbo/LDP/blob/master/result/G%20and%20Normalized%20G%20of%20OUE.png)

- OLH:

![](https://github.com/pumpkinbo/LDP/blob/master/result/G%20and%20Normalized%20G%20of%20OLH.png)

## Defense

The `fake_detect.py` and `norm.py` in `countermeasures` implement two methods of defense against poisoning attacks: **normalization** and **detection of fake users**. `both.py` uses these methods together. Specifically, the central server can first detect and remove the fake users, and then perform normalization. Run these programs on `tiny_synthetic_dataset.xlsx`.

Results:

- Impact of $$\beta$$ on MGA ($$r=10, \epsilon=1$$):
  - OUE:

![](https://github.com/pumpkinbo/LDP/blob/master/result/G%20vs%20beta%20(Countermeasures%20against%20MGA%20for%20OUE).png))

- Impact of $$r$$​ on MGA ($$\beta=0.05, \epsilon=1$$):
  - OUE:

![G vs r (countermeasures against MGA for OUE)](https://github.com/pumpkinbo/LDP/blob/master/result/G%20vs%20r%20(countermeasures%20against%20MGA%20for%20OUE).png)

## Others

The theoretical overall gain of RIA for OLH is derived based on the “perfect” hashing assumption, i.e., an item is hashed to a value in the hash domain $$[d']$$ uniformly at random. Practical hash functions may not satisfy this assumption. Therefore, the theoretical overall gain of RIA for OLH may be inaccurate in practice. `other exp/measure_ria_for_olh.py` use xxhash as hash functions to evaluate the gaps between the theoretical and practical overall gains (running on `synthetic_dataset.xlsx`). 

Result:

![theoretical vs. practical (RIA on OLH)](https://github.com/pumpkinbo/LDP/blob/master/other%20exp/theoretical%20vs.%20practical%20(RIA%20on%20OLH).png)

The theoretical overall gain of MGA for OLH is derived based on the assumption that the attacker can find a hash function that hashes all target items to the same value. In practice, we may not be able to find such hash functions within a given amount of time. Therefore, for each fake user, we randomly sample some xxhash hash functions and use the one that hashes the most target items to the same value. Run `hash_num_exp.py` on `small_synthetic_dataset.xlsx`.

Results:

![G vs number of hash functions（small dataset）](C:\Users\admin\Desktop\G vs number of hash functions（small dataset）.png)
