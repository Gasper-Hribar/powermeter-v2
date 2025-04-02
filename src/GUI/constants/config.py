# This file contains the paths to the default and override config files, as well as the paths to the default and test excel files

import sys
import os
from src.constants.config import BASE_DIR, SRC_DIR
import src.configs.settings as settings

GUI_PATH = os.path.join(SRC_DIR, "GUI")
DATA_PATH = os.path.join(BASE_DIR, "data") # TODO move to configs somwhere src/configs/config.yaml & config.default.yaml
ROUTINES_PATH = os.path.join(SRC_DIR, "configs", "routines", "routine.yaml") # TODO make this more agile


DEFAULT_CONFIG_PATH =  os.path.join(SRC_DIR, 'configs', 'gui_config.default.yaml')
# DEFAULT_CONFIG_PATH = os.'src/GUI/configs/config.default.yaml')

OVERRIDE_CONFIG_PATH = os.path.join(SRC_DIR, 'configs', 'gui_config.yaml')
DEFAULT_SETTINGS_PATH = os.path.join(SRC_DIR, 'configs', 'gui_settings.default.yaml')
OVERRIDE_SETTINGS_PATH = os.path.join(SRC_DIR, 'configs', 'gui_settings.yaml')

GENERAL_ICON_PATH = os.path.join(GUI_PATH, 'Icons')