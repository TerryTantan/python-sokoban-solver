from sources.solver import Solver
import argparse

def main():
    level = int(input("Enter level (1-10): "))
    while level not in range(1, 11):
        print("Invalid level. Please choose a level from 1 to 10.")
        level = int(input("Enter level (1-10): "))

    algorithm = input("Enter algorithm (DFS, BFS, UCS, A*): ")
    while algorithm not in ["DFS", "BFS", "UCS", "A*"]:
        print("Invalid algorithm. Please choose from DFS, BFS, UCS, A*.")
        algorithm = input("Enter algorithm (DFS, BFS, UCS, A*): ")

    if algorithm == "A*":
        algorithm = "AStar"
    input_file = f"inputs/input-{level:02d}.txt"
    output_file = f"outputs/output-{level:02d}.txt"

    print(f"\nRunning {algorithm} on level {level}...")

    solver = Solver(algorithm, input_file, output_file)
    solver.run()

    print(f"Output saved to {output_file}")

if __name__ == "__main__":
    main()