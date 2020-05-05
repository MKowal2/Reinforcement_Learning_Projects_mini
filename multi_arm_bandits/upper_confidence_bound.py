# Matthew Kowal: Reinforcement Learning - Assignment 1
import math
import random
from operator import add
import numpy as np

# Q1 ~~~~~~~~~~~~~~~~~~~~~~~

# Initializing hyperparameters
N = 5000
d = 10
c = 2


# Creating reward function
def score(probability):
    if random.random() < probability:
        return 1
    else:
        return 0

# Defining one run of the UCB algorithm
def ucb(num_steps, arms, exploration_rate):
    # Initializing probabilities and counter variables
    q1 = random.random()
    q2 = random.random()
    q3 = random.random()
    q4 = random.random()
    q5 = random.random()
    q6 = random.random()
    q7 = random.random()
    q8 = random.random()
    q9 = random.random()
    q10 = random.random()

    total_reward = 0
    selections = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
    selected_number = [0] * d
    reward_sums = [0] * d
    optimal_choice = np.argmax(selections)

    time_tracker = []
    optimal_choice_tracker = []
    average_reward_tracker = []

    for t in range(num_steps):
        # setting first upper bound
        max_upper_bound = 0

        for j in range(d):
            # If action j has been chosen before:
            if selected_number[j] > 0:
                # calculating the new upper bound according to UCB algorithm
                reward_average = reward_sums[j]/ selected_number[j]
                explore_value = exploration_rate * math.sqrt(math.log(t) / selected_number[j])
                upper_bound = reward_average + explore_value
            else:
                # else dummy upper bound
                upper_bound = 1e200
            # replace new upper bound if it is greater
            if upper_bound > max_upper_bound:
                max_upper_bound = upper_bound
                chosen_arm = j

        # update our counter variables
        selected_number[chosen_arm] += 1
        reward = score(selections[chosen_arm])
        reward_sums[chosen_arm] += reward
        total_reward += reward

        # print optimal choice number and average reward every 100 iterations
        if t!=0 and t % 100 == 0:
            print("At time-step " + str(t) + ": Optimal choice picked " +
            str(selected_number[optimal_choice]) + " times. Average Reward = " +
            str(total_reward/t))

        if t!=0:
            time_tracker.append(t)
            optimal_choice_tracker.append(selected_number[optimal_choice])
            average_reward_tracker.append(total_reward/t)
    return time_tracker, optimal_choice_tracker, average_reward_tracker

# Running the algorithm once

time, optimal_choice_tracker, average_reward_tracker = ucb(num_steps = N,arms = d, exploration_rate = c)


# ----- Running the algorithm 100 times ------

# average_optimal_choice = []
# average_reward = []
#
# for i in range(100):
#     time, optimal_choice_tracker, average_reward_tracker = ucb(num_steps = N,arms = d, exploration_rate = c)
#     average_optimal_choice.append(optimal_choice_tracker)
#     average_reward.append(average_reward_tracker)
#
#
# optimal_choice_perc = [sum(x) for x in zip(*average_optimal_choice)]
# ave_reward = [sum(x) for x in zip(*average_reward)]
#
# for i in range(len(optimal_choice_perc)):
#     ave_reward[i] = ave_reward[i]/(100)
#     if i ==0:
#         optimal_choice_perc[i] = optimal_choice_perc[i]/(100)
#     else:
#         optimal_choice_perc[i] = optimal_choice_perc[i]/(i*100)
