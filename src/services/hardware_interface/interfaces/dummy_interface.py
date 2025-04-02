
import logging
from src.enums.gpio_directions import EGPIO_Direction
from src.services.hardware_interface.base import I2CSetup, HardwareInterface, SPISetup, UARTSetup
from src.utils.logger import get_logger

logger = get_logger()

class DummyInterface(HardwareInterface):
    _data_rx = ""
    _data_tx = ""
    _is_rx_data_available = False
    _is_tx_data_available = False

    def setup(self, uart_setup: list[UARTSetup], spi_setup: list[SPISetup], i2c_setup: list[I2CSetup]):
        logger.info("SPI, UART, and I2C setup complete.")

    def send_SPI_data(self, spi_name:str, data: list[int]):
        logger.info(f"Sending SPI data: {data} on port {spi_name}")


    def send_and_receive_SPI_data(self, spi_name:str, data:list[int]) -> list[int]:
        logger.info(f"Sending and receiving SPI data: {data} on port {spi_name}")
        return [0, 0, 0, 0]

    def SPI_change_settings(self, spi_name:str, frequency: int, mode: int):
        logger.info(f"Changing SPI settings on port {spi_name} to frequency {frequency} and mode {mode}")

    def send_UART_data(self, uart_name: str, data: str, *args, **kwargs):
        logger.info(f"Sending UART data: {data} on port {uart_name}")
        self._data_tx = data
        self._is_tx_data_available = True
    def send_UART_byte_data(self, uart_name: str, data: bytes):
        logger.info(f"Sending UART byte data: {data} on port {uart_name}")

    def receive_UART_data(self, uart_name: str, *args, **kwargs ) -> str:
        if self._data_rx:
            data = self._data_rx
            self._is_rx_data_available = False
        else:
            data = "Dummy Data"
        logger.info(f"Receiving UART data on port {uart_name}")
        return data
    
    def receive_UART_byte_data(self, uart_name: str, number_of_bytes: int, timeout: float) -> bytes:
        logger.info(f"Receiving UART byte data on port {uart_name}")
        dummy_data = bytes([0] * number_of_bytes)
        return dummy_data

    def set_uart_dummy_data_for_rx(self, data: str):
        self._data_rx = data
        self._is_rx_data_available = True

    def get_uart_dummy_data_from_tx(self) -> str:
        if self._is_tx_data_available:
            self._is_tx_data_available = False
            return self._data_tx
        return ""

    def is_UART_data_available(self, uart_name: str) -> bool:
        logger.info(f"Checking if UART data is available on port {uart_name}")
        return self._is_rx_data_available

    def send_I2C_data(self, i2c_name: str,i2c_address: int, register: int, data: list[int]):
        logger.info(f"Sending I2C data: {data} on bus {i2c_name} and register {register}")
    
    def receive_I2C_data(self, i2c_name:str,i2c_address: int, register: int, length: int) -> list[int]:
        logger.info(f"Receiving I2C data from address {i2c_name} and register {register}")
        return [0] * length

    def send_I2C_byte_data(self, i2c_name:str,i2c_address: int, register: int, data: int):
        logger.info(f"Sending I2C byte data: {data} on bus {i2c_name} and register {register}")
    
    def send_I2C_word_data(self, i2c_name:str,i2c_address: int, register: int, data: int):
        logger.info(f"Sending I2C word data: {data} on bus {i2c_name} and register {register}")
    
    def receive_I2C_byte_data(self, i2c_name:str,i2c_address: int, register: int) -> int:
        logger.info(f"Receiving I2C byte data from bus {i2c_name} and register {register}")
        return 0
    
    def receive_I2C_word_data(self, i2c_name:str,i2c_address: int, register: int) -> int:
        logger.info(f"Receiving I2C word data from bus {i2c_name} and register {register}")
        return 0

    def write_gpio(self, pin: int, value: int):
        logger.info(f"Writing value {value} to GPIO pin {pin}")

    def read_gpio(self, pin: int) -> int:
        logger.info(f"Reading value from GPIO pin {pin}")
        return 0

    def setup_gpio(self, pin: int, direction: EGPIO_Direction):
        logger.info(f"Setting up GPIO pin {pin} as {direction}")
    
    def cleanup(self):
        logger.info("Cleaning up DummyInterface")