import random

# Number of simulations
NUM_TRIALS = 10000

# Counters for each condition
count_sum_7 = 0
count_sum_2 = 0
count_sum_gt_10 = 0

# Simulation loop: roll two dice NUM_TRIALS times
for _ in range(NUM_TRIALS):
    die1 = random.randint(1, 6)  # First die roll (1-6)
    die2 = random.randint(1, 6)  # Second die roll (1-6)
    total = die1 + die2          # Sum of the two dice

    # Count conditions
    if total == 7:
        count_sum_7 += 1
    elif total == 2:
        count_sum_2 += 1
    elif total > 10:
        count_sum_gt_10 += 1

# Calculate probabilities
p_sum_7 = count_sum_7 / NUM_TRIALS
p_sum_2 = count_sum_2 / NUM_TRIALS
p_sum_gt_10 = count_sum_gt_10 / NUM_TRIALS

# Display estimated probabilities
print(f"P(Sum = 7): {p_sum_7:.4f}")
print(f"P(Sum = 2): {p_sum_2:.4f}")
print(f"P(Sum > 10): {p_sum_gt_10:.4f}")
