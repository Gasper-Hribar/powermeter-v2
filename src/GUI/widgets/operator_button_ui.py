from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QPushButton, QWidget)
from src.GUI.constants import ui_operators
from src.GUI.constants.ui_colors import *
from src.GUI.constants.ui_fonts import *
from src.GUI.constants.ui_geometry import *
from src.utils.logger import get_logger


logger = get_logger("GUI")  # type: ignore

"""
Button class definition and configuration methods.

"""

class OperatorButton(QPushButton):


    def __init__(self, parent: QWidget, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName(u"pushButton")
        self.setParent(parent)

        self.default_style = self._default_style()
        self.checked_style = self._checked_style()

        self.setCheckable(False)
        self.setStyleSheet(self.default_style)
        # self.clicked.connect(self._on_click)

        self.setDefault(True)

    def configure(self, operator: str = ui_operators.NOOP, bg: str = C_button_off, fg: str = C_text_dark, checked_bg: str = C_button_on, checked_fg: str = C_text_light, posX: int = 0, posY: int = 0, width: int = OPERATOR_BUTTON_WIDTH, height: int = OPERATOR_BUTTON_HEIGHT, border_radius: int = OPERATOR_BUTTON_HEIGHT//4, padding: int = 0, font: str = "Lato", font_size: int = 10, font_bold: bool = False):
        """
        Configures the operator button with the specified properties.
        Args:
            operator (str): The operator string. Should be a value from ui_operators. Defaults to UI_NOOP.
            bg (str): The background color of the button in its default state. Defaults to UI_LIGHT_GRAY.
            fg (str): The foreground (text) color of the button in its default state. Defaults to UI_BLACK.
            checked_bg (str): The background color of the button when it is checked. Defaults to UI_ORANGE.
            checked_fg (str): The foreground (text) color of the button when it is checked. Defaults to UI_BLACK.
            posX (int): The x-coordinate of the button's position. Defaults to 0.
            posY (int): The y-coordinate of the button's position. Defaults to 0.
            width (int): The width of the button. Defaults to 100.
            height (int): The height of the button. Defaults to 25.
        """

         # Validate width and height
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive integers.")

        # Apply stylesheet
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {fg};
                border-radius: {border_radius}px;
                padding: {padding}px;
                border: 0px solid transparent;
            }}
            QPushButton:pressed {{
                background-color: {checked_bg};
                color: {checked_fg};
            }}
        """)

        self.default_style = f"""
            QPushButton {{
                background-color: {bg};
                color: {fg};
                border-radius: {border_radius}px;
                padding: {padding}px;
            }}
            """
        
        self.checked_style = f"""
            QPushButton {{
                background-color: {checked_bg};
                color: {checked_fg};
                border-radius: {border_radius}px;
                padding: {padding}px;
            }}
            """

        self.setText(operator)
        self.setFixedSize(width, height)
        self.move(posX, posY)
        
        set_font = QFont()
        set_font.setFamilies([font])
        set_font.setPointSize(font_size)
        set_font.setBold(font_bold)
        self.setFont(set_font)

        self._set_active_style(bg, fg, checked_bg, checked_fg, border_radius, padding)
        self._set_disabled_style(UI_LIGHT_GRAY, UI_GRAY, checked_bg, checked_fg, border_radius, padding)

        self.default_style = f"""
            #{self.objectName()} {{
                background-color: {bg};
                color: {fg};
                border-radius: {border_radius}px;
                padding: {padding}px;
            }}
            #{self.objectName()}:pressed {{
                background-color: {checked_bg};
                color: {checked_fg};
            }}
            """
        
    def _set_active_style(self, bg, fg, checked_bg, checked_fg, border_radius, padding):
        self.active_style = f"""
            #{self.objectName()} {{
                background-color: {bg};
                color: {fg};
                border-radius: {border_radius}px;
                padding: {padding}px;
            }}
            #{self.objectName()}:pressed {{
                background-color: {checked_bg};
                color: {checked_fg};
            }}
            """
        
    def _set_disabled_style(self, bg, fg, checked_bg, checked_fg, border_radius, padding):
        self.disabled_style = f"""
            #{self.objectName()} {{
                background-color: {bg};
                color: {fg};
                border-radius: {border_radius}px;
                padding: {padding}px;
            }}
            #{self.objectName()}:pressed {{
                background-color: {checked_bg};
                color: {checked_fg};
            }}
            """

    def _on_click(self):
        print(f"Button {self.text()} clicked.")

    
    def set_enabled(self, enabled: bool):
        self.setEnabled(enabled)
        if enabled:
            self.setStyleSheet(self.active_style)
        else:
            self.setStyleSheet(self.disabled_style)


    def _default_style(self):
        return f"""
                QPushButton {{
                background-color: {C_button_off};  /* Default background */
                color: {C_text_dark};            /* Text color */
                border-radius: 4px;        /* Rounded corners */
                border: none;             /* No border */
                }}
                """

    def _checked_style(self):
        return f"""
                QPushButton {{
                background-color: {C_button_on};  /* Default background */
                color: {C_text_light};            /* Text color */
                border-radius: 4px;        /* Rounded corners */
                border: none;             /* No border */
                }}
                """
    
    def set_callback(self, callback):
        """
        Assign a callback function to the button.
        Args:
            callback (function): The function to be called when the button is clicked.
        """
        if callable(callback):
            self.clicked.connect(callback)
        else:
            raise ValueError("Provided callback is not callable.")
    