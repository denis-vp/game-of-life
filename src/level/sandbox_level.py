import pygame

from src.level.level import Level
import src.constant.color as color


class SandboxLevel(Level):
    """
    Class for a sandbox level.
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

        super().__init__(x, y, width, height, data_file, assets_dir_path, window)

    # ------------------------------------------------------------------------------------------------- #

    def load_data(self) -> None:
        """
        Loads the level data from the level file.
        :return: None
        """

        with open(self.data_file, 'r') as file:
            # Get the number of rows and columns
            self.nr_rows, self.nr_cols = map(int, file.readline().split())

            self.initial_state = [0 for _ in range(self.nr_rows * self.nr_cols)]
            self.current_state = [0 for _ in range(self.nr_rows * self.nr_cols)]
            self.desired_state = [-1 for _ in range(self.nr_rows * self.nr_cols)]

    def load_assets(self) -> None:
        """
        Loads the level's assets.
        Also computes the cell's width and height.
        :return: None
        """

        # Compute the cell's width and height
        self.cell_width = int(self.width // self.nr_cols)
        self.cell_height = int(self.height // self.nr_rows)

        # Load the level's assets
        self.alive_cell_image = pygame.image.load(self.assets_dir_path + '\\alive_cell.png')
        self.dead_cell_image = pygame.image.load(self.assets_dir_path + '\\dead_cell.png')

        # Scale the level's assets
        self.alive_cell_image = pygame.transform.scale(self.alive_cell_image, (self.cell_width, self.cell_height))
        self.dead_cell_image = pygame.transform.scale(self.dead_cell_image, (self.cell_width, self.cell_height))

    # ------------------------------------------------------------------------------------------------- #

    def tick(self):
        """
        Updates the level's state.
        :return: None
        """

        copy_current_state = self.current_state.copy()
        for cell_index in range(len(self.current_state)):
            alive_neighbors = self.get_number_of_alive_neighbors(cell_index)
            if self.current_state[cell_index] == 0 and alive_neighbors == 3:
                copy_current_state[cell_index] = 1
            elif self.current_state[cell_index] == 1 and (alive_neighbors < 2 or alive_neighbors > 3):
                copy_current_state[cell_index] = 0
        self.current_state = copy_current_state.copy()

    # ------------------------------------------------------------------------------------------------- #

    def handle_mouse_click(self, x_pos: int, y_pos: int) -> None:
        """
        Handles a mouse click event.
        Checks if the click was inside the level and if it was, toggles the cell.
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

        # Toggle the cell
        cell_index = cell_y * self.nr_cols + cell_x
        self.toggle_cell(cell_index)

    # ------------------------------------------------------------------------------------------------- #

    def draw_current(self) -> None:
        """
        Draws the current state of the level on the screen.
        :return: None
        """

        # Draw the cells
        cell_x, cell_y = self.x, self.y
        for row in range(self.nr_rows):
            for col in range(self.nr_cols):
                # Get the cell state
                cell_state = self.current_state[row * self.nr_cols + col]
                if cell_state == 0:
                    self.window.blit(self.dead_cell_image, (cell_x, cell_y))
                else:
                    self.window.blit(self.alive_cell_image, (cell_x, cell_y))

                # Move to the next cell
                cell_x += self.cell_width

            # Move to the next row
            cell_x = self.x
            cell_y += self.cell_height

        # Draw the level's cells' borders
        cell_x, cell_y = self.x, self.y
        for row in range(self.nr_rows + 1):
            pygame.draw.line(self.window, color.black, (cell_x, cell_y),
                             (cell_x + self.nr_cols * self.cell_width, cell_y))
            cell_y += self.cell_height

        cell_x, cell_y = self.x, self.y
        for col in range(self.nr_cols + 1):
            pygame.draw.line(self.window, color.black, (cell_x, cell_y),
                             (cell_x, cell_y + self.nr_rows * self.cell_height))
            cell_x += self.cell_width

    def draw_desired(self) -> None:
        """
        Draws the desired state of the level on the screen.
        :return: None
        """

        # Draw the cells
        cell_x, cell_y = self.x, self.y
        for row in range(self.nr_rows):
            for col in range(self.nr_cols):
                # Get the cell state
                cell_state = self.desired_state[row * self.nr_cols + col]
                if cell_state == 0:
                    self.window.blit(self.dead_cell_image, (cell_x, cell_y))
                else:
                    self.window.blit(self.alive_cell_image, (cell_x, cell_y))

                # Move to the next cell
                cell_x += self.cell_width

            # Move to the next row
            cell_x = self.x
            cell_y += self.cell_height

        # Draw the level's cells' borders
        cell_x, cell_y = self.x, self.y
        for row in range(self.nr_rows + 1):
            pygame.draw.line(self.window, color.black, (cell_x, cell_y),
                             (cell_x + self.nr_cols * self.cell_width, cell_y))
            cell_y += self.cell_height

        cell_x, cell_y = self.x, self.y
        for col in range(self.nr_cols + 1):
            pygame.draw.line(self.window, color.black, (cell_x, cell_y),
                             (cell_x, cell_y + self.nr_rows * self.cell_height))
            cell_x += self.cell_width

    # ------------------------------------------------------------------------------------------------- #

    def __copy__(self) -> 'SandboxLevel':
        """
        Creates a shallow copy of the level.
        :return: SandboxLevel, the shallow copy of the level.
        """

        copy = SandboxLevel(self.x, self.y, self.width, self.height, self.data_file, self.assets_dir_path, self.window)

        copy.initial_state = self.initial_state
        copy.current_state = self.current_state
        copy.desired_state = self.desired_state

        return copy

    def __deepcopy__(self, memodict = {}) -> 'SandboxLevel':
        """
        Creates a deep copy of the level.
        :param memodict: dict, the memo dictionary.
        :return: SandboxLevel, the deep copy of the level.
        """

        copy = SandboxLevel(self.x, self.y, self.width, self.height, self.data_file, self.assets_dir_path, self.window)

        copy.initial_state = self.initial_state.copy()
        copy.current_state = self.current_state.copy()
        copy.desired_state = self.desired_state.copy()

        return copy
