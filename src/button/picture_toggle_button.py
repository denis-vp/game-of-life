import pygame

from src.button.toggle_button import ToggleButton


class PicturePushButton(ToggleButton):
    """
    A toggle button with a picture.
    """

    def __init__(self, x: int, y: int, width: int, height: int,
                 func: callable, window: pygame.Surface,
                 image_path: str, image_toggled_path) -> None:
        """
        :param x: int, the x position of the button.
        :param y: int, the width of the button.
        :param width: int, the width of the button.
        :param height: int, the height of the button.
        :param func: int, the function to be called when the button is clicked.
        :param image_path: str, the path to the button's image.
        :param image_toggled_path: str, the path to the button's toggled image.
        """

        self.image_path = image_path
        self.image_toggled_path = image_toggled_path

        super().__init__(x, y, width, height, func, window)

    def load_assets(self) -> None:
        """
        Loads the button's assets.
        :return: None
        """

        self.image = pygame.image.load(self.image_path)
        self.image_toggled = pygame.image.load(self.image_toggled_path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image_toggled = pygame.transform.scale(self.image_toggled, (self.width, self.height))
