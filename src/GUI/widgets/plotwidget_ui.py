from pyqtgraph import PlotWidget, mkPen, AxisItem
from PySide6.QtCore import (Qt, QSize)
from PySide6.QtWidgets import (QWidget, QMainWindow, QGraphicsView)
from PySide6.QtGui import (QFont, QPen, QColor, QBrush)
from src.GUI.schemas.graph_plot_schema import Plot
from src.GUI.constants.ui_colors import *
from src.GUI.constants.ui_fonts import *
from src.GUI.constants.ui_geometry import *
import src.configs.gui_settings as gui_settings
import src.configs.settings as flc_settings
import src.GUI.constants.config as config

version = gui_settings.VERSION
interface = flc_settings.HARDWARE_INTERFACE
general_icon_path = config.GENERAL_ICON_PATH
screen_width = gui_settings.SCREEN_WIDTH
screen_height = gui_settings.SCREEN_HEIGHT

class Graph(PlotWidget):

    def __init__(self, parent: QWidget | QMainWindow):
        super().__init__()
        self.setParent(parent)
        self.setObjectName("graph")
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.max_y = 1.1
        self.min_y = 0
        self.max_x = 0


    def configure(self, name: str = "", labeltext: str = "Graph", bg: str = C_main_background, fg: str = C_text_dark, border: str = C_button_off, posX: int = 0, posY: int = 0, width: int = PLOTWIDGET_WIDTH, height: int = PLOTWIDGET_HEIGHT, border_radius: int = 8, padding: int = 0, font: str = fontfamily, font_size: int = fontsize_small, font_bold: bool = False):
        """
        Configures the graph with the specified properties.
        Args:
            labeltext (str): The text to display on the graph. Defaults to "Graph".
            bg (str): The background color of the graph in its default state. Defaults to transparent.
            fg (str): The foreground (text) color of the graph in its default state. Defaults to UI_BLACK.
            posX (int): The x-coordinate of the graph. Defaults to 0.
            posY (int): The y-coordinate of the graph. Defaults to 0.
            width (int): The width of the graph. Defaults to 140.
            height (int): The height of the graph. Defaults to 25.
            border_radius (int): The radius of the border of the graph. Defaults to 4.
            border (str): The color of the border of the graph. Defaults to UI_GRAY.
            padding (int): The padding of the graph. Defaults to 0.
            font (str): The font of the text displayed on the graph. Defaults to "Lato".
            font_size (int): The size of the font of the text displayed on the graph. Defaults to 10.
            font_bold (bool): Whether the font of the text displayed on the graph should be bold. Defaults to False.
        """


        if not name == "":
            self.setObjectName(name)

        self.setBackground(bg)
        self.setFixedSize(width, height)
        self.setFont(QFont(font, font_size, font_bold))
        self.setYRange(0, 1.1)
        
        self.x_label = AxisItem(orientation='bottom')
        self.y_label = AxisItem(orientation='left')

    def update_plot(self, data: list[Plot], toggle_legend: bool = True, autorange: bool = False):
        self.clear_plot()
        self.max_y = 1.1
        self.min_y = 0
        self.max_x = 0
        for channel in data:
            if channel.visible:
                pen=mkPen(color=channel.color, width=channel.width)
                self.plot(channel.x, channel.y, pen=pen, name=channel.name)
                if min(channel.y) < self.min_y:
                    self.min_y = min(channel.y)
                if max(channel.y) > self.max_y:
                    self.max_y = max(channel.y)
                if max(channel.x) > self.max_x:
                    self.max_x = max(channel.x)

        if toggle_legend:
            self.legend = self.addLegend(offset=(self.width() - int(scale_factor * 150), 0))
            self.legend.setBrush(QColor(255, 255, 255, 150))
            self.legend.setFont(QFont(fontfamily, fontsize_normal))

        if autorange:
            self.setYRange(self.min_y, self.max_y)
            self.setXRange(0, self.max_x)

        self.setAxisItems({'bottom': self.x_label})
        self.setAxisItems({'left': self.y_label})
        
    def clear_plot(self):
        self.clear()

    def set_range(self, plot_range: int | float):
        self.setXRange(-0.05*plot_range*1, plot_range*1.05*1)

    def set_axis_labels(self, x_label: str = "Time", x_unit: str = "s", y_label: str = "", y_unit: str = ""):
        self.x_label.setLabel(text=x_label, units=x_unit)
        self.y_label.setLabel(text=y_label, units=y_unit)
        

class CustomAxisItem(AxisItem):
    def __init__(self, orientation, *args, **kwargs):
        super().__init__(orientation, *args, **kwargs)
        self.unit = "s"
        self.scale_factors = [
            (1e-9, "ns"),
            (1e-6, "µs"),
            (1e-3, "ms"),
            (1, "s"),
        ]

    def updateLabel(self, min_val, max_val):
        """Update the axis label based on the range of values."""
        # Find appropriate unit and scaling factor
        for factor, unit in self.scale_factors:
            if abs(max_val - min_val) >= factor:
                self.unit = unit
                self.scale_factor = factor
                break

        # Update the axis label
        self.setLabel(f"Time ({self.unit})")

    def tickStrings(self, values, scale, spacing):
        """Customize the tick labels to apply the correct scale."""
        # Update the label dynamically based on the current view range
        range_ = self.parentItem().viewRange()
        self.updateLabel(range_[0][0], range_[0][1])

        # Format the tick strings according to the new scale
        print(values)
        return [f"{value / self.scale_factor}" for value in values]
