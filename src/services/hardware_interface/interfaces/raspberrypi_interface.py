import platform
from src.services.hardware_interface.base import HardwareInterface, UARTSetup, SPISetup, I2CSetup
from src.enums.gpio_directions import EGPIO_Direction
from src.utils.logger import get_logger
from src.utils.is_rpi import is_raspberry_pi as is_rpi
import time
# Check if running on Raspberry Pi
is_raspberry_pi = is_rpi()
try:
    import lgpio  # type: ignore
    import serial # type: ignore
    import spidev # type: ignore
    import smbus2 # type: ignore
except ImportError:
    raise ImportError("RaspberryPiInterface requires the pyserial, spidev, and smbus libraries.")
    # if is_raspberry_pi:
    #     raise ImportError("RaspberryPiInterface requires the pyserial, spidev, and smbus libraries.")
    # else:
    #     pass
logger = get_logger()

class RaspberryPiInterface(HardwareInterface):

    def __init__(self):
        super().__init__()
        if not is_raspberry_pi:
            raise RuntimeError("RaspberryPiInterface requires Raspberry Pi hardware.")
        
        logger.info("Initialized RaspberryPiInterface")

    def setup(self, uart_setup: list[UARTSetup], spi_setup: list[SPISetup], i2c_setup: list[I2CSetup]):

        
        

        # Initialize UART, SPI, and I2C dictionaries
        self.uart_connections: dict[str, serial.Serial] = {} 
        self.spi_connections:dict[str, spidev.SpiDev] = {} 
        self.i2c_connections: dict[str, smbus2.SMBus] = {} 
        self.gpio_outputs: dict[int, bool] = {}
        self.gpio_inputs: dict[int, bool] = {}
        # Initialize lgpio chip
        self.gpio_chip = lgpio.gpiochip_open(0)  # Open GPIO chip 0
        if self.gpio_chip < 0:
            raise RuntimeError("Failed to open GPIO chip.")
        # UART Setup
        for uart in uart_setup:
            self.uart_connections[uart.name] = serial.Serial(uart.port, uart.baud_rate, timeout=uart.timeout)

        # SPI Setup
        for spi in spi_setup:
            spi_device = spidev.SpiDev() 
            spi_device.open(spi.bus, spi.device)
            spi_device.max_speed_hz = spi.frequency 
            spi_device.mode = spi.mode
            self.spi_connections[spi.name] = spi_device

        # I2C Setup
        for i2c in i2c_setup:
            self.i2c_connections[i2c.name] = smbus2.SMBus(i2c.bus)
        
        
        logger.info("SPI, UART, and I2C setup complete.")


    def setup_gpio(self, pin: int, direction: EGPIO_Direction):
        if direction == EGPIO_Direction.OUTPUT:
            lgpio.gpio_claim_output(self.gpio_chip, pin)  # Set as output
            self.gpio_outputs[pin] = True
        elif direction == EGPIO_Direction.INPUT:
            lgpio.gpio_claim_input(self.gpio_chip, pin)  # Set as input
            self.gpio_inputs[pin] = True
        else:
            raise ValueError("Direction should be 'IN' or 'OUT'.")

    def write_gpio(self, pin: int, value: int):
        if pin in self.gpio_outputs:
            lgpio.gpio_write(self.gpio_chip, pin, value)
            logger.info(f"Writing value {value} to GPIO pin {pin}")
        else:
            raise ValueError(f"GPIO pin {pin} not configured as output.")

    def read_gpio(self, pin: int) -> int:
        # if pin in self.gpio_inputs:
        logger.info(f"Reading value from GPIO pin {pin}")
        return lgpio.gpio_read(self.gpio_chip, pin)
        # else:
        #     raise ValueError(f"GPIO pin {pin} not configured as input.")

    def SPI_change_settings(self, spi_name: str, frequency: int, mode: int):
        spi_device = self.spi_connections.get(spi_name)
        if spi_device:
            spi_device.max_speed_hz = frequency
            spi_device.mode = mode
        
        else:
            raise ValueError(f"SPI port {spi_name} not configured")

    def send_SPI_data(self, spi_name: str, data: list[int] ):
        spi_device = self.spi_connections.get(spi_name)
        if spi_device:
            spi_device.xfer2(data)
        else:
            raise ValueError(f"SPI port {spi_name} not configured")

    def send_and_receive_SPI_data(self, spi_name: str, data: list[int]) -> list[int]:
        spi_device = self.spi_connections.get(spi_name)
        if spi_device:
            return spi_device.xfer2(data)
        else:
            raise ValueError(f"SPI port {spi_name} not configured")

    def send_UART_data(self, uart_name: str, data: str):
        uart_device = self.uart_connections.get(uart_name)
        if uart_device:
            uart_device.write(data.encode())
        else:
            raise ValueError(f"UART port {uart_name} not configured")
        
    def send_UART_byte_data(self, uart_name: str, data: bytes):
        uart_device = self.uart_connections.get(uart_name)
        if uart_device:
            uart_device.write(data)  # Send raw bytes, not encoded string
        else:
            raise ValueError(f"UART port {uart_name} not configured")
        
    def receive_UART_data(self, uart_name: str) -> str:
        uart_device = self.uart_connections.get(uart_name)
        if uart_device:
            return uart_device.readline().decode('utf-8')
        else:
            raise ValueError(f"UART port {uart_name} not configured")
        
    def receive_UART_byte_data(self, uart_name: str, number_of_bytes: int, timeout: float = 1.0) -> bytes:
        """
        Receive UART data as raw binary, with a timeout for incomplete transmissions.
        
        Args:
            uart_name (str): Name of the UART connection.
            number_of_bytes (int): Number of bytes to read.
        
        Returns:
            bytes: Complete raw binary data received from the UART.
        
        Raises:
            ValueError: If the UART port is not configured or invalid number_of_bytes.
            TimeoutError: If the operation times out.
        """
        if number_of_bytes <= 0:
            raise ValueError("number_of_bytes must be a positive integer")

        uart_device = self.uart_connections.get(uart_name)
        if not uart_device:
            raise ValueError(f"UART port {uart_name} not configured")
        
        data = bytearray()
        start_time = time.time()
        while len(data) < number_of_bytes:
            chunk = uart_device.read(1)
            # Adjust chunk size as needed
            if chunk:
                data.extend(chunk)
            if time.time() - start_time > timeout:
                logger.error(f"UART read operation timed out. Try increasing the timeout value.")
                raise TimeoutError("UART read operation timed out")
            # print(len(data)) # remove after testing
        logger.info(f"Received {len(data)} bytes from UART port {uart_name}")
        return bytes(data)

    def is_UART_data_available(self, uart_name: str) -> bool:
        uart_device = self.uart_connections.get(uart_name)
        if uart_device:
            return uart_device.in_waiting > 0
        else:
            raise ValueError(f"UART port {uart_name} not configured")

    def send_I2C_byte_data(self, i2c_name: str, i2c_address:int , register: int, data: int):
        bus = self.i2c_connections.get(i2c_name)
        if bus:
            bus.write_byte_data(i2c_address, register, data)
        else:
            raise ValueError(f"I2C bus {i2c_name} not configured")

    def send_I2C_word_data(self, i2c_name:str, i2c_address: int, register: int, data: int):

        bus = self.i2c_connections.get(i2c_name)
        if bus:
            bus.write_word_data(i2c_address,register, data)
        else:
            raise ValueError(f"I2C bus {i2c_name} not configured")

    def receive_I2C_byte_data(self, i2c_name:str, i2c_address: int, register: int) ->int:

        bus = self.i2c_connections.get(i2c_name)
        if bus:
            return bus.read_byte_data(i2c_address,register)
        else:
            raise ValueError(f"I2C bus {i2c_name} not configured")
    
    def receive_I2C_word_data(self, i2c_name:str, i2c_address: int, register: int) ->int:
        bus = self.i2c_connections.get(i2c_name)
        if bus:
            return bus.read_word_data(i2c_address,register)
        else:
            raise ValueError(f"I2C bus {i2c_name} not configured")

    def send_I2C_data(self, i2c_name:str, i2c_address: int,register: int, data: list[int]):
        bus = self.i2c_connections.get(i2c_name)
        if bus:
            bus.write_i2c_block_data(i2c_address,register, data)
        else:
            raise ValueError(f"I2C bus {i2c_name} not configured")
    
    def receive_I2C_data(self, i2c_name:str,i2c_address: int, register: int, length: int) -> list[int]:
        bus = self.i2c_connections.get(i2c_name)
        if bus:
            return bus.read_i2c_block_data(i2c_address, register, length)
        else:
            raise ValueError(f"I2C bus {i2c_name} not configured")

    def cleanup(self):
        # Close all connections and cleanup GPIO
        try:
            for uart in self.uart_connections.values():
                uart.close()
        except Exception as e:
            logger.error(e)
        try:
            for spi in self.spi_connections.values():
                spi.close()
        except Exception as e:
            logger.error(e)
        try:
            for gpio in self.gpio_outputs.keys():
                self.write_gpio(gpio, 0)
            # Release all claimed GPIO pins and close the chip
            lgpio.gpiochip_close(self.gpio_chip)
        except Exception as e:
            logger.error(e)

