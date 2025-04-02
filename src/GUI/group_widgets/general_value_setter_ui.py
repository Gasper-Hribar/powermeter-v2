import os
from PySide6.QtCore import (Qt)
from PySide6.QtWidgets import (QWidget, QGridLayout, QMainWindow)
from PySide6.QtGui import (QIcon)
from src.GUI.constants.steps import get_steps
from src.GUI.utils.bound_min_max import bound_min_max
from src.GUI.constants import ui_operators
from src.GUI.constants.ui_colors import *
from src.GUI.constants.ui_fonts import *
from src.GUI.constants.ui_geometry import *
import src.configs.gui_settings as gui_settings
import src.GUI.constants.config as config
from src.GUI.widgets.label_ui import Label
from src.GUI.widgets.operator_button_ui import OperatorButton
from src.GUI.widgets.push_button_ui import PushButton
from src.GUI.toplevel_windows.numpad_ui import NUMPAD_ONLY_INT_NO_UNIT, Numpad
import src.configs.settings as flc_settings
from src.utils.logger import get_logger

logger = get_logger("GUI")

version = gui_settings.VERSION
interface = flc_settings.HARDWARE_INTERFACE
general_icon_path = config.GENERAL_ICON_PATH
screen_width = gui_settings.SCREEN_WIDTH
screen_height = gui_settings.SCREEN_HEIGHT

vs_flag_single_line_pos = 0

VS_SINGLE_LINE = 0b0
VS_MULTI_LINE = 0b1

