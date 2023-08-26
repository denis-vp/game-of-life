import pygame

from src.game import Game
import src.constant.constant as const


def start(data_dir_path: str, assets_dir_path: str) -> None:
    pygame.init()
    game = Game(const.WIDTH, const.HEIGHT, const.TITLE, const.FPS, data_dir_path, assets_dir_path, const.LEVELS)
    game.run()
