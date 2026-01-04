"""
Solution for ICPC 2023 World Finals - Problem F: Herding Cats
Author: [Your Name]
Algorithm: Greedy Strategy with Sequential Processing
"""

import sys

# Set recursion depth just in case
sys.setrecursionlimit(200005)

def can_arrange_for_test_case(n, m, cats_data):
    # Data Structures:
    # 1. cats_at_pot[p] = list of cat indices targeting pot p
    #    Size m+1 because pots are 1-based
    cats_at_pot = [[] for _ in range(m + 1)]
    
    # 2. cat_likes[i] = list of plants cat i likes
    cat_likes = [[] for _ in range(n)]
    
    # Populate data structures
    for cat_idx, (target_p, liked_plants) in enumerate(cats_data):
        cats_at_pot[target_p].append(cat_idx)
        cat_likes[cat_idx] = liked_plants

    # 3. Global Count: cnt[h] = how many ACTIVE cats like plant h
    cnt = [0] * (m + 1)
    for cat_idx in range(n):
        for plant in cat_likes[cat_idx]:
            cnt[plant] += 1

    # 4. used[h] = True if plant h is already placed in a pot
    used = [False] * (m + 1)

    # 5. zero_liked_stack = Stack of 'safe' plants (cnt[h] == 0)
    #    These plants are not liked by ANY active cat.
    zero_liked_stack = []
    for h in range(1, m + 1):
        if cnt[h] == 0:
            zero_liked_stack.append(h)
    
    # Pointer for zero_liked_stack to avoid O(N) pop from start
    z_ptr = 0

    # 6. Reusable frequency array for the current pot's processing
    freq = [0] * (m + 1)
    touched_plants = []

    # === MAIN GREEDY LOOP: Process pots 1 to m ===
    for pot_idx in range(1, m + 1):
        
        target_cats = cats_at_pot[pot_idx]
        
        # --- CASE A: This pot is a TARGET for some cats ---
        if target_cats:
            r = len(target_cats)
            
            # 1. Calculate frequency of plants liked by THESE target cats
            touched_plants.clear()
            for cat_idx in target_cats:
                for h in cat_likes[cat_idx]:
                    if freq[h] == 0:
                        touched_plants.append(h)
                    freq[h] += 1
            
            # 2. Find a valid plant 'chosen' that satisfies 3 conditions:
            #    a. All target cats like it (freq[h] == r)
            #    b. NO active non-target cats like it (cnt[h] == r)
            #    c. Plant is not used yet
            chosen = -1
            for h in touched_plants:
                if freq[h] == r and cnt[h] == r and not used[h]:
                    chosen = h
                    break
            
            # Cleanup freq array for next iteration (Crucial!)
            for h in touched_plants:
                freq[h] = 0
            
            # If no valid plant found, impossible
            if chosen == -1:
                return False
            
            # 3. Place the plant
            used[chosen] = True
            
            # 4. Update Global State (Cats stop here)
            for cat_idx in target_cats:
                for plant in cat_likes[cat_idx]:
                    cnt[plant] -= 1
                    # If plant becomes safe (count drops to 0) and unused, add to safe stack
                    if cnt[plant] == 0 and not used[plant]:
                        zero_liked_stack.append(plant)
                        
        # --- CASE B: This pot is NOT a target (must be safe) ---
        else:
            # We must pick a plant that NO active cat likes (from zero_liked_stack)
            chosen_safe = -1
            while z_ptr < len(zero_liked_stack):
                candidate = zero_liked_stack[z_ptr]
                z_ptr += 1 # Move pointer forward
                
                # Verify it hasn't been used (it might have been used in Case A)
                if not used[candidate]:
                    chosen_safe = candidate
                    break
            
            if chosen_safe == -1:
                return False # No safe plants left
            
            used[chosen_safe] = True
            # No need to update cnt, because cnt[chosen_safe] was already 0

    return True

def solve():
    # Robust I/O handling
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        # Read number of test cases
        num_test_cases = int(next(iterator))
        
        for _ in range(num_test_cases):
            # Read n and m
            n = int(next(iterator))
            m = int(next(iterator))
            
            cats_data = []
            for _ in range(n):
                # Read p (target) and k (num likes)
                p = int(next(iterator))
                k = int(next(iterator))
                likes = []
                for _ in range(k):
                    likes.append(int(next(iterator)))
                cats_data.append((p, likes))
            
            # Run Solver
            if can_arrange_for_test_case(n, m, cats_data):
                print("yes")
            else:
                print("no")
                
    except StopIteration:
        pass

if __name__ == "__main__":
    solve()
