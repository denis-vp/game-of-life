import pygame

from src.button.push_button import PushButton


class PicturePushButton(PushButton):
    """
    A push button with a picture.
    """

    def __init__(self, x: int, y: int, width: int, height: int,
                 func: callable, window: pygame.Surface,
                 image_path: str, image_hover_path: str, image_click_path: str) -> None:
        """
        :param x: int, the x position of the button.
        :param y: int, the width of the button.
        :param width: int, the width of the button.
        :param height: int, the height of the button.
        :param func: int, the function to be called when the button is clicked.
        :param image_path: str, the path to the button's image.
        :param image_hover_path: str, the path to the button's hover image.
        :param image_click_path: str, the path to the button's animation image.
        """

        self.image_path = image_path
        self.image_hover_path = image_hover_path
        self.image_click_path = image_click_path

        super().__init__(x, y, width, height, func, window)

    def load_assets(self) -> None:
        """
        Loads the button's assets.
        :return: None
        """

        self.image = pygame.image.load(self.image_path)
        self.image_hover = pygame.image.load(self.image_hover_path)
        self.image_click = pygame.image.load(self.image_click_path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image_hover = pygame.transform.scale(self.image_hover, (self.width, self.height))
        self.image_click = pygame.transform.scale(self.image_click, (self.width, self.height))
