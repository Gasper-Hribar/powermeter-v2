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
from src.GUI.toplevel_windows.numpad_ui import Numpad
from src.GUI.widgets.dropdown_menu import DropdownMenu
import src.configs.settings as flc_settings

version = gui_settings.VERSION
interface = flc_settings.HARDWARE_INTERFACE
general_icon_path = config.GENERAL_ICON_PATH
screen_width = width
screen_height = height

class DACGroup(QWidget):

    # TODO: CHANGE THE MAX VALUE TO SETTING THAT IS READ FROM THE EXCEL FILES

    def __init__(self, parent: QWidget, port_number: int):
        super().__init__(parent)

        self.setObjectName(u"dacGroup")
        self.setParent(parent)
        self.value = 1.0
        self.callback_set = False
        
        self.port_number = port_number

        self.setStyleSheet(f"""
                            QWidget {{
                                background-color: {C_main_background};
                                border-radius: 4px;
                            }}
                            """)


    def configure(self, name: str = "", labeltext: str = "DACGroup", default_value: float = 0.000, unit_text: str = "V", min: float = 0, max: float = 10,  bg: str = C_main_background, fg: str = C_text_dark, posX: int = 0, posY: int = 0, width: int = DAC_GROUP_WIDTH, height: int = DAC_GROUP_HEIGHT, border: str = "transparent", border_radius: int = 16, padding: int = 0, font: str = fontfamily, font_size: int = fontsize_small, font_bold: bool = False, rowcount: int = 2, colcount: int = 6):
        """
        Configures the group with the specified properties.
        Args:
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
        self.setFixedSize(width, height)
        self.labeltext = labeltext
        self.unit_text = unit_text
        self.value = default_value
        self.min = min
        self.max = max
        
        if not name == "":
            self.setObjectName(name)

        two_label = f"""
                        <div style='text-align: center; font-size: {fontsize_tiny};'>
                            <b>{labeltext}</b><br>{self.value} {unit_text}
                        </div>
                    """

        self.gridlayout = QGridLayout()

        [self.gridlayout.setRowStretch(row, 0) for row in range(rowcount)]
        [self.gridlayout.setColumnStretch(column, 0) for column in range(colcount)]
        [self.gridlayout.setRowMinimumHeight(row, int(height/rowcount)) for row in range(rowcount)]
        [self.gridlayout.setColumnMinimumWidth(column, int(width/colcount)) for column in range(colcount)]
        self.gridlayout.setSpacing(0)
        self.gridlayout.setContentsMargins(0, 2, 0, 2)
        self.setLayout(self.gridlayout)

        steps = get_steps(int(self.max))

        self.decrease_btn = OperatorButton(self)
        self.decrease_btn.configure(operator=ui_operators.DECREASE, bg=C_button_off, fg=C_text_dark, width=OPERATOR_BUTTON_WIDTH, height=OPERATOR_BUTTON_HEIGHT, border_radius=OPERATOR_BUTTON_HEIGHT//5)
        self.gridlayout.addWidget(self.decrease_btn, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.decrease_btn.set_callback(self.decrease_value)

        self.value_entry = Label(self)
        self.value_entry.configure(text=two_label, width=DROPDOWN_WIDTH, height=3 * LABEL_HEIGHT//2, bg=C_dac_label_bg, fg=C_dac_label_fg, border_color=C_dac_label_border, font=fontfamily, font_size=fontsize_small, font_bold=False, border_radius=(LABEL_HEIGHT + LABEL_HEIGHT//3)//2, border=2)
        self.gridlayout.addWidget(self.value_entry, 0, 1, 1, 4, Qt.AlignmentFlag.AlignCenter)

        self.increase_btn = OperatorButton(self)
        self.increase_btn.configure(operator=ui_operators.INCREASE, bg=C_button_off, fg=C_text_dark, width=OPERATOR_BUTTON_WIDTH, height=OPERATOR_BUTTON_HEIGHT, border_radius=OPERATOR_BUTTON_HEIGHT//5)
        self.gridlayout.addWidget(self.increase_btn, 0, 5, 1, 1, Qt.AlignmentFlag.AlignRight)
        self.increase_btn.set_callback(self.increase_value)

        self.dropdown_step = DropdownMenu(self)
        self.dropdown_step.configure(items=steps, width=DROPDOWN_WIDTH, height=DROPDOWN_HEIGHT, font=fontfamily, font_size=fontsize_normal, font_bold=False, bg=C_button_off, fg=C_text_dark, border_radius=DROPDOWN_HEIGHT//2)
        self.gridlayout.addWidget(self.dropdown_step, 1, 1, 1, 4, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)

        self.decrease_btn.setEnabled(True)
        self.increase_btn.setEnabled(True)
        self.value_entry.setEnabled(False)

    """
    Program logic methods specific to the DACGroup widget.
    """

    def decrease_value(self):
        self.set_value(round(self.get_value() - float(self.dropdown_step.get_selected_item()), 3))

    def increase_value(self):
        self.set_value(round(self.get_value() + float(self.dropdown_step.get_selected_item()), 3))

    def set_value(self, value: float):
        self.value = bound_min_max(value, self.min, self.max)
        text = f"""
                        <div style='text-align: center; font-size: {fontsize_normal};'>
                            <b>{self.labeltext}</b><br>{self.value} {self.unit_text}
                        </div>
                    """
        try:
            self.callback(self.objectName(), self.port_number, self.value)
        except Exception as e:
            print(f"Error in callback: {e}")
            pass
        self.value_entry.setText(text)

        
    def sync_value(self, value: float):
        self.value = value
        text = f"""
                        <div style='text-align: center; font-size: {fontsize_normal};'>
                            <b>{self.labeltext}</b><br>{self.value} {self.unit_text}
                        </div>
                    """
        self.value_entry.setText(text)

    def set_callback(self, callback):
        self.callback_set = True
        self.callback = callback

    def get_value(self) -> float:
        return self.value
    
    def get_name(self) -> str:
        return self.objectName()
    
    def get_port_number(self) -> int:
        return self.port_number
        

class DACGroupRPI(QWidget):


    def __init__(self, parent: QWidget, port_number: int):
        super().__init__(parent)

        self.setParent(parent)
        self.value = 1.0
        self.callback_set = False
        self.port_number = port_number

        self.setStyleSheet(f"""
                            QWidget {{
                                background-color: {C_main_background};
                                border-radius: 4px;
                            }}
                            """)


    def configure(self, name:str = "", labeltext: str = "DACGroup", default_value: float = 0.000, unit_text: str = "V", min: float = 0, max: float = 10,  bg: str = C_main_background, fg: str = C_text_dark, posX: int = 0, posY: int = 0, width: int = DAC_GROUP_WIDTH, height: int = DAC_GROUP_HEIGHT, border: str = "transparent", border_radius: int = 8, padding: int = 0, font: str = fontfamily, font_size: int = 10, font_bold: bool = False, rowcount: int = 2, colcount: int = 6):
        """
        Configures the group with the specified properties.
        Args:
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
        self.setFixedSize(width, height)
        self.labeltext = labeltext
        self.unit_text = unit_text
        self.value = default_value
        self.min = min
        self.max = max
        
        if not name == "":
            self.setObjectName(name)
    	
        two_label = f"""{self.labeltext}\n{self.value} {self.unit_text}"""                        

        self.gridlayout = QGridLayout()

        self.gridlayout.setSpacing(0)
        self.gridlayout.setContentsMargins(0, 2, 0, 2)
        self.setLayout(self.gridlayout)

        self.value_entry_button = PushButton(self)
        self.value_entry_button.configure(name=name, text=two_label, bg=C_dac_label_bg, fg=C_dac_label_fg, border=2, border_color=C_dac_label_border, width=DAC_GROUP_WIDTH - DAC_GROUP_WIDTH//5, height=DAC_GROUP_HEIGHT - DAC_GROUP_HEIGHT//4, border_radius=DAC_GROUP_HEIGHT//4, font=fontfamily, font_size=fontsize_small, font_bold=False)
        self.value_entry_button.set_callback(self.open_DACGroupL2)
        self.gridlayout.addWidget(self.value_entry_button, 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.value_entry_button.setEnabled(True)

    """
    Program logic methods specific to the DACGroup widget.
    """
    def open_DACGroupL2(self):
        window_size = (DAC_GROUP_WIDTH + DAC_GROUP_WIDTH//3, DAC_GROUP_HEIGHT + DAC_GROUP_HEIGHT//3)
        self.new_DAC_window = QMainWindow()
        self.new_DAC_window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        if interface == "RASPBERRY_PI":
            self.new_DAC_window.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        else:
            self.new_DAC_window.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)
        self.new_DAC_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.new_DAC_window.setWindowTitle("Set DAC Value")
        self.new_DAC_window.setWindowIcon(QIcon(os.path.join(general_icon_path,"folas_logo.svg")))
        self.new_DAC_window.setFixedSize(window_size[0], window_size[1])

        self.new_DAC_window.setStyleSheet(f"""
            QMainWindow {{
                background-color: {C_main_background};
                border-radius: 4px;
                border: 2px solid {C_adc_label_border};
            }}
        """)

        central_widget = QWidget(self)
        self.new_DAC_window.setCentralWidget(central_widget)

        DAC_group_grid = QGridLayout()
        self.new_DAC_window.setLayout(DAC_group_grid)

        self.DAC_group = DACGroupL2(self.new_DAC_window, self.port_number)
        self.DAC_group.configure(labeltext=self.labeltext, default_value=self.value, unit_text=self.unit_text, min=self.min, max=self.max, bg=C_main_background, fg=C_text_dark, posX=screen_width//2-window_size[0], posY=screen_height//2-window_size[1], width=window_size[0], height=window_size[1], border_radius=window_size[1]//5, padding=0, font=fontfamily, font_size=fontsize_normal, font_bold=False)
        self.DAC_group.set_callback(self.set_value)

        self.new_DAC_window.move(int(screen_width/2 - window_size[0]/2), int(screen_height/2 - window_size[1]/2 - screen_height//10))
        self.new_DAC_window.show()

    def set_value(self, value: float, unit: str):
        if "m" in unit:
            value /= 1000
        
        self.value = bound_min_max(value, self.min, self.max)

        text = f"""{self.labeltext}\n{self.value} {self.unit_text}"""
        try:
            self.callback(self.value_entry_button.get_name(), self.port_number, self.value)
        except Exception as e:
            print(f"Error in callback: {e}")
            pass

        self.value_entry_button.setText(text)

    def sync_value(self, value: float):
        self.value = value
        text = f"""{self.labeltext}\n{self.value} {self.unit_text}"""
        self.value_entry_button.setText(text)

    def set_callback(self, callback):
        self.callback_set = True
        self.callback = callback

    def get_value(self) -> float:
        return self.value
    
    def get_name(self) -> str:
        return self.objectName()
    
    def get_port_number(self) -> int:
        return self.port_number

class DACGroupL2(QWidget):

    def __init__(self, parent: QWidget, port_number: int):
        super().__init__(parent)

        self.setObjectName(u"dacGroupLevel2")
        self.setParent(parent)
        self.value = 1.0
        self.callback_set = False
        
        self.port_number = port_number

        self.setStyleSheet(f"""
                            QWidget {{
                                background-color: {C_main_background};
                                border-radius: 4px;
                            }}
                            """)

    def configure(self, labeltext: str = "DACGroup", default_value: float = 0.000, unit_text: str = "V", min: float = 0, max: float = 10,  bg: str = C_main_background, fg: str = C_text_dark, posX: int = 0, posY: int = 0, width: int = DAC_GROUP_WIDTH, height: int = DAC_GROUP_HEIGHT, border: str = "transparent", border_radius: int = 8, padding: int = 0, font: str = "Lato", font_size: int = 10, font_bold: bool = False, rowcount: int = 2, colcount: int = 5):
        """
        Configures the group with the specified properties.
        Args:
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
            font (str): The font family of the group. Defaults to "Lato".
            font_size (int): The font size of the group. Defaults to 10.
            font_bold (bool): The font weight of the group. Defaults to False.
            rowcount (int): The number of rows in the grid layout. Defaults to 2.
            colcount (int): The number of columns in the grid layout. Defaults to 10.
        """
        
        self.move(posX, posY)
        self.setFixedSize(width, height)
        self.labeltext = labeltext
        self.unit_text = unit_text
        self.value = default_value
        self.min = min
        self.max = max
    	
        two_label = f"""{self.value} {self.unit_text}"""

        self.gridlayout = QGridLayout()

        [self.gridlayout.setRowStretch(row, 0) for row in range(rowcount)]
        [self.gridlayout.setColumnStretch(column, 0) for column in range(colcount)]
        [self.gridlayout.setRowMinimumHeight(row, int(height/rowcount)) for row in range(rowcount)]
        [self.gridlayout.setColumnMinimumWidth(column, int(width/colcount)) for column in range(colcount)]
        self.gridlayout.setSpacing(1)
        self.gridlayout.setContentsMargins(3, 3, 3, 3)
        self.setLayout(self.gridlayout)

        widget_width = int((width-6)/colcount)  # 6 is the total padding on the sides + spacing between widgets
        widget_height = int((height-5)/rowcount)  # 5 is the total padding on the top and bottom + spacing between widgets

        steps = get_steps(int(self.max))

        self.decrease_btn = OperatorButton(self)
        self.decrease_btn.configure(operator=ui_operators.DECREASE, bg=C_button_off, fg=C_text_dark, width=widget_width, height=widget_width, border_radius=widget_width//3)
        self.gridlayout.addWidget(self.decrease_btn, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.decrease_btn.set_callback(self.decrease_value)

        self.value_entry_button = PushButton(self)
        self.value_entry_button.configure(text=two_label, bg=C_dac_label_bg, fg=C_dac_label_fg, border=2, border_color=C_dac_label_border, width=3*widget_width, height=widget_height, border_radius=widget_width//3, font=fontfamily, font_size=fontsize_small, font_bold=False)
        self.gridlayout.addWidget(self.value_entry_button, 0, 1, 1, 3, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.value_entry_button.set_callback(self.open_numpad)

        self.increase_btn = OperatorButton(self)
        self.increase_btn.configure(operator=ui_operators.INCREASE, bg=C_button_off, fg=C_text_dark, width=widget_width, height=widget_width, border_radius=widget_width//3)
        self.gridlayout.addWidget(self.increase_btn, 0, 4, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.increase_btn.set_callback(self.increase_value)

        self.dropdown_step = DropdownMenu(self)
        self.dropdown_step.configure(items=steps, width=3*widget_width, height=widget_width, font=fontfamily, font_size=fontsize_normal, font_bold=False, bg=C_button_off, fg=C_text_dark, border_radius=DROPDOWN_HEIGHT//2, padding=40)
        self.gridlayout.addWidget(self.dropdown_step, 1, 1, 1, 3, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)

        self.OK_button = PushButton(self)
        self.OK_button.configure(text="OK", bg=C_button_off, fg=C_text_dark, width=widget_width, height=widget_width, border_radius=widget_width//3)
        self.gridlayout.addWidget(self.OK_button, 1, 4, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.OK_button.set_callback(self.close_window)

        self.decrease_btn.setEnabled(True)
        self.increase_btn.setEnabled(True)
        self.OK_button.setEnabled(True)
        self.value_entry_button.setEnabled(True)

    """
    Program logic methods specific to the DACGroup widget.
    """
    def open_numpad(self):
        print("Opening numpad")
        size = (NUMPAD_WIDGET_WIDTH, NUMPAD_WIDGET_HEIGHT)
        if not "m" in self.unit_text or not "u" in self.unit_text:
            units = [f"m{self.unit_text}", f"{self.unit_text}"]
        else:
            units = [f"{self.unit_text}"]   

        self.numpad = Numpad(callback=self.set_value, value=self.value, unit=self.unit_text, units=units, width=size[0], height=size[1])
        
        self.numpad.move(int(screen_width/2 - size[0]/2), int(screen_height/2 - size[1]/2 - 100))
        self.numpad.show()

    def decrease_value(self):
        self.set_value(round(self.get_value() - float(self.dropdown_step.get_selected_item()), 3))

    def increase_value(self):
        self.set_value(round(self.get_value() + float(self.dropdown_step.get_selected_item()), 3))

    def set_value(self, value: float, unit: str =""):
        
        if "m" in unit:
            value /= 1000

        self.value = bound_min_max(value, self.min, self.max)

        self.callback(self.value, self.unit_text)
        text = f"""{self.labeltext}\n{self.value:.3f} {self.unit_text}"""
        self.value_entry_button.setText(text)

    def set_callback(self, callback):
        self.callback_set = True
        self.callback = callback

    def get_value(self) -> float:
        return self.value
    
    def get_name(self) -> str:
        return self.objectName()
    
    def get_port_number(self) -> int:
        return self.port_number
    
    def close_window(self):
        self.close()
        self.parent().close() # type: ignore

    
class DACGroupDelayline(QWidget):

    def __init__(self, parent: QWidget, port_number: int):
        super().__init__(parent)

        self.setObjectName(u"dacGroupLevel2")
        self.setParent(parent)
        self.value = 1.0
        self.callback_set = False
        
        self.port_number = port_number

        self.setStyleSheet(f"""
                            QWidget {{
                                background-color: {C_main_background};
                                border-radius: 4px;
                            }}
                            """)

    def configure(self, name: str = "", text: str = "DACGroupDelayline", default_value: int = 0, unit_text: str = "ps", min: float = 0, max: float = 40920, step: int = 10, bg: str = C_main_background, fg: str = C_text_dark, posX: int = 0, posY: int = 0, width: int = DAC_GROUP_WIDTH, height: int = DAC_GROUP_HEIGHT, border: int = 0, border_color: str = "transparent", border_radius: int = 8, padding: int = 0, font: str = "Lato", font_size: int = 10, font_bold: bool = False, rowcount: int = 2, colcount: int = 5):
        """
        Configures the group with the specified properties.
        Args:
            text (str): The text to display on the group. Defaults to "DACGroup".
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
            font (str): The font family of the group. Defaults to "Lato".
            font_size (int): The font size of the group. Defaults to 10.
            font_bold (bool): The font weight of the group. Defaults to False.
            rowcount (int): The number of rows in the grid layout. Defaults to 2.
            colcount (int): The number of columns in the grid layout. Defaults to 10.
        """

        if not name == "":
            self.setObjectName(name)
        
        self.move(posX, posY)
        self.setFixedSize(width, height)
        self.text = text
        self.unit_text = unit_text
        self.value = default_value
        self.min = min
        self.max = max
        self.step = step
    	
        self.text = f"""{self.value} {self.unit_text}"""

        self.gridlayout = QGridLayout()

        [self.gridlayout.setRowStretch(row, 0) for row in range(rowcount)]
        [self.gridlayout.setColumnStretch(column, 0) for column in range(colcount)]
        [self.gridlayout.setRowMinimumHeight(row, int(height/rowcount)) for row in range(rowcount)]
        [self.gridlayout.setColumnMinimumWidth(column, int(width/colcount)) for column in range(colcount)]
        self.gridlayout.setSpacing(1)
        self.gridlayout.setContentsMargins(3, 3, 3, 3)
        self.setLayout(self.gridlayout)

        widget_width = int((width-6)/colcount)  # 6 is the total padding on the sides + spacing between widgets
        widget_height = int((height-5)/rowcount)  # 5 is the total padding on the top and bottom + spacing between widgets

        # TODO: fix the sizing of the widgets

        steps = get_steps(int(self.max))

        self.decrease_btn = OperatorButton(self)
        self.decrease_btn.configure(operator=ui_operators.DECREASE, bg=C_button_off, fg=C_text_dark, width=int(1.2*widget_height), height=widget_height, border_radius=widget_height//3, font=fontfamily, font_size=fontsize_normal, font_bold=False)
        self.gridlayout.addWidget(self.decrease_btn, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.decrease_btn.set_callback(self.decrease_value)

        self.value_entry_button = PushButton(self)
        self.value_entry_button.configure(text=self.text, bg=bg, fg=fg, border=border, border_color=border_color, width=3*widget_width, height=widget_height, border_radius=widget_height//2, font=fontfamily, font_size=fontsize_large, font_bold=False)
        self.gridlayout.addWidget(self.value_entry_button, 0, 1, 1, 3, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.value_entry_button.set_callback(self.open_numpad)

        self.increase_btn = OperatorButton(self)
        self.increase_btn.configure(operator=ui_operators.INCREASE, bg=C_button_off, fg=C_text_dark, width=int(1.2*widget_height), height=widget_height, border_radius=widget_height//3, font=fontfamily, font_size=fontsize_normal, font_bold=False)
        self.gridlayout.addWidget(self.increase_btn, 0, 4, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.increase_btn.set_callback(self.increase_value)

        self.dropdown_step = DropdownMenu(self)
        self.dropdown_step.configure(items=steps, width=3*widget_width, height=widget_height, font=fontfamily, font_size=fontsize_normal, font_bold=False, bg=C_button_off, fg=C_text_dark, border_radius=widget_height//2, padding=widget_width//3)
        self.gridlayout.addWidget(self.dropdown_step, 1, 1, 1, 3, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)

        self.decrease_btn.setEnabled(True)
        self.increase_btn.setEnabled(True)
        self.value_entry_button.setEnabled(True)

    """
    Program logic methods specific to the DACGroup widget.
    """
    def open_numpad(self):
        print("Opening numpad")
        size = (NUMPAD_WIDGET_WIDTH, NUMPAD_WIDGET_HEIGHT)
        units = [f"{self.unit_text}"]   

        self.numpad = Numpad(callback=self.set_value, value=self.value, unit=self.unit_text, units=units, width=size[0], height=size[1])
        if interface == "RASPBERRY_PI":
            self.numpad.move(int(screen_width/2 - size[0]/2), int(screen_height/2 - size[1]/2 - 100))

        self.numpad.show()

    def decrease_value(self):
        self.set_value(int(self.get_value() - int(self.dropdown_step.get_selected_item())))

    def increase_value(self):
        self.set_value(int(self.get_value() + int(self.dropdown_step.get_selected_item())))

    def set_value(self, value: int, unit: str =""):
        value = (value//self.step) * self.step 
        value = int(bound_min_max(float(value), float(self.min), float(self.max)))
        self.value = value
        text = f"""{self.value} {self.unit_text}"""
        self.value_entry_button.setText(text)
        self.callback(self.value, self.unit_text)

    def set_callback(self, callback):
        self.callback_set = True
        self.callback = callback
    
    def sync_value(self, value: int):
        self.value = value

    def set_text(self, text: str):
        self.text = text
        self.value_entry_button.setText(text)

    def get_value(self) -> float:
        return self.value
    
    def get_name(self) -> str:
        return self.objectName()
    
    def get_port_number(self) -> int:
        return self.port_number
    
    def set_enabled(self, enabled: bool):
        self.decrease_btn.set_enabled(enabled)
        self.increase_btn.set_enabled(enabled)
        self.value_entry_button.set_enabled(enabled)
        self.dropdown_step.set_enabled(enabled)
        