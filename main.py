from solver import Solver

if __name__ == "__main__":
    # Parse arguments or input for algorithm choice and file paths
    algorithm = "UCS"  # Example, use argument parsing to select this dynamically
    input_file = "inputs/input-01.txt"
    output_file = "outputs/output-01.txt"

    solver = Solver(algorithm, input_file, output_file)
    solver.run()

    # algorithm = "DFS"  # Example, use argument parsing to select this dynamically
    # input_file = "inputs/input-01.txt"
    # output_file = "outputs/outputDFS-01.txt"
    # solver = Solver(algorithm, input_file, output_file)
    # solver.run()
