import math
from pathlib import Path
import tempfile
import unittest

from gwo import GreyWolf, _update_leaders, run_gwo


class GWOTests(unittest.TestCase):
    def test_leaders_demote_and_copy_positions(self):
        leaders = [GreyWolf([], math.inf) for _ in range(3)]
        for fitness in (3.0, 2.0, 1.0, 0.0):
            wolf = GreyWolf([fitness], fitness)
            _update_leaders(leaders, wolf)
        wolf.position[0] = 99.0
        self.assertEqual([leader.fitness for leader in leaders], [0.0, 1.0, 2.0])
        self.assertEqual(leaders[0].position, [0.0])

    def test_binary_convergence_and_reproducibility(self):
        first = run_gwo(seed=42, output_path=None)
        second = run_gwo(seed=42, output_path=None)
        self.assertEqual(first.best_position, second.best_position)
        self.assertEqual(first.history, second.history)
        self.assertLess(first.best_fitness, 1e-10)
        self.assertEqual(first.best_fitness, sum(x*x for x in first.best_position))
        self.assertTrue(all(a >= b for a, b in zip(first.history, first.history[1:])))

    def test_objective_receives_only_binary_parameters(self):
        target = [1, 0, 1, 1, 0, 1]
        evaluations = []

        def objective(position):
            self.assertEqual(len(position), len(target))
            self.assertTrue(all(type(bit) is int and bit in (0, 1)
                                for bit in position))
            evaluations.append(position.copy())
            return sum(bit != wanted for bit, wanted in zip(position, target))

        result = run_gwo(objective, dimensions=len(target), num_wolves=30,
                         max_iterations=50, seed=42, output_path=None)
        self.assertEqual(len(evaluations), 30 * 51)
        self.assertEqual(result.best_position, target)
        self.assertEqual(result.best_fitness, 0)

    def test_constant_objective_ties_and_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "results.txt"
            result = run_gwo(lambda position: 7.0, dimensions=1, num_wolves=3,
                             max_iterations=3, seed=1, output_path=output)
            self.assertEqual(result.history, [7.0] * 3)
            self.assertEqual(output.read_text(), "1: 7\n2: 7\n3: 7\n")

    def test_zero_iterations_and_evaluation_count(self):
        calls = []
        def objective(position):
            calls.append(position)
            return sum(x*x for x in position)
        result = run_gwo(objective, num_wolves=3, max_iterations=0,
                         seed=1, output_path=None)
        self.assertEqual(len(calls), 3)
        self.assertEqual(result.history, [])
        self.assertEqual(result.best_fitness, min(sum(x*x for x in p) for p in calls))

    def test_invalid_inputs(self):
        for options in ({"dimensions": 0}, {"num_wolves": 2},
                        {"max_iterations": -1}, {"dimensions": 1.5}):
            with self.assertRaises(ValueError):
                run_gwo(output_path=None, **options)
        with self.assertRaises(ValueError):
            run_gwo(lambda position: math.nan, output_path=None)


if __name__ == "__main__":
    unittest.main()
