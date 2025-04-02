from PySide6.QtWidgets import QWidget, QGridLayout
from PySide6.QtCore import Qt
from src.GUI.widgets.push_button_ui import PushButton
from src.GUI.group_widgets.dac_group_ui import DACGroupDelayline
from src.GUI.constants.ui_colors import *
from src.GUI.constants.ui_geometry import *
from src.GUI.constants.ui_fonts import *
import src.configs.gui_settings as gui_settings
from src.GUI.widgets.label_ui import Label
from src.utils.logger import get_logger
from src.GUI.group_widgets.dac_group_ui import Numpad
import src.configs.settings as flc_settings

logger = get_logger("GUI")

version = gui_settings.VERSION
hardware_interface = flc_settings.HARDWARE_INTERFACE
show_logo = gui_settings.LOGO

class DelayLineChannel(QWidget):

    def __init__(self, parent: QWidget | None = None, name: str = "", width: int = DELAYLINE_WINDOW_WIDTH, height: int = LEVEL_2_TAB_WIDGET_HEIGHT, channel: int = -1, label: str = "DELAY LINE X", value: int | float = 0, min_value: int = 0, max_value: int = 10000, step: int = 5, default_unit: str = "ps", units: list[str] = ["ps", "ns"], font: str = fontfamily, fontsize: int = fontsize_huge, font_bold: bool = True):
        super().__init__(parent)

        if default_unit not in units:
            raise ValueError("Default unit must be in units list")
        
        if default_unit == units[1]:
            value = value * 1000
            default_unit = units[0]
            
        self.channel = channel
        self.label = label
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.unit = default_unit
        self.units = units
        self.step = step
         
        widget_height = BUTTON_HEIGHT

        if width >= DELAYLINE_WINDOW_WIDTH:
            widget_width = 2 * width // 3
        else:
            widget_width = width - 10

        self.name = name
        self.setObjectName(u"channelWidget")

        channel_grid = QGridLayout(self)
        channel_grid.setSpacing(5)
        channel_grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(channel_grid)

        if height - DAC_GROUP_DELAYLINE_HEIGHT > 3 * BUTTON_HEIGHT:
            widget_height = BUTTON_HEIGHT
            self.channel_label = Label(self)
            self.channel_label.configure(name="Channel_label", text=self.label, width=widget_width, height=widget_height, bg="transparent", fg=C_text_dark, border=2, border_color="transparent", border_radius=0, font=font, font_size=fontsize, font_bold=font_bold)
            channel_grid.addWidget(self.channel_label, 0, 0, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.channel_value_entry = DACGroupDelayline(self, -1)
        self.channel_value_entry.configure(name=name, text=f"{self.value} {self.unit}", bg=C_main_background, width=width-20, height=DAC_GROUP_DELAYLINE_HEIGHT, border_radius=0, border=2, border_color=C_button_on, font=font, font_size=fontsize, font_bold=font_bold)
        self.channel_value_entry.set_callback(self.set_delay)
        channel_grid.addWidget(self.channel_value_entry, 1, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)

        if height - DAC_GROUP_DELAYLINE_HEIGHT > 5 * BUTTON_HEIGHT:
            self.channel_reset_button = PushButton(self)
            self.channel_reset_button.configure(name="channel_reset_button", text="RESET", bg="transparent", fg=C_main_text, checked_bg="transparent", checked_fg=C_button_on, width=widget_width, height=widget_height, border_radius=widget_height, font=font, font_size=fontsize, font_bold=font_bold)
            self.channel_reset_button.set_callback(lambda: self.reset(channel=channel))
            channel_grid.addWidget(self.channel_reset_button, 2, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)


    def open_numpad(self):
        numpad = Numpad(callback=self.set_delay, value=0, unit=self.unit, units=self.units)
        numpad.show()


    def set_delay(self, value: float | int, unit: str):
        """
        Sets the delay of the delay line in ns. If the delay is set in ns the value is multiplied by 1000 and set to ps.
        The value is then sent to the hardware interface callback function to set the delay line.
        """
        self.calculate_delay(value, unit)
        self.unit = self.units[0]
        print(f"Setting delay to {self.value} {self.unit}")

        logger.info(f"Setting delay to {self.value} {self.unit}")
        self.channel_value_entry.set_text(f"{self.value} {self.unit}")
        self.channel_value_entry.update()

        self.callback(value=self.value, unit=self.unit, channel=self.channel)

    def reset(self, channel: int):
        logger.info(f"Resetting delay line {channel}")

        self.value = 0
        self.unit = "ps"
        self.channel_value_entry.set_text(f"{self.value} {self.unit}")
        self.channel_value_entry.update()

        self.callback(value=0, unit="ps", channel=channel)

    def set_callback(self, callback, *args, **kwargs):
        self.callback = callback

    def calculate_delay(self, value: float | int, unit: str):
        """Calculate delay in ps."""
        if unit == self.units[1]:
            self.value = int(value * 1000)
            self.unit = self.units[0]
        else:
            self.value = int(value)

        if not self.value % self.step == 0:
            self.value = self.value - self.value % self.step
        
    def set_step(self, step: int):
        self.step = step

    def sync_values(self, value: int):
        self.value = value
        self.channel_value_entry.set_text(f"{self.value} {self.unit}")
        self.channel_value_entry.sync_value(self.value)
        self.channel_value_entry.update()

    def enable_channel(self, enabled: bool):
        if enabled:
            self.channel_value_entry.set_enabled(True)
            if self.channel_reset_button:
                self.channel_reset_button.set_enabled(True)
            if self.channel_label:
                self.channel_label.set_text_color(C_text_dark)
        else:
            self.channel_value_entry.set_enabled(False)
            if self.channel_reset_button:    
                self.channel_reset_button.set_enabled(False)
            if self.channel_label:
                self.channel_label.set_text_color(UI_GRAY)