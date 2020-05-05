# # Matthew Kowal: Reinforcement Learning - Assignment 1
import math
import random
from operator import add
import numpy as np

# Q3 ~~~~~~~~~~~~~~~~~~~~~~~

rows = 3
cols = 3
step_size = 0
timestep = 0

# creating an empty board
def create_new_board():
    board = np.zeros((rows, cols))
    return board

# function returning the outcome of the game if it is finished
def is_game_over(board):
    agent_win = 0
    bot_win = 0
    tie = 0
    end = 0
    results = []

    # checking rows
    for i in range(0, rows):
        results.append(np.sum(board[i, :]))

    # check columns
    for i in range(0, cols):
        results.append(np.sum(board[:, i]))

    # check diagonals
    results.append(0)
    for i in range(0, rows):
        results[-1] += board[i, i]
    results.append(0)
    for i in range(0, rows):
        results[-1] += board[i, rows - 1 - i]

    for result in results:
        if result == 3:
            agent_win = 1
            end = 1
            return agent_win, bot_win, tie, end
        if result == -3:
            bot_win = 1
            end = 1
            return agent_win, bot_win, tie, end

    # whether it's a tie
    sum = np.sum(np.abs(board))
    if sum == rows * cols:
        agent_win = 0
        bot_win = 0
        tie = 1
        end = 1
    return agent_win, bot_win, tie, end

# defining hash function to create unique number for each board
def hash_function(board):
    hash_val = 0
    for i in board.reshape(rows * cols):
        if i == -1:
            i = 2
        hash_val = hash_val * 3 + i
    return int(hash_val)

# function to get all states into the value function table
def recursive_get_all_states(board, current_symbol, all_states):
    for i in range(0, rows):
        for j in range(0, cols):
            if board[i][j] == 0:
                new_state = next_state(board, i, j, current_symbol)
                new_hash = hash_function(new_state)
                if new_hash not in all_states.keys():
                    agent_win, bot_win, tie, end = is_game_over(board)
                    all_states[new_hash] = (new_state, is_game_over(new_state))
                    if end == 0:
                        recursive_get_all_states(new_state, -current_symbol, all_states)


# function to begin the value function table process
def get_all_states(board):
    current_symbol = 1
    all_states = dict()
    all_states[hash_function(board)] = (board, is_game_over(board))
    recursive_get_all_states(board, current_symbol, all_states)
    return all_states


# putting a player in position i,j
def next_state(board, i, j, symbol):
        new_state = np.copy(board)
        new_state[i, j] = symbol
        #print(new_state)
        return new_state

# all possible board configurations
board = create_new_board()
all_states = get_all_states(board)

# setting value function to 0 (loss), 1 (wins), 0.5 (else)
def set_values(states):
    state_values_dict = dict()
    for hash_val in all_states.keys():
        (state, ending_values) = all_states[hash_val]
        if ending_values[3] == 1:
            if ending_values[0] == 1:
                state_values_dict[hash_val] = 1
            elif ending_values[1] == 1:
                state_values_dict[hash_val] = 0
            elif ending_values[2] == 1:
                state_values_dict[hash_val] = 0
        else:
            state_values_dict[hash_val] = 0.5
    return state_values_dict

state_values = set_values(all_states)

# agent takes a turn
def take_turn(board):
    next_states = []
    next_positions = []
    global timestep, state_values
    for i in range(rows):
        for j in range(cols):
            if board[i,j] == 0:
                next_positions.append([i,j])
                next_board = next_state(board, i, j, 1)
                next_states.append(hash_function(next_board))

    if np.random.rand() < epsilon:
        turn = next_positions[np.random.randint(len(next_positions))]
        turn.append(1)
        timestep += 1
        return turn

    values = []
    for hash, pos in zip(next_states, next_positions):
        val = state_values[hash]
        values.append((val, pos))

    # to select one of the actions of equal value at random
    np.random.shuffle(values)
    values.sort(key=lambda x: x[0], reverse=True)
    turn = values[0][1]
    turn.append(1)
    timestep += 1
    return turn

# the row-playing opponent
def row_opponent(board_history, board):
    global timestep
    last_move = abs(board_history[timestep]) - abs(board_history[timestep-1])
    last_move_location = np.nonzero(last_move)
    possible_choices = []
    choose_row = last_move_location[0][0]
    if np.count_nonzero(board[last_move_location[0][0]]) == 3:
        for i in range(rows):
            for j in range(cols):
                if board[i,j] == 0:
                    possible_choices.append([i,j])
        num = np.random.randint(len(possible_choices))
        choice = possible_choices[num]
        board = next_state(board, choice[0], choice[1], -1)
    else:
        for j in range(cols):
            if board[choose_row,j] == 0:
                possible_choices.append([choose_row,j])
        num = np.random.randint(len(possible_choices))
        choice = possible_choices[num]
        board = next_state(board, choice[0], choice[1], -1)
    timestep += 1
    return board

