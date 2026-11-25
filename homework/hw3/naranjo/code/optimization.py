"""Budgeted optimization experiments for Homework 3.

GA, simulated annealing, and PSO operate on bounded vectors. For TSP,
random keys turn each vector into a tour by sorting its components.
"""
import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np


# Budget and BudgetExhausted are copied from studios/week-11/swarm.py.
class BudgetExhausted(Exception):
    pass


class Budget:
    """Every algorithm gets exactly the same number of fitness evaluations."""

    def __init__(self, f, max_evals):
        self.f, self.max_evals, self.used = f, max_evals, 0
        self.best = float("inf")
        self.trace = []          # best-so-far, indexed by EVALUATION

    def __call__(self, x):
        if self.used >= self.max_evals:
            raise BudgetExhausted()
        self.used += 1
        v = self.f(x)
        self.best = min(self.best, v)
        self.trace.append(self.best)
        return v

    def exhausted(self):
        return self.used >= self.max_evals


def rastrigin(x):
    x = np.asarray(x)
    return float(10 * len(x) + np.sum(x**2 - 10 * np.cos(2 * np.pi * x)))


def rosenbrock(x):
    x = np.asarray(x)
    return float(np.sum(100 * (x[1:] - x[:-1]**2)**2 + (1 - x[:-1])**2))


@dataclass(frozen=True)
class Problem:
    name: str
    dim: int
    bounds: tuple
    objective: object


def make_problem(name, dim, instance_seed=42):
    if dim < 2:
        raise ValueError("dimension must be at least 2")
    if name == "rastrigin":
        return Problem(name, dim, (-5.12, 5.12), rastrigin)
    if name == "rosenbrock":
        return Problem(name, dim, (-5.0, 10.0), rosenbrock)
    if name == "tsp":
        # Fixed across algorithm seeds, so all algorithms solve the same instance.
        points = np.random.default_rng(instance_seed).uniform(0, 1, (dim, 2))
        distances = np.linalg.norm(points[:, None] - points[None, :], axis=2)

        def tour_length(keys):
            tour = np.argsort(keys, kind="stable")
            return float(distances[tour, np.roll(tour, -1)].sum())

        return Problem(name, dim, (0.0, 1.0), tour_length)
    raise ValueError(f"unknown problem: {name}")


def genetic_algorithm(budget, dim, bounds, rng, population_size=30, mutation=0.1):
    """Tournament selection, arithmetic crossover, Gaussian mutation, elitism."""
    if population_size < 2 or mutation < 0:
        raise ValueError("population_size must be >= 2 and mutation nonnegative")
    lo, hi = bounds
    size = min(population_size, budget.max_evals - budget.used)
    if size == 0:
        return
    population = rng.uniform(lo, hi, (size, dim))
    scores = np.array([budget(x) for x in population])
    while not budget.exhausted():
        # Replace only the worst member if the child is better. This keeps the best.
        parents = []
        for _ in range(2):
            choices = rng.integers(size, size=2)
            parents.append(population[choices[np.argmin(scores[choices])]])
        alpha = rng.random(dim)
        child = alpha * parents[0] + (1 - alpha) * parents[1]
        mask = rng.random(dim) < 1 / dim
        child = np.clip(child + mask * rng.normal(0, mutation * (hi - lo), dim), lo, hi)
        score = budget(child)
        worst = int(np.argmax(scores))
        if score < scores[worst]:
            population[worst], scores[worst] = child, score


def simulated_annealing(budget, dim, bounds, rng, temperature=1.0, step=0.1):
    """Accept improvements and sometimes worse moves; cool over evaluations."""
    if temperature <= 0 or step <= 0:
        raise ValueError("temperature and step must be positive")
    if budget.exhausted():
        return
    lo, hi = bounds
    x = rng.uniform(lo, hi, dim)
    score = budget(x)
    while not budget.exhausted():
        candidate = np.clip(x + rng.normal(0, step * (hi - lo), dim), lo, hi)
        candidate_score = budget(candidate)
        temp = max(temperature * (1 - budget.used / budget.max_evals), 1e-12)
        difference = candidate_score - score
        if difference <= 0 or rng.random() < np.exp(-difference / temp):
            x, score = candidate, candidate_score


def particle_swarm(budget, dim, bounds, rng, particles=30, inertia=0.7, c1=1.5, c2=1.5):
    """PSO with personal/global bests and velocity clamping."""
    if particles < 1:
        raise ValueError("particles must be positive")
    lo, hi = bounds
    size = min(particles, budget.max_evals - budget.used)
    if size == 0:
        return
    positions = rng.uniform(lo, hi, (size, dim))
    velocity = rng.uniform(-0.1 * (hi - lo), 0.1 * (hi - lo), (size, dim))
    scores = np.array([budget(x) for x in positions])
    personal = positions.copy()
    personal_scores = scores.copy()
    best = personal[np.argmin(personal_scores)].copy()
    while not budget.exhausted():
        for i in range(size):
            if budget.exhausted():
                break
            velocity[i] = (inertia * velocity[i]
                           + c1 * rng.random(dim) * (personal[i] - positions[i])
                           + c2 * rng.random(dim) * (best - positions[i]))
            velocity[i] = np.clip(velocity[i], -0.2 * (hi - lo), 0.2 * (hi - lo))
            positions[i] = np.clip(positions[i] + velocity[i], lo, hi)
            score = budget(positions[i])
            if score < personal_scores[i]:
                personal[i], personal_scores[i] = positions[i].copy(), score
                best = personal[np.argmin(personal_scores)].copy()


def random_search(budget, dim, bounds, rng):
    while not budget.exhausted():
        budget(rng.uniform(*bounds, dim))


ALGORITHMS = {"ga": genetic_algorithm, "sa": simulated_annealing,
              "pso": particle_swarm, "random": random_search}


def run(problem, algorithm, evaluations, seed):
    if evaluations < 1:
        raise ValueError("evaluation budget must be positive")
    budget = Budget(problem.objective, evaluations)
    ALGORITHMS[algorithm](budget, problem.dim, problem.bounds, np.random.default_rng(seed))
    if budget.used != evaluations:
        raise RuntimeError("algorithm did not use its full budget")
    return budget


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--problem", choices=("rastrigin", "rosenbrock", "tsp"), required=True)
    parser.add_argument("--dim", type=int, required=True)
    parser.add_argument("--algorithm", choices=ALGORITHMS, required=True)
    parser.add_argument("--evaluations", type=int, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--instance-seed", type=int, default=42)
    parser.add_argument("--output", type=Path, required=True, help="CSV path for this run")
    args = parser.parse_args()
    problem = make_problem(args.problem, args.dim, args.instance_seed)
    budget = run(problem, args.algorithm, args.evaluations, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["problem", "dimension", "instance_seed", "algorithm", "seed", "budget", "evaluation", "best"])
        for evaluation, best in enumerate(budget.trace, 1):
            writer.writerow([args.problem, args.dim, args.instance_seed, args.algorithm,
                             args.seed, args.evaluations, evaluation, best])
    print(f"best={budget.best:.8g}; evaluations={budget.used}; output={args.output}")


if __name__ == "__main__":
    main()
