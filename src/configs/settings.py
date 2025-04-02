import os
from src.constants.config import DATA_PATH
from src.services.hardware_interface.base import I2CSetup, SPISetup, UARTSetup
from src.utils.load_config import load_config
from src.utils.logger import get_logger_level
from collections.abc import Mapping
from typing import Any, Dict, List, Optional, Tuple

# Load configuration
config: Dict[str, Any] = load_config()

# GENERAL
LOGGING_LEVEL: int = get_logger_level(config["general"].get("logging_level", "INFO"))
HARDWARE_INTERFACE: str = config["general"].get("hardware_interface")
RUN_TIMER: bool = config["general"].get("run_timer", True)
INCLUDED_ROUTINES: List[str] = config["general"].get("included_routines", [])
# API
API_USE_API: bool = config["general"].get("api").get("use_api", False)
API_PORT: int = config["general"].get("api").get("port", 8000)
API_HOST: str = config["general"].get("api").get("host", "0.0.0.0")

# API_RS232
API_RS232_USE_API: bool = config["general"].get("api_rs232").get("use_api", False)
API_RS232_COMMUNICATION_NAME: str = config["general"].get("api_rs232").get("communication_name", "")
API_RS232_SIMULATE_RS232: bool = config["general"].get("api_rs232").get("simulate", False)

DRIVERS: Dict[str, Any] = config["general"].get("drivers", None)
HS_DRIVER: Dict[str, Any] = DRIVERS.get("hs_driver", None)
INTERFACE_CHAIN_DRIVER: Dict[str, Any] = DRIVERS.get("interface_chain_driver", None)

# Extract 'args' and 'kwargs' from hs_driver if they exist
HS_DRIVER_NAME: str = HS_DRIVER.get("name", "") if HS_DRIVER else ""
HS_DRIVER_COMMUNICATION_NAME: str = HS_DRIVER.get("communication_interface", "").get("name", "") if HS_DRIVER else ""
HS_DRIVER_SLOAD_PIN: int = HS_DRIVER.get("sload_pin", 0) if HS_DRIVER else 0
HS_DRIVER_ARGS: List[Any] = HS_DRIVER.get("args", []) if HS_DRIVER else []
HS_DRIVER_KWARGS: Dict[str, Any] = HS_DRIVER.get("kwargs", {}) if HS_DRIVER else {}

# Extract 'args' and 'kwargs' from interface_chain_driver if they exist
INTERFACE_CHAIN_DRIVER_NAME: str = INTERFACE_CHAIN_DRIVER.get("name", "")
INTERFACE_CHAIN_LEGACY_DRIVER: bool = INTERFACE_CHAIN_DRIVER.get("use_legacy_driver", True)
INTERFACE_CHAIN_DRIVER_COMMUNICATION_NAME: str = INTERFACE_CHAIN_DRIVER.get("communication_interface", "").get("name", "") if INTERFACE_CHAIN_DRIVER else ""
INTERFACE_CHAIN_DRIVER_ARGS: List[Any] = INTERFACE_CHAIN_DRIVER.get("args", [])
INTERFACE_CHAIN_DRIVER_KWARGS: Dict[str, Any] = INTERFACE_CHAIN_DRIVER.get("kwargs", {})
INTERFACE_CHAIN_DRIVER_NAMES_TO_EXCEL: List[str] = INTERFACE_CHAIN_DRIVER.get("interface_names", [])
INTERFACE_CHAIN_DRIVER_PATH_TO_EXCEL = [os.path.join(DATA_PATH, excel) for excel in INTERFACE_CHAIN_DRIVER_NAMES_TO_EXCEL]

#Extract FLC Mini configuration
FLC_MINI: Optional[Dict[str, Any]] = DRIVERS.get("flc_mini_driver")
FLC_MINI_COMMUNICATION: Optional[Dict[str, Any]] = FLC_MINI.get("communication_interface")  # type: ignore
# Parse UART configurations
UART_CONFIGS: List[UARTSetup] = [UARTSetup(**uart) for uart in config.get("uart", [])]

# Parse SPI configurations
SPI_CONFIGS: List[SPISetup] = [SPISetup(**spi) for spi in config.get("spi", [])]

# Parse I2C configurations
I2C_CONFIGS: List[I2CSetup] = [I2CSetup(**i2c) for i2c in config.get("i2c", [])]