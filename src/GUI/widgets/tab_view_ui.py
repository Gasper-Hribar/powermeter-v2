from PySide6.QtWidgets import (QTabWidget, QWidget)
from PySide6.QtGui import QFont
from src.GUI.constants.ui_colors import *
from src.GUI.constants.ui_fonts import *
from src.GUI.constants.ui_geometry import *
from src.utils.logger import get_logger


logger = get_logger("GUI")  # type: ignore


class TabView(QTabWidget):

    
    def __init__(self, parent: QWidget):
        super().__init__()


        self.setObjectName(u"tabWidget")
        self.setParent(parent)


    def configure(self, width: int = 650, height: int = 40, tabwidth: int = TAB_WIDTH, tabheight: int = TAB_HEIGHT, bg: str = C_main_background, bg_selected: str = C_tab_selected, bg_unselected: str = C_tab_unselected, fg_selected: str = C_text_dark, fg_unselected: str = C_text_dark, font: str = fontfamily, font_size: int = fontsize_normal, top_radius: int = TAB_HEIGHT//4, bottom_radius: int = 0, tabs_closable: bool = False):
        """
        Configures the tab view with the specified properties.
        Args:
            width (int): The width of the tab view. Defaults to 650.
            height (int): The height of the tab view. Defaults to 40.
            tabwidth (int): The width of the tabs. Defaults to 60.
            tabheight (int): The height of the tabs. Defaults to 35.
            bg (str): The background color of the tab view. Defaults to UI_WHITE.
            bg_selected (str): The background color of the selected tab. Defaults to UI_ORANGE.
            bg_unselected (str): The background color of the unselected tabs. Defaults to UI_LIGHT_GRAY.
            fg_selected (str): The text color of the selected tab. Defaults to UI_BLACK.
            fg_unselected (str): The text color of the unselected tabs. Defaults to UI_BLACK.
            tabs_closable (bool): Whether the tabs should be closable. Defaults to False.
        """


        if tabs_closable:
            self.setTabsClosable(True)
            self.tabCloseRequested.connect(self.close_tab)

        self.setFont(QFont(font, font_size, QFont.Weight.ExtraBold))

        self.setStyleSheet(f"""
                           #tabWidget {{
                                background-color: {bg}; /* No background color */
                           }}
                            QTabBar {{
                                background-color: transparent; /* No background color */
                                border: 0px solid transparent; /* No border around the tab content area */
                                margin: 0px; /* No margin around the tab content area */
                                width: {width}px; /* Full width */
                            }}

                            QTabWidget::pane {{
                                border: 0px solid transparent; /* No border around the tab widget */
                                margin: 0px; /* No margin around the tab widget */
                                background-color: transparent;
                                width: {width}px; /* Full width */
                            }}

                            QTabBar::tab {{
                                width: {tabwidth}px;; 
                                height: {tabheight}px;
                                background-color: {bg_unselected};
                                color: {fg_unselected};
                                border: none;
                                border-top-left-radius: 8px;
                                border-top-right-radius: 8px;
                                margin-top: 2px; /* Optional: vertical padding */
                                margin-right: 3px; /* Optional: spacing between tabs */
                            }}

                            QTabBar::tab:selected {{
                                background-color: {bg_selected};
                                color: {fg_selected};
                                border-top-left-radius: {top_radius}px;
                                border-top-right-radius: {top_radius}px;
                                border-bottom-left-radius: {bottom_radius}px;
                                border-bottom-right-radius: {bottom_radius}px;
                            }}

                            QTabBar::tab:!selected {{
                                background-color: {bg_unselected};
                                color: {fg_unselected};
                                border-radius: 8px;
                            }}
                            """)

        self.setFixedSize(width, height)

    def add_tab(self, widget: QWidget, title: str = "Tab", override_width: int = 0, override_height: int = 0):
        
        if override_width > 0 and override_height > 0:
            widget.setFixedSize(override_width, override_height)
            
        self.addTab(widget, title)

    def close_tab(self, index):
        self.removeTab(index)
        self.widget(index).deleteLater()