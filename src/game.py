import os.path
import pygame

from src.button.button import Button
from src.button.solid_color_push_button import SolidColorPushButton
from src.button.solid_color_toggle_button import SolidColorToggleButton
from src.button.toggle_button import ToggleButton
from src.error import GameError
import src.constant.constant as const
import src.constant.color as color
from src.level.sandbox_level import SandboxLevel


class Game:
    """
    Class for the game.
    Represents the game window of Conway's Game of Life.
    """

    def __init__(self, width: int, height: int, title: str, fps: int,
                 data_dir_path: str, assets_dir_path: str, levels: list[str]) -> None:
        """
        :param width: int, the width of the window.
        :param height: int, the height of the window.
        :param title: str, the title of the window.
        :param fps: int, the fps of the game.
        :param data_dir_path: str, the path to the data directory.
        :param assets_dir_path: str, the path to the assets' directory.
        :param levels: list[str], the list of levels to play.
        :raises: GameError if there are no levels to play.
        """

        self.width, self.height = width, height
        self.title = title
        self.fps = fps
        self.data_dir_path = data_dir_path
        self.assets_dir_path = assets_dir_path
        self.levels = levels

        self.level_index = 0
        if len(self.levels) == 0:
            raise GameError('No levels to play!')
        self.level = None

        self.is_ticking = False
        self.level_copy = None
        self.time_since_last_tick = 0

        self.buttons: dict[tuple[tuple[int, int], tuple[int, int]], Button] = {}

        self.window = None
        self.clock = None

        self.info_panel_height = self.height - int(self.height * const.LEVEL_TO_WINDOW_HEIGHT_RATIO)
        self.info_panel_text = None

        self.level_x, self.level_y = 0, self.info_panel_height
        self.level_width, self.level_height = None, None

        self.ready_window()

    # ------------------------------------------------------------------------------------------------- #

    def ready_window(self) -> None:
        """
        Prepares the window for the game.
        Computes the level's position and size and calls ready_level().
        :return: None
        """

        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()

        self.ready_level()
        self.ready_buttons()

    def ready_level(self) -> None:
        """
        Creates a new level object.
        :return: None
        :raises: GameError if the level type is invalid.
        """

        self.level_width = int(self.width * const.LEVEL_TO_WINDOW_WIDTH_RATIO)
        self.level_height = int(self.height * const.LEVEL_TO_WINDOW_HEIGHT_RATIO)

        level_file_name = self.levels[self.level_index]
        level_file_path = os.path.join(self.data_dir_path, level_file_name)
        level_assets_dir_path = os.path.join(self.assets_dir_path, 'level')

        file_name_tokens = level_file_name.split('.')[0].split('_')
        level_type = file_name_tokens[0].lower()
        level_name = ' '.join(file_name_tokens[1:]).title()

        if level_type == 'sandbox':
            from src.level.sandbox_level import SandboxLevel
            self.level = SandboxLevel(self.level_x, self.level_y, self.level_width, self.level_height,
                                      level_file_path, level_assets_dir_path, self.window)
            self.info_panel_text = f'{level_name} - Sandbox: No special rules. No goal.'

        elif level_type == 'pricey':
            from src.level.pricey_level import PriceyLevel
            self.level = PriceyLevel(self.level_x, self.level_y, self.level_width, self.level_height,
                                     level_file_path, level_assets_dir_path, self.window)
            self.info_panel_text = f'{level_name} - Pricey: Limited number of toggles.'

        else:
            raise GameError('Invalid level type!')

    def next_level(self) -> None:
        """
        Loads the next level.
        Untoggles all toggle buttons before loading the next level.
        :return: None
        :raises: GameError if there are no more levels to play.
        """

        self.untoggle_buttons()

        self.level_index += 1
        if self.level_index == len(self.levels):
            self.level_index = 0
        self.ready_level()

    def reset_level(self) -> None:
        """
        Resets the current level.
        Untoggles all toggle buttons before resetting the level.
        :return: None
        """

        self.untoggle_buttons()

        self.level.reset()

    def ready_buttons(self) -> None:
        """
        Creates the buttons for the game.
        :return: None
        """

        button_width = self.width - self.level_width
        button_height = self.level_height // 8

        # Tick button
        tick_button_x = self.level_width
        tick_button_y = self.info_panel_height
        tick_button = SolidColorPushButton(tick_button_x, tick_button_y, button_width, button_height, self.tick_level,
                                           self.window, color.blue, color.dark_blue, color.dark_blue, 'Tick')
        tick_button_coords = ((tick_button_x, tick_button_y), (tick_button_x + button_width, tick_button_y + button_height))
        self.buttons[tick_button_coords] = tick_button

        # Goal button
        goal_button_x = self.level_width
        goal_button_y = self.info_panel_height + button_height
        goal_button = SolidColorToggleButton(goal_button_x, goal_button_y, button_width, button_height, self.toggle_show_desired,
                                             self.window, color.plum, color.purple, 'Show Goal')
        goal_button_coords = ((goal_button_x, goal_button_y), (goal_button_x + button_width, goal_button_y + button_height))
        self.buttons[goal_button_coords] = goal_button

        # Advance button
        advance_button_x = self.level_width
        advance_button_y = self.info_panel_height + button_height * 2
        advance_button = SolidColorToggleButton(advance_button_x, advance_button_y, button_width, button_height, self.toggle_advancing,
                                                self.window, color.red, color.dark_red, 'Advance')
        advance_button_coords = ((advance_button_x, advance_button_y), (advance_button_x + button_width, advance_button_y + button_height))
        self.buttons[advance_button_coords] = advance_button

        # Reset button
        reset_button_x = self.level_width
        reset_button_y = self.info_panel_height + button_height * 3
        reset_button = SolidColorPushButton(reset_button_x, reset_button_y, button_width, button_height, self.reset_level,
                                            self.window, color.yellow, color.orange, color.orange, 'Reset')
        reset_button_coords = ((reset_button_x, reset_button_y), (reset_button_x + button_width, reset_button_y + button_height))
        self.buttons[reset_button_coords] = reset_button

        # Next level button
        next_level_button_x = self.level_width
        next_level_button_y = self.info_panel_height + button_height * 4
        next_level_button = SolidColorPushButton(next_level_button_x, next_level_button_y, button_width, button_height, self.next_level,
                                                 self.window, color.green, color.dark_green, color.dark_green, 'Next Level')
        next_level_button_coords = ((next_level_button_x, next_level_button_y), (next_level_button_x + button_width, next_level_button_y + button_height))
        self.buttons[next_level_button_coords] = next_level_button

    def untoggle_buttons(self) -> None:
        """
        Untoggles all toggle buttons.
        :return: None
        """

        for button in self.buttons.values():
            if isinstance(button, ToggleButton):
                button.toggled = False

    # ------------------------------------------------------------------------------------------------- #

    def run(self) -> None:
        """
        Main loop of the game.
        :return: None
        """

        running = True
        while running:
            # Limit the frame rate
            self.clock.tick(self.fps)

            # Get mouse position for events
            x_pos, y_pos = pygame.mouse.get_pos()
            self.handle_mouse_hover(x_pos, y_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(x_pos, y_pos)

            self.advance()

            self.draw()
            pygame.display.update()

        pygame.quit()
        quit()

    # ------------------------------------------------------------------------------------------------- #

    def tick_level(self) -> None:
        """
        Ticks the level.
        :return: None
        """

        if not self.is_ticking:
            self.level.tick()

    def toggle_show_desired(self) -> None:
        """
        Toggles the show_desired flag.
        :return: None
        """

        # Check if the level is a sandbox level
        if not type(self.level) == SandboxLevel:
            self.level.show_desired = not self.level.show_desired

    def toggle_advancing(self) -> None:
        """
        Sets the is_ticking flag.
        :return: None
        """

        if not self.is_ticking:
            self.level_copy = self.level.__deepcopy__()
            self.is_ticking = True
        else:
            self.level = self.level_copy
            self.is_ticking = False

    def advance(self) -> None:
        """
        Advances the game to the next state if the corresponding button was toggled.
        Limits the advance to twice per second.
        :return: None
        """

        if self.is_ticking:
            self.time_since_last_tick += self.clock.get_time()
            if self.time_since_last_tick >= 500:
                self.level.tick()
                self.time_since_last_tick = 0

    # ------------------------------------------------------------------------------------------------- #

    def handle_mouse_click(self, x_pos: int, y_pos: int) -> None:
        """
        Handles a mouse click event.
        :param x_pos: int, the x position of the mouse click.
        :param y_pos: int, the y position of the mouse click.
        :return: None
        """

        # Check if the level was clicked
        if x_pos < self.level_width:
            if not self.is_ticking and not self.level.show_desired:
                self.level.handle_mouse_click(x_pos, y_pos)
            return

        # Check if a button was clicked
        for button_coords, button in self.buttons.items():
            if x_pos in range(button_coords[0][0], button_coords[1][0]) and y_pos in range(button_coords[0][1], button_coords[1][1]):
                button.click()
                return

    def handle_mouse_hover(self, x_pos: int, y_pos: int) -> None:
        # Check if a button was hovered
        for button_coords, button in self.buttons.items():
            if x_pos in range(button_coords[0][0], button_coords[1][0]) and y_pos in range(button_coords[0][1], button_coords[1][1]):
                button.hovered = True
            else:
                button.hovered = False

    # ------------------------------------------------------------------------------------------------- #

    def draw(self) -> None:
        """
        Draws the window.
        :return: None
        """

        self.window.fill(color.white)

        # Draw the info panel
        info_panel_rect = pygame.Rect(0, 0, self.width, self.info_panel_height)
        pygame.draw.rect(self.window, color.peru, info_panel_rect)

        text = pygame.font.SysFont(const.INFO_PANEL_FONT, const.INFO_PANEL_FONT_SIZE).render(self.info_panel_text, True, color.white)
        text_rect = text.get_rect()
        text_rect.x = 5
        text_rect.y = info_panel_rect.height // 2 - text_rect.height // 2

        self.window.blit(text, text_rect)

        # Draw the objects
        self.level.draw()
        for button in self.buttons.values():
            button.draw()
