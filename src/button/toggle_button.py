import pygame
from abc import abstractmethod

from src.button.button import Button


class ToggleButton(Button):
    """
    Abstract class for a toggle button.
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

        self.toggled = False
        self.image_toggled = None

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

        if self.toggled:
            self.toggled = False
        else:
            self.toggled = True
        super().click()

    def draw(self) -> None:
        """
        Draws the button on the given surface.
        :return: None
        """

        if self.toggled:
            self.draw_toggled()
        else:
            self.draw_normal()

    def draw_normal(self) -> None:
        """
        Draws the button on the given surface.
        :return: None
        """

        self.window.blit(self.image, (self.x, self.y))

    def draw_toggled(self) -> None:
        """
        Draws the button's hover animation on the given surface.
        :return: None
        """

        self.window.blit(self.image_toggled, (self.x, self.y))
