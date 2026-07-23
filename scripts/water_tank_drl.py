#!/usr/bin/env python3
"""Educational DRL example for an autonomous water tank level controller.

The controller learns a policy to keep a tank level near a target value by
observing a disturbance signal taken from the sensor hub recordings when they
are available. This is intentionally simple so students can see the core DRL
loop clearly:

1. Observe the current tank state and a sensor-based disturbance signal.
2. Choose a pump action.
3. Receive a reward for keeping the level close to the target.
4. Update the value estimates and improve the policy.
"""

from __future__ import annotations

import csv
import math
import random
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
SENSORHUB_RECORDINGS = ROOT / "sensorhub" / "recordings"


class WaterTankEnvironment:
    """A toy tank system with a nonlinear and noisy control response."""

    def __init__(self, disturbance_series: List[float], target_level: float = 50.0):
        self.disturbance_series = disturbance_series
        self.target_level = target_level
        self.level = target_level
        self.step_index = 0
        self.max_level = 100.0
        self.min_level = 0.0

    def reset(self) -> Tuple[int, int]:
        self.level = self.target_level
        self.step_index = 0
        return self._state()

    def _state(self) -> Tuple[int, int]:
        level_bucket = int(min(7, max(0, int(self.level / 12.5))))
        demand_bucket = int(min(7, max(0, int(self.current_demand() / 10))))
        return level_bucket, demand_bucket

    def current_demand(self) -> float:
        if not self.disturbance_series:
            return 0.0
        return self.disturbance_series[self.step_index % len(self.disturbance_series)]

    def step(self, action: int) -> Tuple[Tuple[int, int], float, bool]:
        demand = self.current_demand()

        # Simple nonlinear plant dynamics.
        # A larger pump command increases inflow, while demand pulls the level down.
        inflow = 0.35 + 0.06 * action
        outflow = 0.20 + 0.01 * demand
        self.level = max(
            self.min_level,
            min(self.max_level, self.level + inflow - outflow),
        )

        reward = -abs(self.level - self.target_level) - 0.03 * action
        reward -= 0.02 * max(0.0, abs(self.level - self.target_level) - 10.0)

        self.step_index += 1
        next_state = self._state()
        done = self.step_index >= len(self.disturbance_series)
        return next_state, reward, done


class QLearningController:
    """Tabular Q-learning for an educational DRL example."""

    def __init__(self, actions: List[int], alpha: float = 0.25, gamma: float = 0.95):
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.q_table: Dict[Tuple[Tuple[int, int], int], float] = {}
        self.epsilon = 1.0

    def _get_q(self, state: Tuple[int, int], action: int) -> float:
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state: Tuple[int, int]) -> int:
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        values = [self._get_q(state, action) for action in self.actions]
        best_value = max(values)
        best_actions = [a for a, v in zip(self.actions, values) if v == best_value]
        return random.choice(best_actions)

    def update(self, state: Tuple[int, int], action: int, reward: float, next_state: Tuple[int, int]) -> None:
        current = self._get_q(state, action)
        future = max(self._get_q(next_state, a) for a in self.actions)
        updated = current + self.alpha * (reward + self.gamma * future - current)
        self.q_table[(state, action)] = updated

    def decay_epsilon(self) -> None:
        self.epsilon = max(0.05, self.epsilon * 0.995)


def load_sensorhub_disturbance() -> List[float]:
    """Load a disturbance signal from the sensor hub recordings if available."""
    csv_files = sorted(SENSORHUB_RECORDINGS.glob("*.csv"))
    if csv_files:
        latest_file = max(csv_files, key=lambda p: p.stat().st_mtime)
        with latest_file.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            values = []
            for row in reader:
                # The sensor hub CSV has timestamp, value, actual_value.
                raw_value = row.get("value") or row.get("actual_value") or row.get("timestamp")
                try:
                    values.append(float(raw_value))
                except ValueError:
                    continue
            if values:
                return values

    # Fallback to a deterministic synthetic pattern if no sensor hub data exists.
    return [8 + 6 * math.sin(i / 4.0) + (i % 5) * 0.5 for i in range(80)]


def train_agent(episodes: int = 60, steps_per_episode: int = 40) -> Tuple[QLearningController, List[float]]:
    disturbance_series = load_sensorhub_disturbance()
    env = WaterTankEnvironment(disturbance_series=disturbance_series)
    controller = QLearningController(actions=[0, 1, 2, 3, 4])
    rewards_history: List[float] = []

    for episode in range(episodes):
        state = env.reset()
        episode_reward = 0.0

        for _ in range(steps_per_episode):
            action = controller.choose_action(state)
            next_state, reward, done = env.step(action)
            controller.update(state, action, reward, next_state)
            state = next_state
            episode_reward += reward

            if done:
                break

        controller.decay_epsilon()
        rewards_history.append(episode_reward)

    return controller, rewards_history


def evaluate_policy(controller: QLearningController, disturbance_series: List[float]) -> Tuple[List[float], List[float]]:
    env = WaterTankEnvironment(disturbance_series=disturbance_series)
    state = env.reset()
    levels: List[float] = [env.level]
    actions: List[float] = []

    for _ in range(len(disturbance_series)):
        action = controller.choose_action(state)
        actions.append(float(action))
        next_state, reward, done = env.step(action)
        state = next_state
        levels.append(env.level)
        if done:
            break

    return levels, actions


def main() -> None:
    print("Industrial Process Control: Autonomous Water Tank Level Controller")
    print("This script uses a simple DRL loop to learn pump control.\n")

    print("Step 1: Load water input sensor data from the sensor hub recordings.")
    disturbance_series = load_sensorhub_disturbance()
    print(f"Loaded {len(disturbance_series)} disturbance samples.")

    print("\nStep 2: Create the water tank environment and initialize the controller.")
    controller, rewards_history = train_agent(episodes=60, steps_per_episode=40)
    print(f"Average reward over the last 10 episodes: {sum(rewards_history[-10:]) / 10:.2f}")

    print("\nStep 3: Evaluate the learned policy on a fresh run.")
    levels, actions = evaluate_policy(controller, disturbance_series)
    print("First 10 control actions:", [int(a) for a in actions[:10]])
    print("Final tank level:", round(levels[-1], 2))
    print("Level trajectory (first 12 steps):", [round(v, 2) for v in levels[:12]])

    print("\nEducational note:")
    print("- The state is a simple discretized representation of tank level and demand.")
    print("- The pump action is a discrete control command.")
    print("- Q-learning is a classic DRL-style update that teaches the agent how to act.")


if __name__ == "__main__":
    main()
