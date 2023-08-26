import pygame

from src.button.push_button import PushButton


class SolidColorPushButton(PushButton):
    """
    A push button with a solid color and text.
    """

    def __init__(self, x: int, y: int, width: int, height: int,
                 func: callable, window: pygame.Surface,
                 color: tuple[int, int, int], color_hover: tuple[int, int, int], color_click: tuple[int, int, int],
                 text: str = 'Temp', font: str = 'comicsans') -> None:
        """
        :param x: int, the x position of the button.
        :param y: int, the width of the button.
        :param width: int, the width of the button.
        :param height: int, the height of the button.
        :param func: callable, the function to be called when the button is clicked.
        :param window: pygame.Surface, the surface to draw the button on.
        :param color: tuple[int, int, int], the color of the button.
        :param color_hover: tuple[int, int, int], the color of the button when hovered.
        :param color_click: tuple[int, int, int], the color of the button when clicked.
        :param text: str, the text to be displayed on the button.
        :param font: str, the font of the text (must be a font that pygame can render).
        """

        self.color = color
        self.color_hover = color_hover
        self.color_click = color_click
        self.text = text
        self.font = font

        super().__init__(x, y, width, height, func, window)

    def load_assets(self) -> None:
        """
        Loads the button's assets.
        :return: None
        """

        text = pygame.font.SysFont(self.font, 30).render(self.text, 1, (0, 0, 0))

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.image.blit(text, (self.width // 2 - text.get_width() // 2,
                               self.height // 2 - text.get_height() // 2))

        self.image_hover = pygame.Surface((self.width, self.height))
        self.image_hover.fill(self.color_hover)
        self.image_hover.blit(text, (self.width // 2 - text.get_width() // 2,
                                     self.height // 2 - text.get_height() // 2))

        self.image_click = pygame.Surface((self.width, self.height))
        self.image_click.fill(self.color_click)
        self.image_click.blit(text, (self.width // 2 - text.get_width() // 2,
                                     self.height // 2 - text.get_height() // 2))
