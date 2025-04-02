
import yaml
import os

from src.constants.config import DEFAULT_CONFIG_PATH, OVERRIDE_CONFIG_PATH

# Function to recursively update default configuration with overrides
def deep_update(source: dict, overrides: dict) -> dict:
    for key, value in overrides.items():
        if isinstance(value, dict) and value:
            source[key] = deep_update(source.get(key, {}), dict(value))  # Ensure `value` is a dict
        else:
            source[key] = value
    return source

# Load configuration from YAML files
def load_config(default_file=DEFAULT_CONFIG_PATH, override_file=OVERRIDE_CONFIG_PATH):
    # Load default config
    with open(default_file, "r") as file:
        config = yaml.safe_load(file) or {}

    # Load override config if it exists
    if os.path.exists(override_file):
        with open(override_file, "r") as file:
            override_config = yaml.safe_load(file) or {}
        config = deep_update(config, override_config)
    
    return config