def first_fit(items, bin_capacity):
    bins = []
    for item in items:
        placed = False
        for bin in bins:
            if sum(bin) + item <= bin_capacity:
                bin.append(item)
                placed = True
                break
        if not placed:
            bins.append([item])
    return bins

def best_fit(items, bin_capacity):
    bins = []
    for item in items:
        best_bin = None
        min_space = bin_capacity
        for bin in bins:
            space = bin_capacity - (sum(bin) + item)
            if 0 <= space < min_space:
                min_space = space
                best_bin = bin
        
        if best_bin is not None:
            best_bin.append(item)
        else:
            bins.append([item])
    return bins

def worst_fit(items, bin_capacity):
    bins = []
    for item in items:
        max_space = -1
        worst_bin = None
        for bin in bins:
            space = bin_capacity - (sum(bin) + item)
            if space > max_space and space >= 0:
                max_space = space
                worst_bin = bin
        
        if worst_bin is not None:
            worst_bin.append(item)
        else:
            bins.append([item])
    return bins

def brute_force(items, bin_capacity):
    from itertools import permutations
    
    min_bins = len(items)  # pire cas: un bac par objet
    
    # On teste toutes les permutations possibles avec First-Fit
    for perm in permutations(items):
        bins = first_fit(perm, bin_capacity)
        if len(bins) < min_bins:
            min_bins = len(bins)
            if min_bins == 1:  # solution optimale trouvée
                break
    
    return min_bins