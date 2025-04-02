from src.services.hardware_interface.base import I2CSetup, SPISetup, UARTSetup
from .base import HardwareInterface
from src.enums.output_communication_type import EOutputCommunicationType
def interface_factory(communication_type: str) -> HardwareInterface:
    try:
        # Convert the string to the OutputCommunicationType enum
        communication_type_enum = EOutputCommunicationType[communication_type.upper()]
    except KeyError:
        raise ValueError(f"Invalid interface type: {communication_type}")
    
    if communication_type_enum == EOutputCommunicationType.RASPBERRY_PI:
        from src.services.hardware_interface.interfaces.raspberrypi_interface import RaspberryPiInterface
        return RaspberryPiInterface()
    elif communication_type_enum == EOutputCommunicationType.DUMMY:
        from src.services.hardware_interface.interfaces.dummy_interface import DummyInterface
        return DummyInterface()
    else:
        raise ValueError(f"Invalid interface type: {communication_type}")
    
def setup_interface(communication_type: str, uart_setup: list[UARTSetup], spi_setup: list[SPISetup], i2c_setup: list[I2CSetup] ) -> HardwareInterface:
    communication_interface =  interface_factory(communication_type)
    communication_interface.setup(uart_setup, spi_setup, i2c_setup)
    return communication_interface