import os
from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from src.GUI.widgets.push_button_ui import PushButton
from src.GUI.widgets.tab_view_ui import TabView
from src.GUI.constants.ui_colors import *
from src.GUI.constants.ui_geometry import *
from src.GUI.constants.ui_fonts import *
import src.configs.gui_settings as gui_settings
import src.configs.settings as settings
from src.GUI.constants.config import DEFAULT_SETTINGS_PATH, OVERRIDE_SETTINGS_PATH, GENERAL_ICON_PATH
from src.utils.logger import get_logger
from src.utils.load_config import load_config



logger = get_logger("GUI")

interface = settings.HARDWARE_INTERFACE
general_icon_path = GENERAL_ICON_PATH
        
class SettingsWindow(QMainWindow):

    def __init__(self, parent: QWidget | QMainWindow):
        super().__init__(parent)

        self.settings_dict = load_config(DEFAULT_SETTINGS_PATH, OVERRIDE_SETTINGS_PATH)

        self.setWindowTitle("Settings")
        self.setObjectName("SettingsToplevel")
        self.setWindowIcon(QIcon(os.path.join(general_icon_path,"folas_logo.svg")))
        # if interface == "RASPBERRY_PI":
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
            
        self.setFixedSize(SETTINGS_WINDOW_WIDTH, SETTINGS_WINDOW_HEIGHT)
        if interface == "RASPBERRY_PI":
            self.move((width-SETTINGS_WINDOW_WIDTH)//2, (height-SETTINGS_VIEW_HEIGHT)//2)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setStyleSheet(f"""
                            #SettingsToplevel {{
                            background-color: transparent;
                            border: 0px solid transparent;
                            border-radius: 20px;
                            }}
                            """)

        settings_central_widget = QWidget(self)
        settings_central_widget.setObjectName(u"CentralSettingsWidget")
        settings_central_widget.setStyleSheet(f"""
                                        #CentralSettingsWidget {{
                                        background-color: {C_main_background};
                                        border: 2px solid {C_button_off};
                                        border-radius: 0px;
                                        }}
                                        """)
        settings_central_widget.setFixedSize(SETTINGS_WINDOW_WIDTH, SETTINGS_WINDOW_HEIGHT)
        settings_central_grid = QGridLayout(settings_central_widget)
        settings_central_grid.setSpacing(2)
        settings_central_grid.setContentsMargins(10, 10, 10, 10)
        settings_central_widget.setLayout(settings_central_grid)

        self.setCentralWidget(settings_central_widget)


        settings_tab_view = TabView(settings_central_widget)
        settings_tab_view.configure(width=SETTINGS_WINDOW_WIDTH-20, height=SETTINGS_WINDOW_HEIGHT-20, tabwidth=TAB_WIDTH, tabheight=TAB_HEIGHT, bg=C_main_background, bg_selected=C_tab_selected_l2, bg_unselected=C_tab_unselected_l2, fg_selected=C_text_dark, fg_unselected=C_text_light, top_radius=8, bottom_radius=8, tabs_closable=False)
        settings_tab_view.add_tab(QWidget(), "General")
        settings_tab_view.add_tab(QWidget(), "Interface")

        settings_central_grid.addWidget(settings_tab_view, 0, 0, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        save_button = PushButton(settings_central_widget)
        save_button.configure(name="save_button", text="Exit", bg=C_button_off, fg=C_text_dark, width=BUTTON_WIDTH, height=int(scale_factor*BUTTON_HEIGHT), border_radius=BUTTON_HEIGHT//2, font=fontfamily, font_size=fontsize_normal, font_bold=True)
        save_button.set_callback(lambda: self.save_settings())
        settings_central_grid.addWidget(save_button, 1, 0, 1, 1, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        

        self.show()

    def save_settings(self):
        logger.info("Saving settings, refreshing UI.")
        self.close()
        pass
