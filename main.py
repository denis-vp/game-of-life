import os

from src.start import start


DATA_DIR_PATH = os.path.join(os.path.dirname(__file__), 'data')
ASSETS_DIR_PATH = os.path.join(os.path.dirname(__file__), 'assets')


if __name__ == '__main__':
    start(DATA_DIR_PATH, ASSETS_DIR_PATH)
