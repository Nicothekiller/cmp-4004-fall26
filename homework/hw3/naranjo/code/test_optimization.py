import unittest

import numpy as np

from optimization import (ALGORITHMS, Budget, BudgetExhausted, make_problem,
                          rastrigin, rosenbrock, run)


class OptimizationTests(unittest.TestCase):
    def test_benchmarks_at_known_optima(self):
        self.assertAlmostEqual(rastrigin(np.zeros(10)), 0.0)
        self.assertAlmostEqual(rosenbrock(np.ones(10)), 0.0)

    def test_budget_enforces_limit_and_records_best(self):
        budget = Budget(lambda x: x, 3)
        for x in [3, 1, 2]:
            budget(x)
        self.assertEqual(budget.trace, [3, 1, 1])
        self.assertEqual(budget.used, 3)
        with self.assertRaises(BudgetExhausted):
            budget(0)
        self.assertEqual(budget.used, 3)

    def test_all_algorithms_spend_exact_budget_and_are_reproducible(self):
        for problem_name in ("rastrigin", "rosenbrock", "tsp"):
            for algorithm in ALGORITHMS:
                for evaluations in (1, 7, 33):
                    with self.subTest(problem=problem_name, algorithm=algorithm, budget=evaluations):
                        problem = make_problem(problem_name, 4)
                        first = run(problem, algorithm, evaluations, 123)
                        second = run(problem, algorithm, evaluations, 123)
                        self.assertEqual(first.used, evaluations)
                        self.assertEqual(len(first.trace), evaluations)
                        self.assertEqual(first.trace, second.trace)
                        self.assertTrue(all(a >= b for a, b in zip(first.trace, first.trace[1:])))

    def test_tsp_tour_is_closed_and_instance_is_repeatable(self):
        problem = make_problem("tsp", 5, instance_seed=42)
        keys = np.array([0.2, 0.1, 0.4, 0.3, 0.5])
        self.assertGreater(problem.objective(keys), 0)
        self.assertEqual(problem.objective(keys), make_problem("tsp", 5, 42).objective(keys))
        self.assertAlmostEqual(problem.objective(keys), problem.objective(-keys))

    def test_invalid_budgets(self):
        with self.assertRaises(ValueError):
            run(make_problem("rastrigin", 2), "ga", 0, 0)


if __name__ == "__main__":
    unittest.main()
