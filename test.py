import threading
import queue

solver_result = queue.Queue()
def solve_level():
    import time
    result = "rllldduddu"
    result = result.strip()
    for move in result:
        solver_result.put(move)

def start_solver():
    solver_thread = threading.Thread(target=solve_level)
    solver_thread.start()

start_solver()
while not solver_result.empty():
    print(solver_result.get())