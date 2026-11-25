# Homework 3: Optimization

This is the initial implementation for the optimization duel. It uses Python 3.10+ and NumPy, as in the course setup. GA, simulated annealing and PSO were written for this project with AI assistance. The `Budget` wrapper is copied from `studios/week-11/swarm.py`.

## Run

From this directory, install NumPy in your Python environment, then run:

```sh
python3 -m unittest discover -s code -v
python3 code/optimization.py --problem rastrigin --dim 2 --algorithm ga --evaluations 1000 --seed 0 --output results/example.csv
```

Select `rastrigin`, `rosenbrock`, or `tsp` and `ga`, `sa`, `pso`, or `random`. Each run writes one CSV row per objective evaluation, including its best-so-far value. The command refuses to overwrite an existing result. Use separate output names for each run.

Continuous bounds are [-5.12, 5.12] for Rastrigin and [-5, 10] for Rosenbrock. TSP points are uniformly generated in the unit square using `--instance-seed` (default 42), independently of the algorithm seed. A vector of random keys represents a tour: sort the keys to get the city order and include the return edge. This lets all three algorithms run on TSP, but their moves in key space differ from direct tour moves. Record and discuss that choice in the report.

## Still needed

The current code supports individual runs, not the full study. Agree on the budget, settings and TSP instances. Run at least 10 seeds per configuration, add the problem-specific baselines, aggregate results, create plots and the hyperparameter study, and implement the LLM experiment. Do not treat the smoke tests as experimental results. See `REPORT.md` for the remaining report sections and `AI_LOG.md` for the required disclosure and student reflection.
