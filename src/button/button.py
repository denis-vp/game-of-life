import pygame
from abc import ABC, abstractmethod


class Button(ABC):
    """
    Abstract class for a button.
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

        self.x, self.y = x, y
        self.width, self.height = width, height
        self.func = func
        self.window = window

        self.image = None

        self.load_assets()

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

        self.func()

    @abstractmethod
    def draw(self) -> None:
        """
        Draws the button on the given surface.
        :return: None
        """

        pass
