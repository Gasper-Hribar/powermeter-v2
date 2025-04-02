from PySide6.QtCore import (QSize)
from PySide6.QtGui import (QFont, QIcon)
from PySide6.QtWidgets import (QPushButton)

from src.GUI.constants.ui_colors import *
from src.GUI.constants.ui_fonts import *
from src.GUI.constants.ui_geometry import *
from src.utils.logger import get_logger


logger = get_logger("GUI")  # type: ignore


class MenuButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set button text and icon
        

    def configure(self, name: str = "", text: str = "Menu Button", icon_path: str = "", bg: str = C_overview_background, fg: str = C_text_light, font: str = "Lato", font_size: int = 12, font_bold: bool = False):
        
        self.setText("   "+text)
        try:
            self.setIcon(QIcon(icon_path))  # Load the icon from the specified file
            self.setIconSize(QSize(MENU_BUTTON_HEIGHT, MENU_BUTTON_HEIGHT))  # Size of the icon (adjust as needed)
        except Exception as e:
            print(f"Error loading icon: {e}")
        
        
        if not name == "":
            self.setObjectName(name)

                
        # Style the button
        self.setFont(QFont(font, font_size, QFont.Weight.Bold if font_bold else QFont.Weight.Normal))
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {fg};
                border: 0px solid transparent;
                text-align: center; /* Align text to the left */
                padding-left: 5px; /* Add spacing between icon and text */
            }}
        """)
        self.setFixedSize(MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)  # Set button size