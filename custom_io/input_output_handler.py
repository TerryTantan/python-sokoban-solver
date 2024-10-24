from core.grid import Grid


class InputOutputHandler:
    """
    A class to handle reading input for the Sokoban game.

    Attributes:
        input_path (str): The path to the input file.
        output_path (str): The path to the output file.
    """

    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path

    def load_from_file(self) -> Grid:
        with open(self.input_path, "r") as file:
            weight_data = file.readline()  # no need to strip
            grid_data = file.readlines()

        return Grid(weight_data, grid_data)

    def save_to_file(self, data: str) -> None:
        with open(self.output_path, "w") as file:
            file.write(data)
