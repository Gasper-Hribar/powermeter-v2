
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC_DIR = os.path.join(BASE_DIR, "src")
DEFAULT_CONFIG_PATH = 'src/configs/config.default.yaml'
OVERRIDE_CONFIG_PATH = 'src/configs/config.yaml'
LOG_DIR = "logs"
DATA_PATH = "data"