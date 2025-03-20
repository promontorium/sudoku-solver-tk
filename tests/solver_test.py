import unittest
from logging import WARNING
from os import path

from solver import StepSolver
from sudoku import Grid


class SolverTest(unittest.TestCase):
    def test_solutions1(self) -> None:
        self._test_solutions("test.txt")

    def test_solutions2(self) -> None:
        self._test_solutions("kaggle_small.txt")

    def test_solutions3(self) -> None:
        self._test_solutions("top87_ez.txt")

    def test_unsolvable(self) -> None:
        file_path = path.join(path.dirname(__file__), "datasets", "multiple_solutions.txt")
        with open(file_path) as file:
            for line in file:
                quiz = line.strip().split(",")[0]
                grid = Grid(quiz)
                grid.init_candidates()
                step_solver = StepSolver(grid)
                while step_solver.solve():
                    pass
                self.assertFalse(grid.is_solved, f"{quiz}: should not be solved")
                self.assertTrue(grid.is_consistent, f"{quiz}: is inconsistent")

    def _test_solutions(self, file_name: str) -> None:
        file_path = path.join(path.dirname(__file__), "datasets", file_name)
        with open(file_path) as file:
            for line in file:
                if line.startswith("#"):
                    continue
                quiz, solution = line.strip().split(",")
                grid = Grid(quiz)
                step_solver = StepSolver(grid)
                with self.assertNoLogs(level=WARNING):
                    grid.init_candidates()
                    while not grid.is_solved:  # TODO infinite loop ?
                        self.assertTrue(step_solver.solve(), f"{quiz} solution not found")
                result = "".join(str(cell.value) for cell in grid.cells)
                self.assertEqual(result, solution, f"{quiz}: wrong solution")


if __name__ == "__main__":
    unittest.main()
