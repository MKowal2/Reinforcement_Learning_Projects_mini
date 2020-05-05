# Assignment 2 ---> Question 2 - Monte Carlo

# Matthew Kowal – 500884938
# Jae Duk Seo – 500633241

# importing libraries
import numpy as np
import random
import math
import time

gamma = 0.9
eps = 0.25
alpha = 0.1

#p1 = 0.6
#p2 = 0.1
p1 = float(input("Probability p1 : ") or "0.6");
p2 = float(input("Probability p2 : ") or "0.1");
# ========== check if probabilities are correct ========
assert (p1+p2 <= 1.0),"Probabilities must be less than 1 in total!"
assert (p1 > 0 and p2 >= 0),"Probabilities cannot be negative!"


rgoal = 100
rmove = -1

world_size = 10

# left, up, right, down
actions = {'left': -1,
           'up': -10,
           'right': +1,
           'down': +10}

# terminal state function
def is_end(location):
    if location == 10:
        return True
    return False

# creating world numbered 1-100
world = np.arange(1, 101).reshape((world_size, world_size))

# determining agent location function
def agent_loc(board_number):
    index = np.where(world==board_number)
    index = [index[0][0],index[1][0]]
    return index

# world dynamics -> how agent takes a step
def step(board_number, action):
    possible_actions = []
    # corner cases
    top_left_corners = [1,6,51,56]
    if board_number in top_left_corners:
        if action == -10 or action == -1:
            if random.random() < (1-p1+p2):
                possible_actions.append(actions['down'])
                possible_actions.append(actions['right'])
                action = random.choice(possible_actions)
                new_agent_location = board_number + action
                return new_agent_location
            else:
                new_agent_location = board_number
                return new_agent_location
    top_right_corners = [5,55,60]
    if board_number in top_right_corners:
        if action == -10 or action == 1:
            if random.random() < (1-p1+p2):
                possible_actions.append(actions['down'])
                possible_actions.append(actions['left'])
                action = random.choice(possible_actions)
                new_agent_location = board_number + action
                return new_agent_location
            else:
                new_agent_location = board_number
                return new_agent_location
    bot_left_corners = [41,46,91,96]
    if board_number in bot_left_corners:
        if action == 10 or action == -1:
            if random.random() < (1-p1+p2):
                possible_actions.append(actions['up'])
                possible_actions.append(actions['right'])
                action = random.choice(possible_actions)
                new_agent_location = board_number + action
                return new_agent_location
            else:
                new_agent_location = board_number
                return new_agent_location
    bot_right_corners = [45,50,95,100]
    if board_number in bot_right_corners:
        if action == 10 or action == 1:
            if random.random() < (1-p1+p2):
                possible_actions.append(actions['up'])
                possible_actions.append(actions['left'])
                action = random.choice(possible_actions)
                new_agent_location = board_number + action
                return new_agent_location
            else:
                new_agent_location = board_number
                return new_agent_location

    # top edge
    if board_number <= 10:
        if action == 10:
            if random.random() < p1:
                new_agent_location = board_number + action
                return new_agent_location
        if action == -10:
            if random.random() < (1-p1+p2):
                possible_actions.append(actions['left'])
                possible_actions.append(actions['right'])
                action = random.choice(possible_actions)
                new_agent_location = board_number + action
                return new_agent_location
        if action == 1:
            if random.random() < (1-p1+p2):
                possible_actions.append(actions['down'])
                action = random.choice(possible_actions)
                new_agent_location = board_number + action
                return new_agent_location
            else:
                new_agent_location = board_number + action
                return new_agent_location
        if action == -1:
            if random.random() < (1-p1+p2):
                possible_actions.append(actions['down'])
                action = random.choice(possible_actions)
                new_agent_location = board_number + action
                return new_agent_location
            else:
                new_agent_location = board_number + action
                return new_agent_location
        else:
            new_agent_location = board_number
            return new_agent_location
    # bottom edge
    if board_number >=90:
        if action == -10:
            if random.random() < p1:
                new_agent_location = board_number + action
                return new_agent_location
        if action == 10:
            if random.random() < (1-p1+p2):
                possible_actions.append(actions['left'])
                possible_actions.append(actions['right'])
                action = random.choice(possible_actions)
                new_agent_location = board_number + action
                return new_agent_location
        if action == 1:
            if random.random() < (1-p1+p2):
                possible_actions.append(actions['up'])
                action = random.choice(possible_actions)
                new_agent_location = board_number + action
                return new_agent_location
            else:
                new_agent_location = board_number + action
                return new_agent_location
        if action == -1:
            if random.random() < (1-p1+p2):
                possible_actions.append(actions['up'])
                action = random.choice(possible_actions)
                new_agent_location = board_number + action
                return new_agent_location
            else:
                new_agent_location = board_number + action
                return new_agent_location
        else:
            new_agent_location = board_number
            return new_agent_location
    # left edge
    if (board_number-1)%10 == 0:
        if action == 1:
            if random.random() < p1:
                new_agent_location = board_number + action
                return new_agent_location
        if action == -1:
            if random.random() < (1-p1+p2):
                possible_actions.append(actions['up'])
                possible_actions.append(actions['down'])
                action = random.choice(possible_actions)
                new_agent_location = board_number + action
                return new_agent_location
        if action == 10:
            if random.random() < (1-p1+p2):
                possible_actions.append(actions['right'])
                action = random.choice(possible_actions)
                new_agent_location = board_number + action
                return new_agent_location
            else:
                new_agent_location = board_number + action
                return new_agent_location
        if action == -10:
            if random.random() < (1-p1+p2):
                possible_actions.append(actions['right'])
                action = random.choice(possible_actions)
                new_agent_location = board_number + action
                return new_agent_location
            else:
                new_agent_location = board_number + action
                return new_agent_location
        else:
            new_agent_location = board_number
            return new_agent_location

    # right edge
    if board_number%10 == 0:
        if action == -1:
            if random.random() < p1:
                new_agent_location = board_number + action
                return new_agent_location
        if action == 1:
            if random.random() < (1-p1+p2):
                possible_actions.append(actions['up'])
                possible_actions.append(actions['down'])
                action = random.choice(possible_actions)
                new_agent_location = board_number + action
                return new_agent_location
        if action == 10:
            if random.random() < (1-p1+p2):
                possible_actions.append(actions['left'])
                action = random.choice(possible_actions)
                new_agent_location = board_number + action
                return new_agent_location
            else:
                new_agent_location = board_number + action
                return new_agent_location
        if action == -10:
            if random.random() < (1-p1+p2):
                possible_actions.append(actions['left'])
                action = random.choice(possible_actions)
                new_agent_location = board_number + action
                return new_agent_location
            else:
                new_agent_location = board_number + action
                return new_agent_location
        else:
            new_agent_location = board_number
            return new_agent_location

    # middle row sections
    top_middle = [42,44,47,49]
    if board_number in top_middle and action == 10:
        if random.random() < (1-p1+p2):
            possible_actions.append(actions['left'])
            possible_actions.append(actions['right'])
            action = random.choice(possible_actions)
            new_agent_location = board_number + action
            return new_agent_location
        else:
            new_agent_location = board_number
            return new_agent_location
    bottom_middle = [52,54,57,59]
    if board_number in bottom_middle and action == -10:
        if random.random() < (1-p1+p2):
            possible_actions.append(actions['left'])
            possible_actions.append(actions['right'])
            action = random.choice(possible_actions)
            new_agent_location = board_number + action
            return new_agent_location
        else:
            new_agent_location = board_number
            return new_agent_location


    # middle vertical sections
    top_middle = [15,35,65,85]
    if board_number in top_middle and action == 1:
        if random.random() < (1-p1+p2):
            possible_actions.append(actions['up'])
            possible_actions.append(actions['down'])
            action = random.choice(possible_actions)
            new_agent_location = board_number + action
            return new_agent_location
        else:
            new_agent_location = board_number
            return new_agent_location
    bottom_middle = [16,36,66,86]
    if board_number in bottom_middle and action == -1:
        if random.random() < (1-p1+p2):
            possible_actions.append(actions['up'])
            possible_actions.append(actions['down'])
            action = random.choice(possible_actions)
            new_agent_location = board_number + action
            return new_agent_location
        else:
            new_agent_location = board_number
            return new_agent_location

    # doorway sections
    horiz_up_doors = [43,48]
    if board_number in horiz_up_doors and action == 10:
        if random.random() < p1:
            new_agent_location = board_number + action
            return new_agent_location
        if random.random() < (1-p1+p2):
            possible_actions.append(actions['left'])
            possible_actions.append(actions['right'])
            action = random.choice(possible_actions)
            new_agent_location = board_number + action
            return new_agent_location
        else:
            new_agent_location = board_number
            return new_agent_location
    horiz_down_doors = [53,58]
    if board_number in horiz_down_doors and action == -10:
        if random.random() < p1:
            new_agent_location = board_number + action
            return new_agent_location
        if random.random() < (1-p1+p2):
            possible_actions.append(actions['left'])
            possible_actions.append(actions['right'])
            action = random.choice(possible_actions)
            new_agent_location = board_number + action
            return new_agent_location
        else:
            new_agent_location = board_number
            return new_agent_location
    vert_right_doors = [26,76]
    if board_number in vert_right_doors and action == -1:
        if random.random() < p1:
            new_agent_location = board_number + action
            return new_agent_location
        if random.random() < (1-p1+p2):
            possible_actions.append(actions['up'])
            possible_actions.append(actions['down'])
            action = random.choice(possible_actions)
            new_agent_location = board_number + action
            return new_agent_location
        else:
            new_agent_location = board_number
            return new_agent_location
    vert_left_doors = [25,75]
    if board_number in vert_left_doors and action == 1:
        if random.random() < p1:
            new_agent_location = board_number + action
            return new_agent_location
        if random.random() < (1-p1+p2):
            possible_actions.append(actions['up'])
            possible_actions.append(actions['down'])
            action = random.choice(possible_actions)
            new_agent_location = board_number + action
            return new_agent_location
        else:
            new_agent_location = board_number
            return new_agent_location

    # regular board moves
    if action == 1 or action == -1:
        if random.random() < p1:
            new_agent_location = board_number + action
            return new_agent_location
        if random.random() < (1-p1+p2):
            possible_actions.append(actions['up'])
            possible_actions.append(actions['down'])
            action = random.choice(possible_actions)
            new_agent_location = board_number + action
            return new_agent_location
        else:
            new_agent_location = board_number
            return new_agent_location

    if action == 10 or action == -10:
        if random.random() < p1:
            new_agent_location = board_number + action
            return new_agent_location
        if random.random() < (1-p1+p2):
            possible_actions.append(actions['left'])
            possible_actions.append(actions['right'])
            action = random.choice(possible_actions)
            new_agent_location = board_number + action
            return new_agent_location
        else:
            new_agent_location = board_number
            return new_agent_location

    new_agent_location = board_number
    return new_agent_location

