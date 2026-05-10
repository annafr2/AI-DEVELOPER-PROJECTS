"""Training loop: runs N_EPISODES on the training split, validates, saves best model."""
import os
import numpy as np
import config
from environment import TradingEnv
from agent import DQNAgent


def run_episode(env: TradingEnv, agent: DQNAgent, train: bool = True):
    state = env.reset()
    total_reward = 0.0
    steps = 0

    while True:
        action = agent.select_action(state)
        next_state, reward, done, info = env.step(action)

        if train:
            ns = next_state if not done else np.zeros_like(state)
            agent.store(state, action, reward, ns, done)
            agent.learn()

        total_reward += reward
        steps        += 1
        if done or steps >= config.MAX_STEPS_PER_EPISODE:
            break
        state = next_state

    return total_reward, env.total_return_pct, env.total_trades


def train(splits: dict, ticker: str = config.DEFAULT_TICKER):
    agent        = DQNAgent()
    best_val_ret = -np.inf
    model_path   = os.path.join(config.MODEL_DIR, f"{ticker}_best.pt")

    ep_rewards, ep_returns, val_returns = [], [], []

    print(f"\nTraining Dueling DQN on {ticker} — {config.N_EPISODES} episodes")
    print(f"Device: {agent.device}  |  Replay buffer: {config.REPLAY_BUFFER_SIZE}")

    for ep in range(1, config.N_EPISODES + 1):
        train_env = TradingEnv(*splits["train"])
        rew, ret, trades = run_episode(train_env, agent, train=True)
        agent.decay_epsilon()
        ep_rewards.append(rew)
        ep_returns.append(ret)

        # ── Validation every 10 episodes ──────────────────────────────────────
        if ep % 10 == 0:
            val_env   = TradingEnv(*splits["val"])
            _, vret, _ = run_episode(val_env, agent, train=False)
            val_returns.append(vret)

            if vret > best_val_ret:
                best_val_ret = vret
                agent.save(model_path)

            avg_loss = np.mean(agent.losses[-200:]) if agent.losses else 0.0
            print(
                f"Ep {ep:4d}/{config.N_EPISODES} | "
                f"eps={agent.epsilon:.3f} | "
                f"train_ret={ret:+.1f}% | "
                f"val_ret={vret:+.1f}% | "
                f"trades={trades} | "
                f"loss={avg_loss:.4f}"
            )

    print(f"\nBest validation return: {best_val_ret:+.2f}%  → saved to {model_path}")
    return agent, ep_rewards, ep_returns, val_returns, model_path


def evaluate_test(splits: dict, agent: DQNAgent):
    test_env = TradingEnv(*splits["test"])
    _, ret, trades = run_episode(test_env, agent, train=False)
    pv = test_env.final_value
    print(f"\nTest set  |  final portfolio: ${pv:,.2f}  |  return: {ret:+.2f}%  |  trades: {trades}")
    return test_env
