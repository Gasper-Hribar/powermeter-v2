import os
from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout, QMainWindow
from PySide6.QtGui import QIcon 
from PySide6.QtCore import Qt, QSize
from src.GUI.UI.widgets.label_ui import Label
from src.GUI.UI.widgets.push_button_ui import PushButton
from src.GUI.constants.ui_colors import *
from src.GUI.constants.ui_geometry import *
from src.GUI.constants.ui_fonts import *
import src.configs.gui_settings as gui_settings
import src.configs.settings as settings
from src.GUI.constants.config import GENERAL_ICON_PATH

# sys.path.append("C:\\Users\\hriba\\Desktop\\FOLAS\\FLC")

fontfamily = gui_settings.FONT
fontsize_normal = gui_settings.FONTSIZES["fontsize_normal"]
fontsize_large = gui_settings.FONTSIZES["fontsize_large"]
fontsize_small = gui_settings.FONTSIZES["fontsize_small"]
version = gui_settings.VERSION
interface = settings.HARDWARE_INTERFACE
general_icon_path = GENERAL_ICON_PATH
show_logo = gui_settings.LOGO

# numpad flags

NUMPAD_NO_UNITS = 0
NUMPAD_ONE_UNIT = 1
NUMPAD_TWO_UNITS = 2
NUMPAD_ONLY_INT_NO_UNIT = 3


