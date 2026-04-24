import numpy as np
class GridWorldMDP:
def __init__(self, size, goal, trap):
  self.size = size
  self.goal = goal
  self.trap = trap
  self.state_space = [(i, j) for i in range(size) for j in range(size)]
  self.action_space = ['UP', 'DOWN', 'LEFT', 'RIGHT']
  self.transitions = self.build_transitions()
  self.rewards = self.build_rewards()
def build_transitions(self):
  transitions = {}
  for state in self.state_space:
  transitions[state] = {}
  for action in self.action_space:
    transitions[state][action] = self.calculate_transitions(state, action)
  return transitions

def calculate_transitions(self, state, action):
  i, j = state
  if action == 'UP':
    return self.validate_state(i - 1, j)
  elif action == 'DOWN':
    return self.validate_state(i + 1, j)
  elif action == 'LEFT':
    return self.validate_state(i, j - 1)
  elif action == 'RIGHT':
    return self.validate_state(i, j + 1)
    
def validate_state(self, i, j):
  i = max(0, min(i, self.size - 1))
  j = max(0, min(j, self.size - 1))
  if (i, j) == self.goal or (i, j) == self.trap: # Added trap as terminal
    return [(1.0, (i, j))] # Stay in terminal state
  else:
    return [(1.0, (i, j))]

def validate_state(self, i, j):
  i = max(0, min(i, self.size - 1))
  j = max(0, min(j, self.size - 1))
  if (i, j) == self.goal or (i, j) == self.trap: # Added trap as terminal
    return [(1.0, (i, j))] # Stay in terminal state
  else:
    return [(1.0, (i, j))]
    
def build_rewards(self):
  rewards = {}
  for state in self.state_space:
    rewards[state] = -1.0 # Default reward
    rewards[self.goal] = 0.0 # Override goal
    rewards[self.trap] = -10.0 # Override trap
  return rewards

def value_iteration(mdp, gamma=0.9, epsilon=0.01):
  state_values = {state: 0.0 for state in mdp.state_space}
  while True:
    delta = 0
    
  for state in mdp.state_space:
    if state == mdp.goal or state == mdp.trap:
      continue
  v = state_values[state]
  state_values[state] = max([sum([p * (mdp.rewards[next_state] + gamma *
  state_values[next_state])
  for p, next_state in mdp.transitions[state][action]])
    for action in mdp.action_space])
      delta = max(delta, abs(v - state_values[state]))
      if delta < epsilon:
        break
  return state_values
