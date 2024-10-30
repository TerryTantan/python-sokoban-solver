from solver import Solver

if __name__ == "__main__":
    # Parse arguments or input for algorithm choice and file paths
    algorithm = "DFS"  # Example, use argument parsing to select this dynamically
    input_file = "inputs/input-06.txt"
    output_file = "outputs/output-01.txt"

    solver = Solver(algorithm, input_file, output_file)
    solver.run()

    algorithm = "BFS"  # Example, use argument parsing to select this dynamically
    # input_file = "inputs/input-00.txt"
    output_file = "outputs/output-02.txt"
    solver = Solver(algorithm, input_file, output_file)
    solver.run()

    algorithm = "UCS"  # Example, use argument parsing to select this dynamically
    # input_file = "inputs/input-00.txt"
    output_file = "outputs/output-03.txt"
    solver = Solver(algorithm, input_file, output_file)
    solver.run()

    algorithm = "A*"  # Example, use argument parsing to select this dynamically
    # input_file = "inputs/input-00.txt"
    output_file = "outputs/output-04.txt"
    solver = Solver(algorithm, input_file, output_file)
    solver.run()