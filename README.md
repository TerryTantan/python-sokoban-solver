# Sokoban Game

This project is a Sokoban game created with **Pygame**. The game includes a UI with various game states, support for multiple levels, and a solver to automatically solve the levels. The UI is enhanced with textured buttons, and the game grid is rendered using textures for elements like walls, floor, stones, and switches.

## Features

- **Game States**: The game has multiple states (`playing`, `selecting`, `solution`, `solving`, `illustrating`, `pausing`, `won`) with buttons adapting to each state.
- **Solver Integration**: Levels can be solved by the solver, with visual illustration of the solution moves.
- **Texture-Based UI**: The game's UI elements, like buttons and board, are texture-based, allowing for a visually enhanced experience.
- **Interactive Buttons**: Buttons for different actions and game states respond to hover and click with visual effects.

## Requirements

- **Python 3.10 or higher**
- **Windows 10 or higher**

## How to Set up

- Open your terminal.
- Change your working directory to the project directory.
- Create a virtual environment.
> `python -m venv venv`
- Activate the environment.
> `venv\Scripts\activate`
- Install dependencies.
> `pip install -r requirements.txt`
- Open the game.
  - For GUI version.
  > `python sokoban_game_gui.py`
  - For CLI version.
  > `python sokoban_game_cli.py`

## Directory Structure

```
├── inputs/
│   └── inputs/
├── outputs/
│   ├── AStar/
│   ├── BFS/
│   ├── DFS/
│   └── UCS/
├── resources/
├── sources/
│   ├── algorithms/
│   ├── configs/
│   ├── core/
│   ├── custom_io/
│   ├── data_structures/
│   └── solver.py
├── .gitignore
├── README.md
├── requirements.txt
├── sokoban_game_cli.py
└── sokoban_game_gui.py
```

- **inputs**: Contains game levels files for the Sokoban game.
- **outputs**: Contains result files from different pathfinding algorithms:
  - **AStar**: Already generated output files from the A* pathfinding algorithm.
  - **BFS**: Already generated output files from Breadth-First Search algorithm.
  - **DFS**: Already generated output files from Depth-First Search algorithm.
  - **UCS**: Already generated output files from Uniform Cost Search algorithm.
- **resources**: Contains game assets.
- **sources**: Main source code directory containing:
  - **algorithms**: Implementation of various pathfinding/solving algorithms.
  - **configs**: Configuration files for game settings.
  - **core**: Core game logic and essential components.
  - **custom_io**: Input/output handling specific to your game.
  - **data_structures**: Custom data structures used in the game.
  - **solver**.py: Contains the main solving logic for the Sokoban puzzles.
- **requirements.txt**: Lists all Python package dependencies needed to run the game.
- **sokoban_game_cli.py**: Command-line interface version of the game.
- **sokoban_game_gui.py**: Graphical user interface version of the game.

## How to Play

1. **Run the Game**: `python sokoban_game.py`
2. **Navigate Levels**: Use arrow keys to move the character.
3. **Choose Level**: Click "Levels" to select a level.
4. **Get Solution**: Select "Solution" and choose an algorithm to solve the level.
5. **Restart**: Click "Restart" at any point to reset the level.