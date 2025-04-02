from PySide6.QtCore import (Qt)
from PySide6.QtWidgets import (QWidget, QGridLayout)
from src.GUI.constants.ui_colors import *
from src.GUI.constants.ui_fonts import *
from src.GUI.constants.ui_geometry import *
import src.configs.gui_settings as gui_settings
from src.GUI.widgets.label_ui import Label
from src.GUI.widgets.text_entry_ui import TextEntry

version = gui_settings.VERSION
class ADCGroup(QWidget):

    
    def __init__(self, parent: QWidget, port_number: int):
        super().__init__(parent)

        self.setParent(parent)
        self.value = 1.0
        self.port_number = port_number



    def configure(self, name: str = "", labeltext: str = "ADCGroup", default_value: float = 0.000, unit_text: str = "V", min: float = 0, max: float = 10, bg: str = "transparent", fg: str = C_text_dark, border: str = C_button_off, posX: int = 0, posY: int = 0, width: int = 140, height: int = 25, border_radius: int = 12, padding: int = 0, font: str = fontfamily, font_size: int = fontsize_small, font_bold: bool = False, rowcount: int = 1, colcount: int = 8):
        """
        Configures the group with the specified properties.
        Args:
            labeltext (str): The text to display on the group. Defaults to "ADCGroup".
            bg (str): The background color of the group in its default state. Defaults to transparent.
            fg (str): The foreground (text) color of the group in its default state. Defaults to UI_BLACK.
            unit_text (str): The unit of the value displayed in the group. Defaults to "V".
            min (float): The minimum value that the group can display. Defaults to 0.
            max (float): The maximum value that the group can display. Defaults to 10.
            posX (int): The x-coordinate of the group. Defaults to 0.
            posY (int): The y-coordinate of the group. Defaults to 0.
            width (int): The width of the group. Defaults to 140.
            height (int): The height of the group. Defaults to 25.
            border_radius (int): The radius of the border of the group. Defaults to 4.
            border (str): The color of the border of the group. Defaults to UI_GRAY.
            padding (int): The padding of the group. Defaults to 0.
            font (str): The font of the text displayed on the group. Defaults to "Lato".
            font_size (int): The size of the font of the text displayed on the group. Defaults to 10.
            font_bold (bool): Whether the font of the text displayed on the group should be bold. Defaults to False.
            rowcount (int): The number of rows in the grid layout of the group. Defaults to 2.
            colcount (int): The number of columns in the grid layout of the group. Defaults to 8.
        """

        if not name == "":
            self.setObjectName(name)

        self.setStyleSheet(f"""
                            #{{{name}}} {{
                                background-color: {bg};
                                border-radius: {border_radius}px;
                                border: 0px solid {border};
                            }}
                            """)
        
        # self.setAutoFillBackground(False)
        
        self.move(posX, posY)

        if len(labeltext) > 9:
            labeltext = labeltext[:9] + "."


        self.setFixedSize(width, height)
        if LABEL_WIDTH + TEXT_ENTRY_WIDTH > width:
            label_width = width - TEXT_ENTRY_WIDTH
        else:
            label_width = LABEL_WIDTH - int(scale_factor*10)
        # label_width = LABEL_WIDTH - int(scale_factor*10)

        self.gridlayout = QGridLayout()

        [self.gridlayout.setRowStretch(row, 0) for row in range(rowcount)]
        [self.gridlayout.setColumnStretch(column, 0) for column in range(colcount)]
        [self.gridlayout.setRowMinimumHeight(row, int(height/rowcount)) for row in range(rowcount)]
        self.gridlayout.setSpacing(0)
        self.gridlayout.setContentsMargins(1, 1, 1, 1)
        self.setLayout(self.gridlayout)

        #define the label
        self.label = Label(self)
        self.label.configure(text=f"{labeltext}", width=label_width, height=height, bg="transparent", fg=fg, font=fontfamily, font_size=fontsize_small, font_bold=True, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.gridlayout.addWidget(self.label, 0, 0, 1, colcount//2, Qt.AlignmentFlag.AlignLeft)

        self.value_entry = TextEntry(self)
        self.value_entry.configure(name=name, default_value=str(default_value), unit=unit_text, edit_enabled=False, width=TEXT_ENTRY_WIDTH, height=height-2, bg=C_adc_label_bg, fg=C_adc_label_fg, border_color=border, border_radius=(height-2)//2, font=fontfamily, font_size=fontsize_small, font_bold=True)
        self.gridlayout.addWidget(self.value_entry, 0, colcount//2 + 1, 1, colcount//2, Qt.AlignmentFlag.AlignRight)

        self.update()


    def set_value(self, value: float):
    
        self.value = value
        self.value_entry.set_value(value)
        self.value_entry.update()

    def set_unit_prefix(self, unit_prefix: str):
        self.value_entry.set_unit_prefix(unit_prefix)
        self.value_entry.update()

    def set_amplification(self, amplification: float | int):
        self.value_entry.set_amplification(amplification)
        self.value_entry.update()
    
    def get_amplification(self) -> float:
        return self.value_entry.get_amplification()

    def get_name(self) -> str:
        return self.objectName()
    
    def get_port_number(self) -> int:
        return self.port_number
    
    def get_value(self) -> float:
        return self.value