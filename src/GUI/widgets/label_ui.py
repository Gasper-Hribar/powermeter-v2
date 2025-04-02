from PySide6.QtCore import (Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QLabel, QWidget)
from src.GUI.constants.ui_colors import *
from src.GUI.constants.ui_fonts import *
from src.GUI.constants.ui_geometry import *
from src.utils.logger import get_logger


logger = get_logger("GUI")  # type: ignore

class Label(QLabel):
    
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        # self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")

    def configure(self, name: str = "", text: str = "EmptyLabel", posX: int = 0, posY: int = 0, width: int = LABEL_WIDTH, height: int = LABEL_HEIGHT, bg: str = "transparent", fg: str = C_text_dark, border_radius: int = 4, border_color: str = "transparent", border: int = 0, font: str = fontfamily, font_size: int = fontsize_small, font_bold: bool = False, alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter):
        """
        Configures the label with the specified properties.
        Args:
            text (str): The text to display on the label. Defaults to "EmptyLabel".
            posX (int): The x-coordinate of the label's position. Defaults to 0.
            posY (int): The y-coordinate of the label's position. Defaults to 0.
            width (int): The width of the label. Defaults to 100.
            height (int): The height of the label. Defaults to 25.
            bg (str): The background color of the label. Defaults to UI_LIGHT_GRAY.
            fg (str): The foreground (text) color of the label. Defaults to UI_BLACK.
            font (str): The font family of the label. Defaults to "Lato".
            font_size (int): The font size of the label. Defaults to 10.
            font_bold (bool): The font weight of the label. Defaults to False.
            alignment (Qt.AlignmentFlag): The alignment of the text in the label. Defaults to AlignCenter.
        """
        
        while text[-1] == " ":
            text = text[:-1]

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

        self.setAlignment(alignment)


        self.setStyleSheet(f"""
                            QLabel {{
                                background-color: {bg};
                                color: {fg};
                                border-radius: {border_radius}px;
                                padding: 0px;
                                border: {border}px solid {border_color};
                            }}
                            """)

    def set_text(self, text):
        self.setText(text)
        self.update()
    
    def set_text_color(self, color: str):
        self.setStyleSheet(f"""
                            #{self.objectName()} {{
                            color: {color};
                            }}
                           """)

    def get_value(self):
        return self.text()