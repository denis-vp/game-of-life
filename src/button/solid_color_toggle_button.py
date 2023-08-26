import pygame

from src.button.toggle_button import ToggleButton
import src.constant.constant as const
import src.constant.color as color


class SolidColorToggleButton(ToggleButton):
    """
    A toggle button with a solid color and text.
    """

    def __init__(self, x: int, y: int, width: int, height: int,
                 func: callable, window: pygame.Surface,
                 color: tuple[int, int, int], color_toggled: tuple[int, int, int],
                 text: str = 'Temp') -> None:
        """
        :param x: int, the x position of the button.
        :param y: int, the width of the button.
        :param width: int, the width of the button.
        :param height: int, the height of the button.
        :param func: callable, the function to be called when the button is clicked.
        :param window: pygame.Surface, the surface to draw the button on.
        :param color: tuple[int, int, int], the color of the button.
        :param color_toggled: tuple[int, int, int], the color of the button when toggled.
        :param text: str, the text to be displayed on the button.
        """

        self.color = color
        self.color_toggled = color_toggled
        self.text = text

        super().__init__(x, y, width, height, func, window)

    def load_assets(self) -> None:
        """
        Loads the button's assets.
        :return: None
        """

        text = pygame.font.SysFont(const.BUTTON_FONT, const.BUTTON_FONT_SIZE).render(self.text, 1, color.black)

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.image.blit(text, (self.width // 2 - text.get_width() // 2,
                               self.height // 2 - text.get_height() // 2))

        self.image_toggled = pygame.Surface((self.width, self.height))
        self.image_toggled.fill(self.color_toggled)
        self.image_toggled.blit(text, (self.width // 2 - text.get_width() // 2,
                                       self.height // 2 - text.get_height() // 2))
