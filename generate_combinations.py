import numpy as np
import itertools

# Given a set of N elements, choose m random, non-repeating subsets of k elements
def generate_combinations(df, k=5, m=500):
    list_of_dataframe_subsets = []

    temp_df = df.drop(['votes', 'player_id'], axis=1)

    total_variables = temp_df.columns.values.tolist()

    subsets = np.random.permutation([x for x in itertools.permutations(total_variables, k)])[:m]

    for subset in subsets:
        subset_df = df.drop(subset, axis=1)
        list_of_dataframe_subsets.append(subset_df)

    return list_of_dataframe_subsets
