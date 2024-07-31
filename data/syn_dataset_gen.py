import pandas as pd
import numpy as np

n_total = 1000000
n_unique = 1024

# Generate integers that follow the Zipf distribution
ranks = np.arange(1, n_unique + 1)
probs = 1. / ranks  # zipf distribution
probs /= probs.sum()    # normalization
numbers = np.random.choice(ranks, size=n_total, p=probs)


unique_nums = [i for i in range(1, n_unique + 1)]

# write into file
data = {'Word': [unique_nums[num - 1] for num in numbers]}
df = pd.DataFrame(data)

output_file = 'synthetic_dataset.xlsx'
df.to_excel(output_file, index=False)

print(f"The systhetic dataset has been written to {output_file}.")
