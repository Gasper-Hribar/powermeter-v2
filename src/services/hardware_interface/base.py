# This is a base class for all output communication services.
# It provides a common interface for all output communication services.
# The output communication services are responsible for sending the output
from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.enums.gpio_directions import EGPIO_Direction

@dataclass
class UARTSetup:
    port: str
    baud_rate: int
    timeout: int
    name: str

@dataclass
class SPISetup:
    bus: int | str
    device: int
    frequency: int
    mode: int
    name: str
    
@dataclass
class I2CSetup:
    bus: int | str
    name: str

class HardwareInterface(ABC):

    
    def __del__(self):
        self.cleanup()

    @abstractmethod
    def setup(self,uart_setup: list[UARTSetup], spi_setup: list[SPISetup], i2c_setup: list[I2CSetup]):
        pass
    
    @abstractmethod
    def send_SPI_data(self, spi_name: str, data:  list[int]):
        pass
    
    @abstractmethod
    def send_and_receive_SPI_data(self, spi_name: str, data: list[int]) -> list[int]:
        pass
    @abstractmethod
    def SPI_change_settings(self, spi_name: str, frequency: int, mode: int):
        pass

    @abstractmethod
    def is_UART_data_available(self, uart_name: str) -> bool:
        pass

    @abstractmethod
    def send_UART_data(self, uart_name: str, data: str, *args, **kwargs):
        pass
    
    @abstractmethod
    def send_UART_byte_data(self, uart_name: str, data: bytes):
        pass

    @abstractmethod
    def receive_UART_data(self, uart_name: str, *args, **kwargs) -> str:
        pass
    
    @abstractmethod
    def send_I2C_data(self, i2c_name:str,i2c_address: int, register:int , data: list[int]):
        pass
    
    @abstractmethod
    def receive_UART_byte_data(self, uart_name: str, number_of_bytes: int, timeout: float) -> bytes:
        pass

    @abstractmethod
    def receive_I2C_data(self, i2c_name:str,i2c_address: int, register:int, length: int) -> list[int]:
        pass

    @abstractmethod
    def send_I2C_byte_data(self, i2c_name:str, i2c_address: int,register: int, data: int):
        pass
    
    @abstractmethod
    def send_I2C_word_data(self, i2c_name:str, i2c_address: int,register: int, data: int):
        pass

    @abstractmethod
    def receive_I2C_byte_data(self, i2c_name:str,i2c_address: int, register: int) ->int:
        pass
    
    @abstractmethod
    def receive_I2C_word_data(self, i2c_name:str, i2c_address: int,register: int) ->int:
        pass

    @abstractmethod
    def write_gpio(self, pin: int, value: int):
        pass

    @abstractmethod
    def read_gpio(self, pin: int) -> int:
        pass

    @abstractmethod
    def setup_gpio(self, pin: int, direction: EGPIO_Direction):
        pass

    @abstractmethod
    def cleanup(self):
        pass