class Numpad(QMainWindow):
     
    def __init__(self, callback, value: float, unit: str, units: list[str], parent: QWidget | None = None, width: int = NUMPAD_WIDGET_WIDTH, height: int = NUMPAD_WIDGET_HEIGHT, flag: int = NUMPAD_NO_UNITS):
        super().__init__(parent)

        # Store parameters
        self.callback = callback
        self.init_value = str(value)

        self.unit = unit
        self.units = units
        self.numpad_width = width
        self.numpad_height = height
        self.decimal_count_offset = 0
        self.first_input = True
        screen = get_screen_size()
        self.move(screen[0]//2 - width//2, screen[1]//2 - height//2)

        # Configure main window
        self.setWindowTitle("Set Value")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setFixedSize(self.numpad_width, self.numpad_height)

        # Apply styles
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {C_main_background};
                border-radius: 4px;
                border: 2px solid {C_adc_label_border};
            }}
        """)

        # Central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)
        layout.setSpacing(1)
        layout.setContentsMargins(2, 2, 2, 2)
        # self.history = [char for char in self.init_value] if value != 0 else []
        self.history = []
        # Buttons
        widget_width = int((self.numpad_width - 4 - 4) / 5)
        widget_height = int((self.numpad_height - 3 - 4) / 4)
        
        # Value label
        self.value_label = Label(self)
        self.value_label.configure(
            text=f"{self.init_value} {self.unit}",
            posX=0, posY=0,
            width=self.numpad_width - widget_width, height=widget_height,
            font_size=fontsize_large, bg=C_main_background,
            fg=C_text_dark, font_bold=True
        )
        layout.addWidget(self.value_label, 0, 0, 1, 4)

        self.create_button("_back", layout, 0, 4, self.delete_last, -1, widget_width, widget_height)
        self.create_button("0", layout, 2, 4, self.add_to_value, 0, widget_width, widget_height)
        self.create_button("1", layout, 1, 0, self.add_to_value, 1, widget_width, widget_height)
        self.create_button("2", layout, 1, 1, self.add_to_value, 2, widget_width, widget_height)
        self.create_button("3", layout, 1, 2, self.add_to_value, 3, widget_width, widget_height)
        self.create_button("4", layout, 1, 3, self.add_to_value, 4, widget_width, widget_height)
        self.create_button("5", layout, 1, 4, self.add_to_value, 5, widget_width, widget_height)
        self.create_button("6", layout, 2, 0, self.add_to_value, 6, widget_width, widget_height)
        self.create_button("7", layout, 2, 1, self.add_to_value, 7, widget_width, widget_height)
        self.create_button("8", layout, 2, 2, self.add_to_value, 8, widget_width, widget_height)
        self.create_button("9", layout, 2, 3, self.add_to_value, 9, widget_width, widget_height)
       
        if flag == NUMPAD_ONLY_INT_NO_UNIT:
            self.create_button("OK", layout, 3, 0, self.confirm_value, -1, widget_width * 5 + 5, widget_height, colspan=5)
        else:
            self.create_button(".", layout, 3, 0, self.add_to_value,".", widget_width, widget_height)
            if len(self.units) == 2:
                self.create_button(f"{self.units[0]}", layout, 3, 1, self.set_unit, f"{self.units[0]}", widget_width, widget_height)
                self.create_button(f"{self.units[1]}", layout, 3, 2, self.set_unit, f"{self.units[1]}", widget_width, widget_height)
                self.create_button("OK", layout, 3, 3, self.confirm_value, -1, widget_width * 2 + 2, widget_height, colspan=2)
            elif len(self.units) == 1:
                self.create_button(f"{self.units[0]}", layout, 3, 1, self.set_unit, self.unit, widget_width, widget_height)
                self.create_button("OK", layout, 3, 2, self.confirm_value, -1, widget_width * 3 + 3, widget_height, colspan=3)
            else:
                self.create_button("OK", layout, 3, 1, self.confirm_value, -1, widget_width * 4 + 4, widget_height, colspan=4)
        

        # Show the window
        self.show()

    def showEvent(self, event):
        """Ensure the window takes focus when shown."""
        self.activateWindow()
        self.raise_()
        super().showEvent(event)

    def create_button(self, text, layout, row, col, callback, value, width=50, height=50, colspan=1):
        """Helper function to create custom buttons."""
        button = PushButton(self)

        if text[0] == "_":
            if text[1:] == "back":
                button.configure(
                    text="", posX=row, posY=col,
                    width=width, height=height,
                    font_size=fontsize_large, font_bold=True,
                    bg=C_button_off, fg=C_text_dark,
                    checked_bg=C_button_on, checked_fg=C_text_light,
                    border_radius=4
                )
                button.setIcon(QIcon(os.path.join(general_icon_path, "backspace.svg")))
                button.setIconSize(QSize(20, 20))
        else:
            button.configure(
                text=text, posX=row, posY=col,
                width=width, height=height,
                font_size=fontsize_large, font_bold=True,
                bg=C_button_off, fg=C_text_dark,
                checked_bg=C_button_on, checked_fg=C_text_light,
                border_radius=4
            )
        button.clicked.connect(lambda: callback(value))
        layout.addWidget(button, row, col, 1, colspan)
        
    def calculate_current_value_from_history(self):
        value = f""
        for val in self.history:
           
            value = f"{value}{val}"
        
        self.value_label.set_text(f"{value} {self.unit}")

    def add_to_value(self, val):
        """Adds a digit to the current value."""
        self.history.append(val)
        self.calculate_current_value_from_history()

    def delete_last(self, _):
        try:        
            self.history.pop()
        except IndexError:
            self.history = ["0"]
        
        self.calculate_current_value_from_history()

    def dec_count(self, _):
        """Tracks decimal point precision."""
        self.decimal_count_offset += 1

    def set_unit(self, unit_text):
        """Sets the unit for the value."""
        value = self.value_label.text().split(" ")[0]
        self.unit = unit_text
        self.value_label.set_text(f"{value} {self.unit}")

    def confirm_value(self, _):
        """Confirms the value and closes the window."""
        value = self.value_label.text()
        try:
            numeric_value, unit = value.split(" ")[0], value.split(" ")[1]
            numeric_value = float(numeric_value)
            self.callback(numeric_value, unit)
        except Exception:
            self.callback(0.0, self.unit)
        self.close()
