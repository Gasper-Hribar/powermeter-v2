from PySide6.QtWidgets import QWidget, QTextEdit
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from src.GUI.constants.ui_colors import *
from src.GUI.constants.ui_fonts import *
from src.GUI.constants.ui_geometry import *
from src.utils.logger import get_logger


class ConsoleOutput(QTextEdit):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setObjectName("ConsoleOutput")
        self.setReadOnly(True)
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.max_lines = 100
        self.current_line = 0
        
    def configure(self, name: str = "", width: int = SAFETY_CONSOLE_WIDTH, height: int = SAFETY_CONSOLE_HEIGHT, bg: str = C_main_background, fg: str = C_text_dark, font: str = fontfamily, font_size: int = fontsize_normal, font_bold: bool = False):
        
        if not name == "":
            self.setObjectName(name)
        self.setFixedSize(width, height)
        self.setFont(QFont(font, font_size, font_bold))
        self.setStyleSheet(f"""
                            #ConsoleOutput {{
                            background-color: {bg}
                            }}
                            QScrollBar:vertical {{
                                border: none;
                                background: transparent;  /* Scrollbar background */
                                width: 10px;
                                margin: 0px 0px 0px 0px;
                            }}

                            QScrollBar::handle:vertical {{
                                background: {C_button_off}; /* Handle color */
                                min-height: 20px;
                                border-radius: 5px; /* Rounded handle */
                            }}

                            QScrollBar::handle:vertical:hover {{
                                background: #aaaaaa; /* Hover effect */
                            }}

                            QScrollBar::sub-line:vertical,
                            QScrollBar::add-line:vertical {{
                                background: none; /* Remove up and down arrow buttons */
                                height: 0px;
                            }}

                            QScrollBar::add-page:vertical,
                            QScrollBar::sub-page:vertical {{
                                background: none; /* Transparent area above and below handle */
                            }}

                            QScrollBar:horizontal {{
                                border: none;
                                background: transparent;
                                height: 10px;
                                margin: 0px 0px 0px 0px;
                            }}

                            QScrollBar::handle:horizontal {{
                                background: {C_button_off};
                                min-width: 20px;
                                border-radius: 5px;
                            }}

                            QScrollBar::handle:horizontal:hover {{
                                background: #aaaaaa;
                            }}

                            QScrollBar::sub-line:horizontal,
                            QScrollBar::add-line:horizontal {{
                                background: none;
                                width: 0px;
                            }}

                            QScrollBar::add-page:horizontal,
                            QScrollBar::sub-page:horizontal {{
                                background: none;
                            }}
                            """)
        
    def log(self, message: str):
        self.append(message)
        self.current_line += 1
        if self.current_line > self.max_lines:
            self.clear_console()
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def clear_console(self):
        self.current_line = 0
        self.clear()