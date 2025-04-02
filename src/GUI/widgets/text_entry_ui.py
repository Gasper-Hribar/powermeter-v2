from PySide6.QtCore import (Qt)
from PySide6.QtGui import (QFont, QIntValidator)
from PySide6.QtWidgets import (QLineEdit)
from src.GUI.utils.bound_min_max import bound_min_max
from src.GUI.constants.ui_colors import *
from src.GUI.constants.ui_fonts import *
from src.GUI.constants.ui_geometry import *
from src.utils.logger import get_logger


logger = get_logger("GUI")  # type: ignore


class TextEntry(QLineEdit):

    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setPlaceholderText('Enter text')  # Placeholder text



    def configure(self, name: str = "", default_value: str = "Enter Text", unit: str = "", posX: int = 0, posY: int = 0, width: int = TEXT_ENTRY_WIDTH, height: int = TEXT_ENTRY_HEIGHT, bg: str = C_main_background, fg: str = C_text_dark, border: int = 2, border_color: str = C_button_off, border_radius: int = TEXT_ENTRY_HEIGHT//4, font: str = fontfamily, font_size: int = fontsize_normal, font_bold: bool = False,  edit_enabled: bool = True, numerical: bool = True, set_min: float = 0, set_max: float = 10000000000):
        """
        Configures the text entry with the specified properties.
        Args:
            default_value (str): The default text to display in the text entry. Defaults to "Enter Text".
            posX (int): The x-coordinate of the text entry's position. Defaults to 0.
            posY (int): The y-coordinate of the text entry's position. Defaults to 0.
            edit_enabled (bool): Whether the text entry should be editable. Defaults to True.
            numerical (bool): Whether the text entry should only accept numerical (float) input. Defaults to True.
            width (int): The width of the text entry. Defaults to 100.
            height (int): The height of the text entry. Defaults to 25.
            font (str): The font family to use for the text entry. Defaults to "Lato".
            font_size (int): The font size to use for the text entry. Defaults to 10.
            font_bold (bool): Whether the text should be bold. Defaults to False.
            set_min (int): The minimum value that the text entry can accept. Defaults to 0.
            set_max (int): The maximum value that the text entry can accept. Defaults to 10.
        """
        self.unit = unit
        self.amplification = 1.0

        if edit_enabled:
            self.setReadOnly(False)
            self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        else:
            self.setReadOnly(True)
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        if numerical:
            self.setValidator(QIntValidator())
            self.numerical = numerical
            self.min = set_min
            self.max = set_max
        
        self.move(posX, posY)
        self.setFixedSize(width, height)
        if not name == "":
            self.setObjectName(name)

        set_font = QFont()
        set_font.setFamilies([font])
        set_font.setPointSize(font_size)
        set_font.setBold(font_bold)
        self.setFont(set_font)
        self.setText(f"{default_value} {self.unit}")

        
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet(f"""
                            QLineEdit {{
                            background-color: {bg};  /* Default background */
                            color: {fg};             /* Text color */
                            border-radius: {border_radius}px;         /* Rounded corners */
                            border: {border}px solid {border_color};  /* Gray border */
                            padding: 0px;               /* Padding around the text */
                            }}  
                            """)
        
        self.textChanged.connect(self._on_confirm)

    def _on_confirm(self):
        pass

    def get_value(self):
        value = self.text()
        value = value.split(" ")[0]
        return float(value)
    
    def set_min(self, value: float):
        self.min = value

    def set_max(self, value: float):
        self.max = value

    def set_amplification(self, amp: float):
        # print(f"setting amp: {amp}") 
        self.amplification = amp
    
    def set_unit_prefix(self, prefix: str):
        self.unit = f"{prefix}{self.unit[-1]}"

    def get_amplification(self):
        return self.amplification
        
    def set_value(self, value: float = 0.000, text: str = "", powermeter: bool = False):
        if self.numerical:
            value = bound_min_max(value, self.min, self.max)
            value *= self.amplification
            
            self.setText(f"{value:.3f} {self.unit}")
        else:
            self.setText(text)
