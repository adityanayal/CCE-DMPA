import pandas as pd
from itertools import combinations

# Function to generate candidate itemsets of length k from the previous frequent itemsets
def generate_candidates(prev_freq_itemsets, k):
    candidates = []
    for i in range(len(prev_freq_itemsets)):
        for j in range(i + 1, len(prev_freq_itemsets)):
            itemset1 = prev_freq_itemsets[i]
            itemset2 = prev_freq_itemsets[j]

            # Join step: Create a new candidate by merging two itemsets
            new_candidate = tuple(sorted(set(itemset1).union(itemset2)))

            # Prune step: Check if all subsets of the candidate are in the previous frequent itemsets
            prune = True
            for subset in combinations(new_candidate, k - 1):
                subset = tuple(sorted(subset))
                if subset not in prev_freq_itemsets:
                    prune = False
                    break

            if prune:
                candidates.append(new_candidate)

    return candidates

# Function to calculate support count for each candidate itemset
def calculate_support_count(candidate_itemsets, transactions):
    support_counts = {}
    for transaction in transactions:
        for candidate in candidate_itemsets:
            if set(candidate).issubset(transaction):
                if candidate in support_counts:
                    support_counts[candidate] += 1
                else:
                    support_counts[candidate] = 1
    return support_counts

# Function to find frequent itemsets using the Apriori algorithm with join and prune
def apriori_join_prune(transactions, min_support_count):
    frequent_itemsets = []
    k = 1
    unique_items = set(item for transaction in transactions for item in transaction)

    while True:
        if k == 1:
            candidate_itemsets = [(item,) for item in unique_items]
        else:
            candidate_itemsets = generate_candidates(frequent_itemsets[-1], k)

        support_counts = calculate_support_count(candidate_itemsets, transactions)

        freq_itemsets_k = [itemset for itemset, count in support_counts.items() if count >= min_support_count]

        if not freq_itemsets_k:
            break

        frequent_itemsets.append(freq_itemsets_k)
        k += 1

    return frequent_itemsets

# Example usage
if __name__ == "__main__":
    # Read data from an Excel file
    excel_file_path = "your_excel_file.xlsx"
    df = pd.read_excel(excel_file_path)

    # Assuming your Excel file has a column named 'Transaction' containing transaction data
    transactions = df['Transaction'].str.split(',')

    # Set the minimum support count
    min_support_count = 2

    # Find frequent itemsets using Apriori with join and prune
    frequent_itemsets = apriori_join_prune(transactions, min_support_count)

    # Print the frequent itemsets
    for k, itemsets in enumerate(frequent_itemsets, start=1):
        print(f"Frequent Itemsets of Length {k}:")
        for itemset in itemsets:
            print(itemset)
