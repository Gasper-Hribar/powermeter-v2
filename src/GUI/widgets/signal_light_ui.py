from PySide6.QtCore import (QSize, Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QRadioButton, QWidget)
from src.GUI.constants.ui_colors import *
from src.GUI.constants.ui_fonts import *
from src.GUI.constants.ui_geometry import *
from src.utils.logger import get_logger


logger = get_logger("GUI")  # type: ignore

class SignalLight(QRadioButton):

    
    def __init__(self, parent: QWidget, port_number: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName(u"signalLight")
        self.setParent(parent)
        
        self.port_number = port_number

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
    def configure(self, name: str = "", text: str = "SignalLight", fg: str = C_text_dark, posX: int = 0, posY: int = 0, width: int = SIGNAL_LIGHT_WIDTH, height: int = SIGNAL_LIGHT_HEIGHT, unchecked_color: str = "transparent", checked_color: str = C_button_on, font: str = fontfamily, font_size: int = fontsize_small, font_bold: bool = True):
        """
        Configures the radio button with the specified properties.
        Args:
            text (str): The text to display on the radio button. Defaults to "SignalLight".
            posX (int): The x-coordinate of the radio button's position. Defaults to 0.
            posY (int): The y-coordinate of the radio button's position. Defaults to 0.
            width (int): The width of the radio button. Defaults to 100.
            height (int): The height of the radio button. Defaults to 30.
        """
        if len(text) > 11:
            text = text[:9] + "..."

        self.setText(text)
        self.setFixedSize(width, height)
        self.move(posX, posY)

        if not name == "":
            self.setObjectName(name)
        
        set_font = QFont()
        set_font.setFamilies([font])
        set_font.setPointSize(font_size)
        set_font.setBold(font_bold)
        self.setFont(set_font)
        self.setEnabled(False)
        self.setAutoExclusive(False)  # Allow independent toggling


        self.setStyleSheet(f"""
                            QRadioButton {{
                            background-color: transparent;  /* Default background */
                            color: {fg};            /* Text color */
                            height: {width}px;               /* Height of the checkbox */
                            width: {height}px;                /* Width of the checkbox */
                            border: 0px solid; /* Optional border */
                            border-radius: 4px;
                            padding: 0px;
                            }}

                            QRadioButton:checked {{
                            color: {checked_color};
                            }}

                            QRadioButton::indicator {{
                            width: {height//4}px;  /* Total size of the button */
                            height: {height//4}px;
                            border: {height//4}px solid {unchecked_color};  /* Gray border */
                            border-radius: {height//3}px;  /* Make it a perfect circle */
                            background-color: transparent;  /* White inner part */
                            margin: 2px;  /* Ensures proper spacing */
                            }}
                            
                            QRadioButton::indicator:checked {{
                            width: {height//4}px;  /* Total size of the button */
                            height: {height//4}px;
                            border: {height//4}px solid {checked_color};  /* Gray border */
                            border-radius: {height//3}px;  /* Make it a perfect circle */
                            background-color: transparent;  /* Red inside when checked */
                            background-clip: content-box;  /* Keeps inner content white */
                            }}
                            """)
        
        self.setIconSize(QSize(height, height))

        
    def set_state(self, state: bool):
        self.setChecked(state)
        self.update()

    def set_text(self, text: str):
        self.setText(text)
        self.update()
    
    def get_state(self) -> bool:
        return self.isChecked()
    
    def get_port_number(self) -> int:
        return self.port_number
    
    def get_name(self) -> str:
        return self.objectName()

        