from PySide6.QtCore import (Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QCheckBox, QWidget)
from src.GUI.constants.ui_colors import *
from src.GUI.constants.ui_fonts import *
from src.GUI.constants.ui_geometry import *
from src.utils.logger import get_logger


logger = get_logger("GUI")  # type: ignore


class CheckBox(QCheckBox):

    
    def __init__(self, parent: QWidget):
        super().__init__()
        
        self.setObjectName(u"checkBox")
        # self.setParent(parent)

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)


    def configure(self, name: str = "", text: str = "", posX: int = 0, posY: int = 0, width: int = CHECKBOX_WIDTH, height: int = CHECKBOX_HEIGHT, bg: str = "transparent", fg: str = C_text_dark, checked_color: str = C_button_on, unchecked_color: str = C_button_off, font: str = fontfamily, font_size: int = fontsize_small, font_bold: bool = False):
        """
        Configures the checkbox with the specified properties.
        Args:
            text (str): The text to display on the checkbox.
            posX (int): The x-coordinate of the checkbox's position.
            posY (int): The y-coordinate of the checkbox's position.
            width (int): The width of the checkbox.
            height (int): The height of the checkbox.
            font (str): The font family to use for the text.
            font_size (int): The font size to use for the text.
            font_bold (bool): Whether the text should be bold.
        """
        if text == "":
            width = CHECKBOX_HEIGHT
        self.setText(text)
        
        self.setFixedSize(width, height)
        if not name == "":
            self.setObjectName(name)

        set_font = QFont()
        set_font.setFamilies([font])
        set_font.setPointSize(font_size)
        set_font.setBold(font_bold)
        self.setFont(set_font)
        # Customize the style
        self.setStyleSheet(f"""
            QCheckBox {{
                background-color: {bg};  /* Default background */
                color: {fg};             /* Text color */
                height: {height};               /* Height of the checkbox */
                width: {width};                /* Width of the checkbox */
                border-radius: 4px;
                padding: 0px;
            }}            
            QCheckBox::indicator {{
                width: {CHECKBOX_HEIGHT//2}px;  /* Set the size of the tick box */
                height: {CHECKBOX_HEIGHT//2}px;
                border-radius: {CHECKBOX_HEIGHT//4}px;  /* Optional rounding */
            }}
            QCheckBox::indicator:checked {{
                background-color: {checked_color};  /* Green when checked */
                border: {CHECKBOX_HEIGHT//6}px solid {checked_color};  /* Darker green border */
            }}

            QCheckBox::indicator:unchecked {{
                background-color: {bg};  /* White when unchecked */
                border: {CHECKBOX_HEIGHT//6}px solid {unchecked_color};  /* Gray border */
            }}

        """)
        self.setChecked(False)  # Uncheck the box by default

        # Align the text in the center of the box
        self.setTristate(False)  # Ensure it's binary (checked/unchecked)

    def set_callback(self, callback, *args, **kwargs):
        """
        Assign a callback function to the button.
        Args:
            callback (function): The function to be called when the button is clicked.
        """
        if callable(callback):
            try:
                self.pressed.connect(lambda: callback(self.isChecked(), *args, **kwargs))
            except Exception as e:
                self.pressed.connect(callback)
        else:
            raise ValueError("Provided callback is not callable.")