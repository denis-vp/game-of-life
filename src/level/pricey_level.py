import pygame

import src.constant.color as color
from src.level.sandbox_level import SandboxLevel


class PriceyLevel(SandboxLevel):
    """
    Class for a pricey level.
    Represents the playing field for Conway's Game of Life.
    There are a limited number of toggles available.
    """

    def __init__(self, x: int, y: int, width: int, height: int,
                 data_file: str, assets_dir_path: str, window: pygame.Surface) -> None:
        """
        :param x: int, the x position of the level.
        :param y: int, the y position of the level.
        :param width: int, the width of the level.
        :param height: int, the height of the level.
        :param data_file: str, the path to the file containing the level data.
        :param assets_dir_path: str, the path to the assets' directory.
        """

        self.max_toggles = None
        self.nr_toggles = 0
        self.current_toggles = set()

        super().__init__(x, y, width, height, data_file, assets_dir_path, window)

    # ------------------------------------------------------------------------------------------------- #

    def load_data(self) -> None:
        """
        Loads the level data from the level file.
        :return: None
        """

        with open(self.data_file, 'r') as file:
            lines = file.readlines()

            # Get the number of maximum toggles
            self.max_toggles = int(lines[0].split()[0])

            # Get the number of rows and columns
            self.nr_rows, self.nr_cols = map(int, lines[1].split())

            # Get the initial state
            for line in lines[2:]:
                if line.startswith('\n'):
                    break
                for cell in line.split():
                    self.initial_state.append(int(cell))
            self.current_state = self.initial_state.copy()

            # Get the desired state
            for line in lines[self.nr_rows + 3:]:
                for cell in line.split():
                    self.desired_state.append(int(cell))

    def reset(self) -> None:
        """
        Resets the level to its initial state.
        :return: None
        """

        super().reset()

        self.current_toggles = set()
        self.nr_toggles = 0

    # ------------------------------------------------------------------------------------------------- #

    def handle_mouse_click(self, x_pos: int, y_pos: int) -> None:
        """
        Handles a mouse click event.
        Checks if the click was inside the level and if it was, toggles the cell if there are still available toggles.
        :param x_pos: int, the x position of the mouse click.
        :param y_pos: int, the y position of the mouse click.
        :return: None
        """

        # Get the cell coordinates
        cell_x = int((x_pos - self.x) // self.cell_width)
        cell_y = int((y_pos - self.y) // self.cell_height)

        # Check if the cell is in the level
        if cell_x < 0 or cell_x >= self.nr_cols or cell_y < 0 or cell_y >= self.nr_rows:
            return

        # Toggle the cell if there are still available toggles
        cell_index = cell_y * self.nr_cols + cell_x
        if cell_index in self.current_toggles:
            self.toggle_cell(cell_index)

            self.current_toggles.remove(cell_index)
            self.nr_toggles -= 1

        elif self.nr_toggles < self.max_toggles:
            self.toggle_cell(cell_index)

            self.current_toggles.add(cell_index)
            self.nr_toggles += 1

    # ------------------------------------------------------------------------------------------------- #

    def __copy__(self) -> 'PriceyLevel':
        """
        Returns a shallow copy of the level.
        :return: PriceyLevel, the shallow copy of the level.
        """

        copy = PriceyLevel(self.x, self.y, self.width, self.height, self.data_file, self.assets_dir_path, self.window)

        copy.max_toggles = self.max_toggles
        copy.nr_toggles = self.nr_toggles
        copy.current_toggles = self.current_toggles

        copy.initial_state = self.initial_state
        copy.current_state = self.current_state
        copy.desired_state = self.desired_state

        return copy

    def __deepcopy__(self, memodict={}) -> 'PriceyLevel':
        """
        Returns a deep copy of the level.
        :param memodict: dict, the memo dictionary.
        :return: PriceyLevel, the deep copy of the level.
        """

        copy = PriceyLevel(self.x, self.y, self.width, self.height, self.data_file, self.assets_dir_path, self.window)

        copy.max_toggles = self.max_toggles
        copy.nr_toggles = self.nr_toggles
        copy.current_toggles = self.current_toggles.copy()

        copy.initial_state = self.initial_state.copy()
        copy.current_state = self.current_state.copy()
        copy.desired_state = self.desired_state.copy()

        return copy
