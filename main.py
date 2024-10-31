from solver import Solver

def run_algorithm(algorithm, input_file, output_file):
    print("Running algorithm:", algorithm)
    solver = Solver(algorithm, input_file, output_file)
    solver.run()

if __name__ == "__main__":
    input = "inputs/input-10.txt"
    run_algorithm("DFS", input, "outputs/output-01.txt")
    run_algorithm("BFS", input, "outputs/output-02.txt")
    run_algorithm("UCS", input, "outputs/output-03.txt")
    run_algorithm("A*", input, "outputs/output-04.txt")
