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
- Change your working directory to the project directory: **22120049_22120405_22120406/**
- Create a virtual environment.
> `python -m venv Source\Venv`
- Activate the environment.
> `Source\Venv\Scripts\activate`
- Install dependencies.
> `pip install -r Source\requirements.txt`
- Open the game.
> `python Source\main.py`

## Directory Structure

```
22120049_22120405_22120406/ 
├── Source/ 
│ ├── Codes/ 
│ └── Resources/ 
│ ├── .gitignore 
│ ├── input-01.txt 
│ ├── input-02.txt 
│ ├── input-03.txt 
│ ├── input-04.txt 
│ ├── input-05.txt 
│ ├── input-06.txt 
│ ├── input-07.txt 
│ ├── input-08.txt 
│ ├── input-09.txt 
│ ├── input-10.txt 
│ ├── output-01.txt 
│ ├── output-02.txt 
│ ├── output-03.txt 
│ ├── output-04.txt 
│ ├── output-05.txt 
│ ├── output-06.txt 
│ ├── output-07.txt 
│ ├── output-08.txt 
│ ├── output-09.txt 
│ ├── output-10.txt 
│ ├── main.py 
│ ├── README.md 
│ └── requirements.txt
└── Report.pdf
```

- **Source/**: Contains all source files related to the project.
  - **Codes/**: Directory intended for code files.
  - **Resources/**: Directory with resource files used in the project.
    - **input-01.txt to input-10.txt**: Sample input files for testing or data processing.
    - **output-01.txt to output-10.txt**: Sample output files for testing or data processing.
    - **.gitignore**: Specifies files or directories that should be ignored by Git.
  - **main.py**: The main script file to run the application.
  - **README.md**: Provides an overview and instructions for using the project.
  - **requirements.txt**: Lists the dependencies required for the project.
- **Report.pdf**: Report about the application.

## How to Play

1. **Run the Game**: `python sokoban_game.py`
2. **Navigate Levels**: Use arrow keys to move the character.
3. **Choose Level**: Click "Levels" to select a level.
4. **Get Solution**: Select "Solution" and choose an algorithm to solve the level.
5. **Restart**: Click "Restart" at any point to reset the level.