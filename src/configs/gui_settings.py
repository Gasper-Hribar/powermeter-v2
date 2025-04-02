import os
from src.utils.load_config import load_config
from typing import Dict, Any, List, Optional, Tuple
from src.GUI.constants.config import DEFAULT_CONFIG_PATH, OVERRIDE_CONFIG_PATH, DEFAULT_SETTINGS_PATH, OVERRIDE_SETTINGS_PATH

# Load configuration
config: Dict[str, Any] = load_config(DEFAULT_CONFIG_PATH, OVERRIDE_CONFIG_PATH)
settings: Dict[str, Any] = load_config(DEFAULT_SETTINGS_PATH, OVERRIDE_SETTINGS_PATH)

VERSION: str = config["version"]
# HARDWARE_INTERFACE: str = config["general"]["hardware_interface"]
FULLSCREEN: bool = config["general"]["fullscreen_mode"]
ENABLE_CURSOR: bool = config["general"]["enable_cursor"]
LOGO: bool = config["general"]["show_logo"]
REFRESH_RATE: int = 1000 // config["general"]["refresh_rate"]

FONT: str = config["typography"]["fonts"].get("default")
ALTERNATIVE_FONT: str = config["typography"]["fonts"].get("alternative")
FONTSIZES: Dict[str, int] = config["typography"]["fontsizes"]

SCREEN_WIDTH: int = config["general"]["screen_resolution"]["width"]
SCREEN_HEIGHT: int = config["general"]["screen_resolution"]["height"]

WINDOW_HEIGHT: int = config["general"]["window_size"]["height"]
WINDOW_WIDTH: int = config["general"]["window_size"]["width"]
