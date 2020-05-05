# Matthew Kowal: Reinforcement Learning - Assignment 1
import math
import random
import numpy as np

# Q2 ~~~~~~~~~~~~~~~~~~~~~~~

# Setting the hyperparameters
alpha_inaction = 0.2
alpha_penalty = 0.6
beta_penalty = 0.4
N = 5000
k = 10

# Initializing true probabilities
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
reward_probs = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]

# Creating reward function
def score(probability):
    if random.random() < probability:
        return 1
    else:
        return 0

# creating LRI function
def linear_reward_inaction(alpha, d):
    # initializing counter variables
    total_reward = 0
    selected_number = [0] * d
    reward_sums = [0] * d
    optimal_choice = np.argmax(reward_probs)
    estimated_prob = [0.1 for i in range(d)]

    time_tracker = []
    optimal_choice_tracker = []
    average_reward_tracker = []

    # first choice of action
    choice = np.random.choice(d, p=estimated_prob)

    for t in range(N):
        reward = score(reward_probs[choice])
        selected_number[choice] += 1
        if reward == 1:
            estimated_prob[choice] += alpha * (1 - estimated_prob[choice])
            for x in range(len(estimated_prob)):
                if x is not choice:
                    estimated_prob[x] = (1 - alpha) * estimated_prob[x]

            total_reward += 1
            reward_sums[choice] += 1

        choice = np.random.choice(d, p=estimated_prob)

        if t!=0 and t % 100 == 0:
            print("At time-step " + str(t) + ": Optimal choice picked " +
            str(selected_number[optimal_choice]) + " times. Average Reward = " +
            str(total_reward/t))

        if t!=0:
            time_tracker.append(t)
            optimal_choice_tracker.append(selected_number[optimal_choice])
            average_reward_tracker.append(total_reward/t)
    return time_tracker, optimal_choice_tracker, average_reward_tracker



# creating LRP function
def linear_reward_penalty(alpha, beta, d):
    # initializing counter variables
    total_reward = 0
    selected_number = [0] * d
    reward_sums = [0] * d
    optimal_choice = np.argmax(reward_probs)
    estimated_prob = [0.1 for i in range(d)]

    time_tracker = []
    optimal_choice_tracker = []
    average_reward_tracker = []

    # first choice of action
    choice = np.random.choice(d, p=estimated_prob)

    for t in range(N):
        reward = score(reward_probs[choice])
        selected_number[choice] += 1
        if reward == 1:
            estimated_prob[choice] += alpha * (1 - estimated_prob[choice])
            for x in range(len(estimated_prob)):
                if x is not choice:
                    estimated_prob[x] = (1 - alpha) * estimated_prob[x]

            total_reward += 1
            reward_sums[choice] += 1
        else:
            estimated_prob[choice] = (1 - beta) * estimated_prob[choice]
            for x in range(len(estimated_prob)):
                if x is not choice:
                    estimated_prob[x] = (beta / (d-1)) + (1 - beta) * estimated_prob[x]

        choice = np.random.choice(d, p=estimated_prob)

        if t!=0 and t % 100 == 0:
            print("At time-step " + str(t) + ": Optimal choice picked " +
            str(selected_number[optimal_choice]) + " times. Average Reward = " +
            str(total_reward/t))

        if t!=0:
            time_tracker.append(t)
            optimal_choice_tracker.append(selected_number[optimal_choice])
            average_reward_tracker.append(total_reward/t)
    return time_tracker, optimal_choice_tracker, average_reward_tracker


# Running the algorithm once (comment out to run other algorithm)

#time, optimal_choice_tracker, average_reward_tracker = linear_reward_penalty(alpha = alpha_penalty, beta = beta_penalty, d = k)
time, optimal_choice_tracker, average_reward_tracker = linear_reward_inaction(alpha = alpha_penalty, d = k)


# Running the algorithm 100 times

# average_optimal_choice = []
# average_reward = []
#
# for i in range(100):
#     # (comment out to run other algorithm)
#     #time, optimal_choice_tracker, average_reward_tracker = linear_reward_inaction(alpha = alpha_penalty, d = k)
#     time, optimal_choice_tracker, average_reward_tracker = linear_reward_penalty(alpha = alpha_penalty, beta = beta_penalty, d = k)
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
