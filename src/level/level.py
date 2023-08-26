import os
import pygame
from abc import ABC, abstractmethod


class Level(ABC):
    """
    Abstract class for a level.
    Represents the playing field for Conway's Game of Life.
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

        self.x, self.y = x, y
        self.width, self.height = width, height
        self.data_file = data_file
        self.assets_dir_path = assets_dir_path
        self.window = window

        self.initial_state = []
        self.current_state = []
        self.desired_state = []
        self.nr_rows, self.nr_cols = None, None
        self.load_data()

        self.show_desired = False
        self.cell_width, self.cell_height = None, None
        self.alive_cell_image, self.dead_cell_image = None, None

        self.load_assets()

    # ------------------------------------------------------------------------------------------------- #

    @abstractmethod
    def load_data(self) -> None:
        """
        Loads the level data from the level file.
        :return: None
        """

        pass

    def reset(self) -> None:
        """
        Resets the level to its initial state.
        :return: None
        """

        self.current_state = self.initial_state.copy()

    @abstractmethod
    def load_assets(self) -> None:
        """
        Loads the level's assets.
        :return: None
        """

        pass

    # ------------------------------------------------------------------------------------------------- #

    def toggle_cell(self, cell_index: int) -> None:
        """
        Toggles the cell at the given row and column.
        :param cell_index: int, the index of the cell to toggle.
        :return: None
        """

        if self.current_state[cell_index] == 0:
            self.current_state[cell_index] = 1
        elif self.current_state[cell_index] == 1:
            self.current_state[cell_index] = 0

    @abstractmethod
    def tick(self) -> None:
        """
        Advances the level to the next state.
        :return: None
        """

        pass

    # ------------------------------------------------------------------------------------------------- #

    def get_neighbors(self, cell_index: int) -> list[int]:
        """
        Returns the indices of the neighbors of the cell at the given row and column.
        :param cell_index: int, the index of the cell.
        :return: list[int], the indices of the neighbors of the cell at the given row and column.
        """

        neighbors = []
        if cell_index % self.nr_cols != 0:
            neighbors.append(cell_index - 1)
        if cell_index % self.nr_cols != self.nr_cols - 1:
            neighbors.append(cell_index + 1)
        if cell_index >= self.nr_cols:
            neighbors.append(cell_index - self.nr_cols)
        if cell_index < self.nr_cols * (self.nr_rows - 1):
            neighbors.append(cell_index + self.nr_cols)
        if cell_index % self.nr_cols != 0 and cell_index >= self.nr_cols:
            neighbors.append(cell_index - self.nr_cols - 1)
        if cell_index % self.nr_cols != self.nr_cols - 1 and cell_index >= self.nr_cols:
            neighbors.append(cell_index - self.nr_cols + 1)
        if cell_index % self.nr_cols != 0 and cell_index < self.nr_cols * (self.nr_rows - 1):
            neighbors.append(cell_index + self.nr_cols - 1)
        if cell_index % self.nr_cols != self.nr_cols - 1 and cell_index < self.nr_cols * (self.nr_rows - 1):
            neighbors.append(cell_index + self.nr_cols + 1)
        return neighbors

    def get_number_of_alive_neighbors(self, cell_index: int) -> int:
        """
        Returns the number of alive neighbors of the cell at the given row and column.
        :param cell_index: int, the index of the cell.
        :return: int, the number of alive neighbors of the cell at the given row and column.
        """

        alive_neighbors = 0
        for neighbor in self.get_neighbors(cell_index):
            if self.current_state[neighbor] == 1:
                alive_neighbors += 1
        return alive_neighbors

    # ------------------------------------------------------------------------------------------------- #

    @abstractmethod
    def handle_mouse_click(self, x_pos: int, y_pos: int) -> None:
        """
        Handles a mouse click event.
        Checks if the click was inside the level and if it was, toggles the cell.
        :param x_pos: int, the x position of the mouse click.
        :param y_pos: int, the y position of the mouse click.
        :return: None
        """

        pass

    # ------------------------------------------------------------------------------------------------- #

    def draw(self) -> None:
        """
        Draws the level on the given surface.
        :return: None
        """

        if self.show_desired:
            self.draw_desired()
        else:
            self.draw_current()

    @abstractmethod
    def draw_current(self) -> None:
        """
        Draws the current state of the level on the given surface.
        :return: None
        """

        pass

    @abstractmethod
    def draw_desired(self) -> None:
        """
        Draws the desired state of the level on the given surface.
        :return: None
        """

        pass

    # ------------------------------------------------------------------------------------------------- #

    @abstractmethod
    def __copy__(self) -> 'Level':
        """
        Returns a shallow copy of the level.
        :return: Level, a shallow copy of the level.
        """

        pass

    @abstractmethod
    def __deepcopy__(self, memodict={}) -> 'Level':
        """
        Returns a deep copy of the level.
        :return: Level, a deep copy of the level.
        """

        pass
