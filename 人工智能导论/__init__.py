import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt

environment = gym.make("FrozenLake-v1", is_slippery=False)#, render_mode='human')
environment.reset()
environment.render()



plt.rcParams['figure.dpi'] = 300
plt.rcParams.update({'font.size': 17})

qtable = np.zeros((environment.observation_space.n, environment.action_space.n))

# Hyperparameters
episodes = 1000  # Total number of episodes
alpha = 0.5  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 1.0  # Amount of randomness in the action selection
epsilon_decay = 0.001  # Fixed amount to decrease

# List of outcomes to plot
outcomes = []

print('Q-table before training:')
print(qtable)

'''# Q-Learning
for _ in range(episodes):
    state, _ = environment.reset()
    done = False

    # By default, we consider our outcome to be a failure
    outcomes.append("Failure")

    # Until the agent gets stuck in a hole or reaches the goal, keep training it
    while not done:
        # Generate a random number between 0 and 1
        rnd = np.random.random()

        # If random number < epsilon, take a random action
        if rnd < epsilon:
            action = environment.action_space.sample()
        # Else, take the action with the highest value in the current state
        else:
            action = np.argmax(qtable[state])

        # Implement this action and move the agent in the desired direction
        new_state, reward, done, info, _ = environment.step(action)

        # Update Q(s,a)
        qtable[state, action] = qtable[state, action] + \
                                alpha * (reward + gamma * np.max(qtable[new_state]) - qtable[state, action])

        # Update our current state
        state = new_state

        # If we have a reward, it means that our outcome is a success
        if reward:
            outcomes[-1] = "Success"

    # Update epsilon
    epsilon = max(epsilon - epsilon_decay, 0)
    '''

# SARSA
for _ in range(episodes):
    state, _ = environment.reset()
    done = False

    # By default, we consider our outcome to be a failure
    outcomes.append("Failure")

    # Select the initial action using epsilon-greedy policy
    rnd = np.random.random()
    if rnd < epsilon:
        action = environment.action_space.sample()
    else:
        action = np.argmax(qtable[state])

    # Until the agent gets stuck in a hole or reaches the goal, keep training it
    while not done:
        # Implement the selected action and move the agent in the desired direction
        new_state, reward, done, info, _ = environment.step(action)

        # Select the next action using epsilon-greedy policy
        rnd = np.random.random()
        if rnd < epsilon:
            next_action = environment.action_space.sample()
        else:
            next_action = np.argmax(qtable[new_state])

        # Update Q(s,a)
        qtable[state, action] = qtable[state, action] + \
                                alpha * (reward + gamma * qtable[new_state, next_action] - qtable[state, action])

        # Update our current state and action
        state = new_state
        action = next_action

        # If we have a reward, it means that our outcome is a success
        if reward:
            outcomes[-1] = "Success"

    # Update epsilon
    epsilon = max(epsilon - epsilon_decay, 0)
#'''
print()
print('===========================================')
print('Q-table after training:')
print(qtable)



episodes = 100
nb_success = 0

# Evaluation
for _ in range(100):
    state, _ = environment.reset()
    done = False

    # Until the agent gets stuck or reaches the goal, keep training it
    while not done:
        # Choose the action with the highest value in the current state
        action = np.argmax(qtable[state])

        # Implement this action and move the agent in the desired direction
        new_state, reward, done, info, _ = environment.step(action)

        # Update our current state
        state = new_state

        # When we get a reward, it means we solved the game
        nb_success += reward

# Let's check our success rate!
print(f"Success rate = {nb_success / episodes * 100}%")
# Plot outcomes
plt.figure(figsize=(12, 5))
plt.xlabel("Run number")
plt.ylabel("Outcome")
ax = plt.gca()
ax.set_facecolor('#efeeea')
plt.bar(range(len(outcomes)), outcomes, color="#0A047A", width=1.0)
plt.show()