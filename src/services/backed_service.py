from src.services.hardware_interface.base import HardwareInterface
import src.configs.settings as settings
from src.services.hardware_interface.setup_interface import setup_interface
from src.decorators.singleton import singleton
from numpy import uint32

@singleton
class BackendService():
    
    hi: HardwareInterface

    def __init__(self):
        self.hi = setup_interface(settings.HARDWARE_INTERFACE, settings.UART_CONFIGS, settings.SPI_CONFIGS, settings.I2C_CONFIGS)

backend_service = BackendService()