# the column-playing opponent
def col_opponent(board_history, board):
    global timestep
    last_move = abs(board_history[-1]) - abs(board_history[-2])
    last_move_location = np.nonzero(last_move)
    possible_choices = []
    choose_col = last_move_location[1][0]
    if np.count_nonzero(board[:,last_move_location[1][0]]) == 3:
        for i in range(rows):
            for j in range(cols):
                if board[i,j] == 0:
                    possible_choices.append([i,j])
        num = np.random.randint(len(possible_choices))
        choice = possible_choices[num]
        board = next_state(board, choice[0], choice[1], -1)
    else:
        for i in range(rows):
            if board[i,choose_col] == 0:
                possible_choices.append([i,choose_col])
        num = np.random.randint(len(possible_choices))
        choice = possible_choices[num]
        board = next_state(board, choice[0], choice[1], -1)
    timestep += 1
    return board

# the diagonal-playing opponent
def diagonal_opponent(board_history, board):
    global timestep
    last_move = abs(board_history[timestep]) - abs(board_history[timestep-1])
    last_move_location = np.nonzero(last_move)
    possible_choices = []
    for i in range(rows):
        for j in range(cols):
            if board[i,j] == 0:
                possible_choices.append([i,j])
    # center case
    if (last_move_location[0][0], last_move_location[1][0]) == (1,1):
        num = np.random.randint(len(possible_choices))
        choice = possible_choices[num]
        board = next_state(board, choice[0], choice[1], -1)
    # corner cases
    elif (last_move_location[0][0], last_move_location[1][0]) == (0,0):
        if [2,2] in possible_choices:
            board = next_state(board, 2, 2, -1)
        else:
            num = np.random.randint(len(possible_choices))
            choice = possible_choices[num]
            board = next_state(board, choice[0], choice[1], -1)
    elif (last_move_location[0][0], last_move_location[1][0]) == (2,2):
        if [0,0] in possible_choices:
            board = next_state(board, 0, 0, -1)
        else:
            num = np.random.randint(len(possible_choices))
            choice = possible_choices[num]
            board = next_state(board, choice[0], choice[1], -1)
    elif (last_move_location[0][0], last_move_location[1][0]) == (2,0):
        if [0,2] in possible_choices:
            board = next_state(board, 0, 2, -1)
        else:
            num = np.random.randint(len(possible_choices))
            choice = possible_choices[num]
            board = next_state(board, choice[0], choice[1], -1)
    elif (last_move_location[0][0], last_move_location[1][0]) == (0,2):
        if [2,0] in possible_choices:
            board = next_state(board, 2, 0, -1)
        else:
            num = np.random.randint(len(possible_choices))
            choice = possible_choices[num]
            board = next_state(board, choice[0], choice[1], -1)
    # center border locations
    elif (last_move_location[0][0], last_move_location[1][0]) == (0,1):
        if [1,0] in possible_choices:
            board = next_state(board, 1, 0, -1)
        elif [1,2] in possible_choices:
            board = next_state(board, 1, 2, -1)
        else:
            num = np.random.randint(len(possible_choices))
            choice = possible_choices[num]
            board = next_state(board, choice[0], choice[1], -1)
    elif (last_move_location[0][0], last_move_location[1][0]) == (1,0):
        if [0,1] in possible_choices:
            board = next_state(board, 0, 1, -1)
        elif [2,1] in possible_choices:
            board = next_state(board, 2, 1, -1)
        else:
            num = np.random.randint(len(possible_choices))
            choice = possible_choices[num]
            board = next_state(board, choice[0], choice[1], -1)
    elif (last_move_location[0][0], last_move_location[1][0]) == (1,2):
        if [0,1] in possible_choices:
            board = next_state(board, 0, 1, -1)
        elif [2,1] in possible_choices:
            board = next_state(board, 2, 1, -1)
        else:
            num = np.random.randint(len(possible_choices))
            choice = possible_choices[num]
            board = next_state(board, choice[0], choice[1], -1)
    elif (last_move_location[0][0], last_move_location[1][0]) == (2,1):
        if [1,0] in possible_choices:
            board = next_state(board, 1, 0, -1)
        elif [1,2] in possible_choices:
            board = next_state(board, 1, 2, -1)
        else:
            num = np.random.randint(len(possible_choices))
            choice = possible_choices[num]
            board = next_state(board, choice[0], choice[1], -1)
    timestep += 1
    return board


