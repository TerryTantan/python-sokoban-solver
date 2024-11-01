from solver import Solver

if __name__ == "__main__":
    # Parse arguments or input for algorithm choice and file paths
    algorithms = ["DFS", "BFS", "UCS", "A*"]

    for i in range(9, 11):  # Loop from input-01 to input-10
        for algorithm in algorithms:
            if not (algorithm == "DFS" or algorithm == "BFS"):
                continue
            _algorithm = algorithm
            if algorithm == "A*":
                _algorithm = "AStar"
            input_file = f"inputs/input-{i:02d}.txt"  # Format to input-01, input-02, ..., input-08
            output_file = f"outputs/{_algorithm}/output{_algorithm}Latest-{i:02d}.txt"  # Format to outputAlgorithmNameNew-number.txt

            solver = Solver(algorithm, input_file, output_file)
            solver.run()

    # Run BFS on test 2
    # input_file = "inputs/input-03.txt"
    # output_file = "outputs/BFS/outputBFSNew-03.txt"
    # solver = Solver("BFS", input_file, output_file)
    # solver.run()
