def policy_iteration(mdp, gamma=0.9):
  policy = {state: np.random.choice(mdp.action_space) for state in mdp.state_space if state != mdp.goal and state != mdp.trap}
  state_values = {state: 0.0 for state in mdp.state_space}
  while True:
    # Policy Evaluation
    while True:
      delta = 0
      for state in mdp.state_space:
        if state == mdp.goal or state == mdp.trap:
          continue
        v = state_values[state]
        action = policy[state]
        state_values[state] = sum([p * (mdp.rewards[next_state] + gamma * state_values[next_state])
      for p, next_state in mdp.transitions[state][action]])
        delta = max(delta, abs(v - state_values[state]))
        if delta < 0.01: # Fixed indentation
          break
  # Policy Improvement
  policy_stable = True
  for state in mdp.state_space:
    if state == mdp.goal or state == mdp.trap:
      continue
    old_action = policy[state]
    policy[state] = max(mdp.action_space, key=lambda a: sum([p * (mdp.rewards[next_state] + gamma * state_values[next_state])
  for p, next_state in mdp.transitions[state][a]]))
    if old_action != policy[state]:
      policy_stable = False
    if policy_stable:
      break
  return policy, state_values

  # Example Usage:
  size = 3
  goal = (2, 2)
  trap = (1, 1)
  mdp = GridWorldMDP(size, goal, trap)
  
  # Value Iteration
  value_iteration_result = value_iteration(mdp)
  print("Value Iteration Results:")
  for state, value in value_iteration_result.items():
    print(f"State: {state}, Value: {value}")

  # Policy Iteration
  policy_iteration_result, policy_iteration_state_values = policy_iteration(mdp)
  print("\nPolicy Iteration Results:")
  for state, action in policy_iteration_result.items():
    print(f"State: {state}, Action: {action}, Value: {policy_iteration_state_values[state]}")