# initializing Q(s,a) to zero for all (s,a) format = [[left],[up],[right],[down]]
action_values = np.zeros((world_size, world_size,4))

# initializing list of returns to be averaged
return_lists = []
#create list for each state -> format = return_lists[board_location-1][0=left, 1=up, 2=right, 3=down]
for i in range(100):
    return_lists.append([[],[],[],[]])

# mapping from action to index (Left, Up, Right, Down)
def get_action_temp(action):
    if action == -1:
        action_temp = 0
    if action == -10:
        action_temp = 1
    if action == 1:
        action_temp = 2
    if action == 10:
        action_temp = 3
    return action_temp

# policy = probability of taking each action for each state-action pair
policy = []
for i in range(100):
    policy.append([0.25,0.25,0.25,0.25])

# make decision based on policy
def policy_decision(board_number):
    board_number = board_number-1
    possible_actions = []
    # choose argmax(policy2[board_number])
    policy_temp = np.copy(policy)

    if random.random() < eps:
        possible_actions.append(actions['left'])
        possible_actions.append(actions['up'])
        possible_actions.append(actions['right'])
        possible_actions.append(actions['down'])
        action = random.choice(possible_actions)
        return action

    maximum = max(policy_temp[board_number])
    for i in range(4):
        if policy_temp[board_number][i] == maximum:
            policy_temp[board_number][i] = 1
        else:
            policy_temp[i] = 0
    if np.count_nonzero(policy_temp[board_number]) > 1:
        if policy_temp[board_number][0] == 1:
            possible_actions.append(actions['left'])
        if policy_temp[board_number][1] == 1:
            possible_actions.append(actions['up'])
        if policy_temp[board_number][2] == 1:
            possible_actions.append(actions['right'])
        if policy_temp[board_number][3] == 1:
            possible_actions.append(actions['down'])
        action = random.choice(possible_actions)
        return action

    action = np.argmax(policy_temp[board_number])
    if action == 0:
        action = actions['left']
        return action
    if action == 1:
        action = actions['up']
        return action
    if action == 2:
        action = actions['right']
        return action
    if action == 3:
        action = actions['down']
        return action


