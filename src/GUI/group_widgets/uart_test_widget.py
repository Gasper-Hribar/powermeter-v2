from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QCheckBox)
from PySide6.QtCore import Slot, QTimer, QEvent, Qt
from PySide6.QtGui import QKeyEvent
import logging

from src.services.hardware_interface.testing.uart import UARTTestManager

class UARTTestWidget(QDialog):
    def __init__(self, hardware_interface, uart_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("UART Testing")
        self.setMinimumSize(500, 400)

        # Create layouts
        main_layout = QVBoxLayout()
        send_layout = QHBoxLayout()
        
        # Send message components
        self.send_input = QLineEdit()
        self.send_input.setPlaceholderText("Enter message to send")
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        send_layout.addWidget(self.send_input)
        send_layout.addWidget(send_button)

        # Message log
        self.message_log = QTextEdit()
        self.message_log.setReadOnly(True)

        # Command history
        self.command_history = []
        self.history_index = -1

        # Add components to main layout
        main_layout.addLayout(send_layout)
        main_layout.addWidget(self.message_log)

        # Set layout
        self.setLayout(main_layout)

        # Setup UART test manager
        self.uart_test_manager = UARTTestManager(
            hardware_interface, 
            uart_name
        )
        
        # Setup logging
        self.logger = logging.getLogger(__name__)

        # Start testing thread
        self.uart_test_manager.start_testing()

        # Setup periodic message checking
        self.check_message_timer = QTimer()
        self.check_message_timer.timeout.connect(self.check_messages)
        self.check_message_timer.start(500)  # Check every 500ms

        # Install event filter to handle up/down arrow keys
        self.send_input.installEventFilter(self)
    
    def eventFilter(self, arg__1, arg__2):
        """
        Handle up/down arrow keys for command history navigation
        """
        if arg__1 == self.send_input:
            if arg__2.type() == QEvent.Type.KeyPress:
                # Direct key event extraction for PySide6
                if isinstance(arg__2, QKeyEvent):

                    key = arg__2.key()
                    # Up Arrow - go back in history
                    # Up Arrow - go back in history (to older commands)
                    if key == Qt.Key.Key_Up:
                        if self.command_history and self.history_index < len(self.command_history) - 1:
                            self.history_index += 1
                            self.send_input.setText(self.command_history[-self.history_index - 1])
                        return True
                    
                    # Down Arrow - go forward in history (to more recent commands)
                    elif key == Qt.Key.Key_Down:
                        self.history_index -= 1
                        if self.history_index >= 0:
                            self.send_input.setText(self.command_history[-self.history_index - 1])
                        else:
                            self.send_input.clear()
                            self.history_index = -1
                        return True
        
        return super().eventFilter(arg__1, arg__2)
    @Slot()
    def send_message(self):
        """Send a message via UART"""
        message = self.send_input.text()
        if message:
            # Add to command history
            self.command_history.append(message)
            self.history_index = -1

            self.uart_test_manager.send_message(message)
            self.log_message(f"Sent: {message}")
            self.send_input.clear()

    @Slot()
    def check_messages(self):
        """Check for incoming messages"""
        # Check for received messages
        message = self.uart_test_manager.receive_message()
        if message:
            self.log_message(f"Received: {message}")

        # Auto-simulate if checkbox is checked
        self.uart_test_manager._simulate_receive()

    def log_message(self, message):
        """Log message to the text area"""
        current_log = self.message_log.toPlainText()
        updated_log = f"{current_log}\n{message}" if current_log else message
        self.message_log.setPlainText(updated_log)
        # Scroll to bottom
        self.message_log.verticalScrollBar().setValue(
            self.message_log.verticalScrollBar().maximum()
        )

    def closeEvent(self, arg__1):
        """Ensure testing thread is stopped when widget is closed"""
        self.uart_test_manager.stop_testing()
        arg__1.accept()