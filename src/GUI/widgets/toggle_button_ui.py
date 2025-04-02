from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QPushButton, QWidget)
from src.GUI.constants.ui_colors import *
from src.GUI.constants.ui_fonts import *
from src.GUI.constants.ui_geometry import *
from src.utils.logger import get_logger


logger = get_logger("GUI")  # type: ignore


"""
Button class definition and configuration methods.

"""

class ToggleButton(QPushButton):
    num = 0

    def __init__(self, parent: QWidget, port_number: int=-1,*args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName(u"pushButton")
        self.setParent(parent)
        self.port_number = port_number

        self.default_style = self._default_style()
        self.checked_style = self._checked_style()

        self.setCheckable(True)
        self.setStyleSheet(self.default_style)
        self.toggled.connect(self._on_toggle)

        self.setDefault(True)
        ToggleButton.num += 1


    def configure(self, name:str = "", text: str = f"ToggleButton", bg: str = C_button_off, fg: str = C_text_dark, active_bg: str = C_button_on, active_fg: str = C_text_light, posX: int = 0, posY: int = 0, width: int = BUTTON_WIDTH, height: int = BUTTON_HEIGHT, border_radius: int = BUTTON_HEIGHT//2, padding: int = 0, font: str = fontfamily, font_size: int = fontsize_normal, font_bold: bool = False, limit_len = True):
        """
        Configures the button with the specified properties.
        Args:
            text (str): The text to display on the button. Defaults to "ToggleButton".
            bg (str): The background color of the button in its default state. Defaults to UI_LIGHT_GRAY.
            fg (str): The foreground (text) color of the button in its default state. Defaults to UI_BLACK.
            active_bg (str): The background color of the button when it is checked. Defaults to UI_ORANGE.
            active_fg (str): The foreground (text) color of the button when it is checked. Defaults to UI_BLACK.
            posX (int): The x-coordinate of the button's position. Defaults to 0.
            posY (int): The y-coordinate of the button's position. Defaults to 0.
            width (int): The width of the button. Defaults to 100.
            height (int): The height of the button. Defaults to 25.
        """
        if text == "ToggleButton":
            text = f"ToggleButton_{ToggleButton.num}"
        
        
        if not name == "":
            self.setObjectName(name)

        if limit_len:
            if len(text) > 14:
                text = text[:14]

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
            }}
            QPushButton:pressed {{
                background-color: {active_bg};
                color: {active_fg};
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
                background-color: {active_bg};
                color: {active_fg};
                border-radius: {border_radius}px;
                padding: {padding}px;
            }}
            """

        self.setText(text)
        self.setFixedSize(width, height)
        self.move(posX, posY)
        
        set_font = QFont()
        set_font.setFamilies([font])
        set_font.setPointSize(font_size)
        set_font.setBold(font_bold)
        self.setFont(set_font)
        

    def _on_toggle(self, checked):
        if checked:
            self.setStyleSheet(self.checked_style)
        else:
            self.setStyleSheet(self.default_style)

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
    
    def set_callback(self, callback, *args, **kwargs):
        """
        Assign a callback function to the button.
        Args:
            callback (function): The function to be called when the button is clicked.
        """
        if callable(callback):
            self.callback = callback
            try:
                self.clicked.connect(lambda: self.callback(*args, **kwargs, state=self.isChecked()))
                
            except Exception as e:
                self.clicked.connect(callback)
                print(f"Catched exception: {e}")
    
        else:
            raise ValueError("Provided callback is not callable.")
        
    def get_name(self) -> str:
        """
        Get the name of the button.
        Returns:
            str: The name of the button.
        """
        return self.objectName()
    
    def get_port_number(self) -> int:
        """
        Get the port number of the button.
        Returns:
            int: The port number of the button.
        """
        return self.port_number
    
    def get_state(self) -> bool:
        """
        Get the state of the button.
        Returns:
            bool: The state of the button.
        """
        return self.isChecked()
    
    def set_checked(self, state: bool, *args, **kwargs):
        self.setChecked(state)
        try:
            self.callback(*args, **kwargs, state=self.isChecked())
        except TypeError as e:
            self.callback() 
            logger.error(f"{e}")