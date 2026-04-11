# TASKS — L50 Dynamic Drone Race

## Phase 1: Core Implementation
- [x] `config.py` — all constants, event probabilities, hyperparameters
- [x] `environment.py` — DroneEnv with random pit / barrier / bridge / wind events
- [x] `agent_qlearn.py` — Q-Learning agent (model-free, epsilon-greedy)
- [x] `agent_bellman.py` — Value Iteration agent (model-based, re-solves on change)
- [x] `train.py` — dual-agent episode loop, synchronized environments
- [x] `visualize.py` — 4-panel competition dashboard
- [x] `main.py` — CLI entry point, final summary table

## Phase 2: Documentation
- [x] `PRD.md` — product requirements and architecture
- [x] `TASKS.md` — this file
- [x] `README.md` — simple English guide (explain like to a child)
- [x] `requirements.txt` — dependencies

## Phase 3: Testing
- [ ] Run `python main.py --no-viz` and verify 800 episodes complete
- [ ] Confirm events spawn (check "Events:" column in console output)
- [ ] Confirm Bellman re-solves (no error on first env change)
- [ ] Confirm `outputs/race_final.png` is created
- [ ] Verify all Python files are under 150 lines

## Phase 4: Experiments (optional, for deeper learning)

### Experiment A — Slower changes
Change `EVENT_INTERVAL = 60` in `config.py`.
Does Bellman win by an even bigger margin? Why?

### Experiment B — Rapid changes
Change `EVENT_INTERVAL = 10`, `EVENT_LIFETIME = 20`.
World changes very fast. Does Q-Learning keep up better? Why?

### Experiment C — Pit storm
Change `EVENT_WEIGHTS = [0.6, 0.1, 0.1, 0.2]` (more pits).
Which algorithm handles surprise danger better?

### Experiment D — Longer training
Increase `NUM_EPISODES = 2000`.
Does Q-Learning eventually catch up with Bellman given enough time?

### Experiment E — Swap to SARSA (on-policy Q-Learning)
In `train.py`, change `_run_qlearn` so that:
```python
next_action = agent.choose_action(next_state)
agent.update(state, action, reward, next_state, next_action, done)
```
And update `QLearningAgent.update` to accept `next_action` and use
`Q[next_state, next_action]` instead of `max Q[next_state]`.
Compare: does SARSA (safer) or Q-Learning (greedier) score higher?