def monte_carlo(episodes):
    time_steps = 0
    #generate episode using pi
    for j in range(episodes):
        # create empty lists for each Returns(s,a)
        agent_location = random.randrange(1,100)

        # trivial case of starting in terminal state
        if agent_location == 10:
            agent_location = 9
        states_visited = []
        # create list of state-action pairs that were visited
        state_actions_visited = []

        # agent completes episode
        for t in range(1000000):
            time_steps += 1

            # check if agent location is in visited states
            if agent_location not in states_visited:
                states_visited.append(agent_location)

            # check if episode is over
            if is_end(agent_location):
                G = 100
                action_temp = get_action_temp(action)
                state_actions_visited.append([agent_location, action_temp])
                for stateaction in state_actions_visited:
                    return_lists[stateaction[0]-1][stateaction[1]].append(G)
                action_values[agent_loc(agent_location)[0], agent_loc(agent_location)[1],[action_temp]] = sum(return_lists[agent_location-1][action_temp])/len(return_lists[agent_location-1][action_temp])
                print(j+1, 'episodes completed!')
                print(time_steps, ' time steps total!')
                break

            action = policy_decision(agent_location)

            # calculate return and append to return_lists
            G = -1
            action_temp = get_action_temp(action)

            # check if agent location is in visited states
            if [agent_location, action_temp] not in state_actions_visited:
                state_actions_visited.append([agent_location, action_temp])
            for stateaction in state_actions_visited:
                return_lists[stateaction[0]-1][stateaction[1]].append(G)
            # set action value to new value
            action_values[agent_loc(agent_location)[0], agent_loc(agent_location)[1],[action_temp]] = sum(return_lists[agent_location-1][action_temp])/len(return_lists[agent_location-1][action_temp])

            # take step
            agent_location = step(agent_location, action)

        #then asssign new policy to argmaxa(Q(s,a))
        #for every state
        for s in states_visited:
            # set A_star to the best action
            A_star = np.max(action_values[agent_loc(s)[0], agent_loc(s)[1]])
            # for all actions
            count = 0
            for a in action_values[agent_loc(s)[0], agent_loc(s)[1]]:
                # if the action is best, set to 1-e-e/4
                if a == A_star:
                    policy[s-1][count] = 1-eps+(eps/4)
                # else set it to e/4
                else:
                    policy[s-1][count] = eps/4
                count += 1
        #policy_print(policy)

def policy_print(policy_lists):
    #display a 10x10 policy grid
    policy_display = []
    for i in range(10):
        policy_display.append([[],[],[],[],[],[],[],[],[],[]])
    count = 0
    for x in policy_lists:
        a = np.argmax(x)
        policy_display[math.floor(count/10)][count%10] = a
        count += 1

    for y in range(10):
        count2 = 0
        for j in policy_display[y]:
            if j == 0:
                policy_display[y][count2] = 'L'
            if j == 1:
                policy_display[y][count2] = 'U'
            if j == 2:
                policy_display[y][count2] = 'R'
            if j == 3:
                policy_display[y][count2] = 'D'
            count2 += 1
    # print optimal policy
    print('The optimal policy found is:')
    for z in policy_display:
        print(z)


start = time.time()
monte_carlo(episodes = 1000)
end = time.time()
print(policy)
policy_print(policy)
print('Monte Carlo took ', end - start, ' seconds!')
