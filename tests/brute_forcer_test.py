import unittest
from logging import WARNING
from os import path

from solver import BruteForcer
from sudoku import Grid


class BruteForcerTest(unittest.TestCase):
    def test_solutions(self) -> None:
        self._test_solutions("topn87_hr.txt")

    def test_no_solutions(self) -> None:
        file_path = path.join(path.dirname(__file__), "datasets", "no_solutions.txt")
        with open(file_path) as file:
            for line in file:
                quiz = line.strip()
                grid = Grid(quiz)
                brute_forcer = BruteForcer(grid)
                with self.assertLogs(level=WARNING):
                    self.assertFalse(brute_forcer.solve(), f"{quiz} should be unsolvable")
                self.assertFalse(grid.is_solved, f"{quiz} should remain unsolvable")

    def _test_solutions(self, file_name: str) -> None:
        file_path = path.join(path.dirname(__file__), "datasets", file_name)
        with open(file_path) as file:
            for line in file:
                quiz, solution = line.strip().split(",")
                grid = Grid(quiz)
                brute_forcer = BruteForcer(grid)
                with self.assertNoLogs(level=WARNING):
                    self.assertTrue(brute_forcer.solve(), f"{quiz}: solution not found")
                    self.assertEqual(
                        "".join(str(cell.value) for cell in grid.cells), solution, f"{quiz}: wrong solution"
                    )


if __name__ == "__main__":
    unittest.main()
