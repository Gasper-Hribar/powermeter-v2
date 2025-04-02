from src.GUI.constants.config import DEFAULT_SETTINGS_PATH, OVERRIDE_SETTINGS_PATH
import src.configs.gui_settings as gui_settings
from src.utils.load_config import load_config


STEPS = {
    'default': ["1", "0.1", "0.01", "0.001"],
    'default_low': ["0.1", "0.01", "0.001", "0.0001"],
    'default_mid': ["5", "1", "0.1", "0.01"],
    'default_large': ["10", "1", "0.1", "0.01"],
    "default_xlarge": ["100", "10", "1", "0.1"],
    
}

STEPS_DELAY_LINE= {
    'SY89297U': ["1000", "500", "100", "10", "5"],
    'NB6L295': ["5500", "1100", "550", "110", "11"],
    'MCP23S17': ["5000", "1000", "500", "100", "10"],
    'MCP23S17_40NS': ["5000", "1000", "500", "100", "10"],
    "NONE": []
}

def get_steps(max: int) -> list:
    try:
        return STEPS[f"{max}"]
    except KeyError:
        if max < 2:
            return STEPS['default_low']
        
        elif max > 200:
            return STEPS['default_xlarge']
        elif max > 50:
            return STEPS['default_large']
        elif max > 10:
            return STEPS['default_mid']
        
        return STEPS['default']