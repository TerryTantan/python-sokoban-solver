from custom_io.input_output_handler import InputOutputHandler as IOHandler
from algorithms.dfs import DFS
from algorithms.bfs import BFS
from algorithms.ucs import UCS
from algorithms.base_search import BaseSearch, Solution
from core.grid import Grid


class Solver:
    def __init__(self, algorithm_name, input_file, output_file):
        self.algorithm_name = algorithm_name
        self.input_file = input_file
        self.output_file = output_file
        self.io_handler = IOHandler(self.input_file, self.output_file)

    def run(self):
        # Load initial state
        initial_grid = self.io_handler.load_from_file()

        # Choose algorithm
        algorithm: BaseSearch | None = None
        if self.algorithm_name == "DFS":
            algorithm = DFS(initial_grid)
        elif self.algorithm_name == "BFS":
            algorithm = BFS(initial_grid)
        elif self.algorithm_name == "UCS":
            algorithm = UCS(initial_grid)
        else:
            raise ValueError("Invalid algorithm name")
        # Add other algorithms here (BFS, UCS, AStar)

        # Run the search
        if algorithm.search():
            # Write output
            self.io_handler.save_to_file(
                self.algorithm_name + "\n" + str(algorithm.get_solution()),
            )