if __name__ == "__main__":
    # Test the RaspberryPiInterface class
    interface = RaspberryPiInterface()
    try:
        interface.setup([
            UARTSetup(port="/dev/ttyAMA1", baud_rate=9600, timeout=1, name="uart0"),
            UARTSetup(port="/dev/ttyAMA4", baud_rate=9600, timeout=1, name="uart1"),
        ], [
            SPISetup(bus=0, device=0, frequency=500000, mode=0, name="spi0"),
            SPISetup(bus=1, device=0, frequency=500000, mode=0, name="spi1"),
        ], [
            I2CSetup(bus=1, name="i2c0"),
        ])
        

        # interface.setup_gpio(17, EGPIO_Direction.OUTPUT)
        # interface.write_gpio(17, 1)

        # interface.write_gpio(17, 0)
        
        interface.send_and_receive_SPI_data("spi0", [0x01, 0x02])
        print("SPI0")
        interface.send_and_receive_SPI_data("spi0", [0x01, 0x02])
        print("SPI1")
        interface.send_and_receive_SPI_data("spi1", [0x01, 0x02])
        

        interface.send_UART_data("uart0", "Hello, UART!")
        logger.info(interface.receive_UART_data("uart1"))

        # interface.send_I2C_byte_data("i2c0", 0x02, 0x01, 0x02)
        
    except Exception as e:
        import traceback

        logger.error(e)   
        traceback.print_exc()  # This will print the full traceback of the exception

    finally:
       interface.cleanup()