class ValueSetter(QWidget):

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setObjectName(u"ValueSetter")
        self.setParent(parent)
        self.value = 0
        self.callback_set = False
        self.step_value = 1
        self.step = 1
        self.flags = 0

        self.setStyleSheet(f"""
                            #ValueSetter {{
                                background-color: {C_main_background};
                                border-radius: 4px;
                            }}
                            """)


    def configure(self, name: str = "", labeltext: str = "ValueSetter", default_value: int = 0, unit_text: str = "", min: int = 0, max: int = 1000,  bg: str = C_main_background, fg: str = C_text_dark, posX: int = 0, posY: int = 0, width: int = 150, height: int = 25, border: str = "transparent", border_radius: int = 12, padding: int = 0, font: str = fontfamily, font_size: int = fontsize_small, font_bold: bool = False, rowcount: int = 1, colcount: int = 6, flags: int = 0):
        """
        Configures the group with the specified properties.
        Args:
            name (str): The name of the group. Defaults to "".
            labeltext (str): The text to display on the group. Defaults to "DACGroup".
            bg (str): The background color of the group in its default state. Defaults to transparent.
            fg (str): The foreground (text) color of the group in its default state. Defaults to UI_BLACK.
            checked_bg (str): The background color of the group when it is checked. Defaults to UI_ORANGE.
            checked_fg (str): The foreground (text) color of the group when it is checked. Defaults to UI_BLACK.
            posX (int): The x-coordinate of the group's position. Defaults to 0.
            posY (int): The y-coordinate of the group's position. Defaults to 0.
            width (int): The width of the group. Defaults to 100.
            height (int): The height of the group. Defaults to 60.
            border_radius (int): The border radius of the group. Defaults to 6.
            padding (int): The padding of the group. Defaults to 0.
            font (str): The font family of the group. Defaults to fontfamily.
            font_size (int): The font size of the group. Defaults to 10.
            font_bold (bool): The font weight of the group. Defaults to False.
            rowcount (int): The number of rows in the grid layout. Defaults to 2.
            colcount (int): The number of columns in the grid layout. Defaults to 10.
        """
        
        self.move(posX, posY)
        self.labeltext = labeltext
        self.unit_text = unit_text
        self.value = default_value
        self.min = min
        self.max = max
        self.flags = flags
        fontsize = font_size

        self.setFixedSize(width, height)

        if OPERATOR_BUTTON_HEIGHT > height:
            operator_size = height
        else:
            operator_size = OPERATOR_BUTTON_HEIGHT
        
        if not name == "":
            self.setObjectName(name)
    	
        text = self._get_text_from_value(self.labeltext, self.value, self.unit_text)

        self.gridlayout = QGridLayout()

        [self.gridlayout.setRowStretch(row, 0) for row in range(rowcount)]
        [self.gridlayout.setColumnStretch(column, 0) for column in range(colcount)]
        [self.gridlayout.setRowMinimumHeight(row, int(height/rowcount)) for row in range(rowcount)]
        [self.gridlayout.setColumnMinimumWidth(column, int(width/colcount)) for column in range(colcount)]
        self.gridlayout.setSpacing(0)
        self.gridlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.gridlayout)

        self.decrease_btn = OperatorButton(self)
        self.decrease_btn.configure(operator=ui_operators.DECREASE, width=operator_size, height=operator_size, border_radius=operator_size//4, bg=C_button_off, fg=C_text_dark)
        self.gridlayout.addWidget(self.decrease_btn, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.decrease_btn.set_callback(self.decrease_value)

        self.value_entry = PushButton(self)
        self.value_entry.configure(name=name, text=text, bg=bg, fg=fg, border=2, border_color=border, width=DROPDOWN_WIDTH, height=height, border_radius=3 * height//7, font=font, font_size=fontsize, font_bold=font_bold)
        self.gridlayout.addWidget(self.value_entry, 0, 1, 1, 4, Qt.AlignmentFlag.AlignCenter)
        self.value_entry.set_callback(self.open_numpad)

        self.increase_btn = OperatorButton(self)
        self.increase_btn.configure(operator=ui_operators.INCREASE, width=operator_size, height=operator_size, border_radius=operator_size//4, bg=C_button_off, fg=C_text_dark)
        self.gridlayout.addWidget(self.increase_btn, 0, 5, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.increase_btn.set_callback(self.increase_value)

        self.decrease_btn.setEnabled(True)
        self.increase_btn.setEnabled(True)
        self.value_entry.setEnabled(True)

    """
    Program logic methods specific to the ValueSetter widget.
    """

    def decrease_value(self):
        self.set_value(int(self.get_value() - self.step))

    def increase_value(self):
        self.set_value(int(self.get_value() + self.step))

    def set_value(self, value: float, *args, **kwargs):
        self.value = int(bound_min_max(value, self.min, self.max))
        text = self._get_text_from_value(self.labeltext, self.value * self.step_value, self.unit_text)
        try:
            self.callback(name=self.objectName(), value=self.value)
            self.value_entry.setText(text)
        except Exception as e:
            logger.info(f"{self.objectName()}: Error in callback: {e}")
            # self.value_entry.setText("Error")
    
        
    def sync_value(self, value: float):
        self.value = value
        text = self._get_text_from_value(self.labeltext, self.value, self.unit_text)
        self.value_entry.setText(text)

    def set_callback(self, callback, *args, **kwargs):
        self.callback_set = True
        self.callback = callback

    def get_value(self) -> float:
        return self.value
    
    def get_name(self) -> str:
        return self.objectName()
    
    def set_value_from_numpad(self, value: float, *args, **kwargs):
        point_value = value//self.step_value
        self.set_value(point_value)
    
    def open_numpad(self):
        numpad = Numpad(callback=self.set_value_from_numpad, value=self.value*self.step_value, unit=self.unit_text, units=[""], flag=NUMPAD_ONLY_INT_NO_UNIT)
        numpad.show()

    def set_step_value(self, step: int):
        if not self.step_value == step:
            self.step_value = step
        self.set_value(self.value)

    def _get_text_from_value(self, label, value, unit) -> str:
        if self.flags & (1 << vs_flag_single_line_pos) == 0:
            return f"{value} {unit}"
        else:
            return f"""{label}\n{value} {unit}""" 
       
    def set_unit(self, unit: str):
        self.unit_text = unit