def play_game(opponent):
    global state_values

    # create new board and tracking variables
    board = create_new_board()
    board_tracker = []
    state_value_tracker = []
    state_value_tracker.append(state_values[hash_function(board)])
    board_tracker.append(board)
    end = 0

    # each game can only take 9 turns max
    for i in range(10):
        # agent plays
        turn = take_turn(board)
        board = next_state(board, turn[0], turn[1], turn[2])
        state_value_tracker.append(state_values[hash_function(board)])
        board_tracker.append(board)
        # check to see if game is over
        agent_win, bot_win, tie, end = is_game_over(board)
        if end == 1:
            for j in reversed(range(len(state_value_tracker)-1)):
                # update value function
                temp_diff = learning_rate * (state_value_tracker[j+1] - state_value_tracker[j])
                state_values[hash_function(board_tracker[j])] += temp_diff
            return agent_win, bot_win, tie
        # opponent plays
        if opponent == 'row':
            board = row_opponent(board_tracker, board)
        elif opponent == 'col':
            board = col_opponent(board_tracker, board)
        elif opponent == 'diag':
            board = diagonal_opponent(board_tracker, board)
        state_value_tracker.append(state_values[hash_function(board)])
        board_tracker.append(board)
        agent_win, bot_win, tie, end = is_game_over(board)
        # update value function
        if end == 1:
            for j in reversed(range(len(board_tracker)-1)):
                temp_diff = learning_rate * (state_value_tracker[j+1] - state_value_tracker[j])
                state_values[hash_function(board_tracker[j])] += temp_diff
            return agent_win, bot_win, tie

# play game function WITHOUT update function
def play_game_test(opponent):
    global state_values
    board = create_new_board()
    board_tracker = []
    state_value_tracker = []
    state_value_tracker.append(state_values[hash_function(board)])
    board_tracker.append(board)
    end = 0
    for i in range(10):
        turn = take_turn(board)
        board = next_state(board, turn[0], turn[1], turn[2])
        state_value_tracker.append(state_values[hash_function(board)])
        board_tracker.append(board)
        agent_win, bot_win, tie, end = is_game_over(board)
        if end == 1:
            return agent_win, bot_win, tie
        if opponent == 'row':
            board = row_opponent(board_tracker, board)
        elif opponent == 'col':
            board = col_opponent(board_tracker, board)
        elif opponent == 'diag':
            board = diagonal_opponent(board_tracker, board)
        state_value_tracker.append(state_values[hash_function(board)])
        board_tracker.append(board)
        agent_win, bot_win, tie, end = is_game_over(board)
        if end == 1:
            return agent_win, bot_win, tie

# training function
def train(iterations, opponent, val_end):
    global timestep, learning_rate, state_values
    # keeps track of wins, losses, ties
    win_loss_tie = [0,0,0]
    last100_win_loss_tie = [0,0,0]
    sum_state_values_tracker = []
    sum_state_values_tracker.append(sum(state_values.values()))
    for t in range(iterations):
        timestep = 0
        win, loss, tie = play_game(opponent)
        sum_state_values_tracker.append(sum(state_values.values()))
        score = [win, loss, tie]
        win_loss_tie = list(map(add, win_loss_tie, score))
        if t !=0 and t % 500 == 0:
            print('Win %, Loss %, Tie % = ', [x / sum(win_loss_tie) for x in win_loss_tie])
        # if the value functions total values change less than 'val_end' -> return
        if abs(sum_state_values_tracker[t]-sum_state_values_tracker[t-1]) < val_end:
            print(t)
            return win_loss_tie

# play the opponent 1000 times and record win/loss/tie ratio
def test(opponent):
    global timestep, learning_rate, state_values
    test_win_loss_tie = [0,0,0]
    for t in range(1000):
        timestep = 0
        win, loss, tie = play_game_test(opponent)
        score = [win, loss, tie]
        test_win_loss_tie = list(map(add, test_win_loss_tie, score))
    return test_win_loss_tie


# set epsilon to 0 for greedy move
# 0 < epsilon < 1 for an epsilon chance at a random move
epsilon = 0.0

# learning rate (step size) parameter
learning_rate = 0.1

# train takes: 'row', 'col' or 'diag' for the three types of opponents.
# Iterations is the number to stop at if the sum of the value functions do not stop changing
# by val_end
scores = train(iterations = 10000, opponent = 'row', val_end = 0.0001)
# setting epsilon to 0 so agent doesn't explore during test time
epsilon = 0.0
test1000 = test('row') # MAKE SURE THIS MATCHES THE OPPONENT DURING TRAINING
print('For 1000 test games, Win %, Loss %, Tie % = ', [x / sum(test1000) for x in test1000])
