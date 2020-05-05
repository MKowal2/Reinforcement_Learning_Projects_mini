# Reinforcement Learning Projects


In this repo, there are two main classes of RL algorithms implemented, based off of the algorithms found in the Reinforcement Learning (Sutton &amp; Barto 2nd Edition) textbook (which is a fantastic book, highly recommend!). The first set of algorithms are multi-armed bandits with two types of learning algorithms: Upper-confidence-bound action selection (section 2.7) and learning automata. There is also an implementation of a tic-tac-toe playing algorithm (section 1.5).

The second group of algorithms are temporal difference learning algorithms. I have implemented 3 algorithms which attempt to end up in the top right corner of a 10x10 grid, which is split into 4 equal squares, each square having a single doorway to access the other squares. The algorithm needs to learn to travel through these doorways and end up in the top right corner. The three algorithms implemented are:
- Monte Carlo control with epsilon-soft policies
- Q-learning
- SARSA 
