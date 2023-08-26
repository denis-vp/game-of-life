import pygame
from abc import abstractmethod

from src.button.button import Button


class PushButton(Button):
    """
    Abstract class for a push button.
    """

    def __init__(self, x: int, y: int, width: int, height: int,
                 func: callable, window: pygame.Surface) -> None:
        """
        :param x: int, the x position of the button.
        :param y: int, the width of the button.
        :param width: int, the width of the button.
        :param height: int, the height of the button.
        :param func: int, the function to be called when the button is clicked.
        :param window: pygame.Surface, the surface to draw the button on.
        """

        self.hovered = False
        self.image_hover = None
        self.image_click = None

        super().__init__(x, y, width, height, func, window)

    @abstractmethod
    def load_assets(self) -> None:
        """
        Loads the button's assets.
        :return: None
        """

        pass

    def click(self) -> None:
        """
        Calls the button's function and plays the click animation.
        :return: None
        """

        self.draw_click()
        super().click()

    def draw(self) -> None:
        """
        Draws the button on the given surface.
        :return: None
        """

        if self.hovered:
            self.draw_hover()
        else:
            self.draw_normal()

    def draw_normal(self) -> None:
        """
        Draws the button on the given surface.
        :return: None
        """

        self.window.blit(self.image, (self.x, self.y))

    def draw_hover(self) -> None:
        """
        Draws the button's hover animation on the given surface.
        :return: None
        """

        self.window.blit(self.image_hover, (self.x, self.y))

    def draw_click(self) -> None:
        """
        Draws the button's click animation on the given surface.
        :return: None
        """

        self.window.blit(self.image_click, (self.x, self.y))
        pygame.display.update()
        pygame.time.delay(200)
        self.window.blit(self.image, (self.x, self.y))
