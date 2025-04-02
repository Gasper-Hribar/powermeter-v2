from PySide6.QtCore import (Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QComboBox, QWidget, QStyledItemDelegate)
from src.GUI.constants.ui_colors import *
from src.GUI.constants.ui_fonts import *
from src.GUI.constants.ui_geometry import *
from src.utils.logger import get_logger


logger = get_logger("GUI")  # type: ignore

class FixedHeightDelegate(QStyledItemDelegate):
    def __init__(self, height, parent=None):
        super().__init__(parent)
        self.height = height

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(self.height)  # Set fixed height
        return size


class DropdownMenu(QComboBox):

    
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setObjectName(u"comboBox")
        self.setParent(parent)


    def configure(self, name: str = "", items: list = [], posX: int = 0, posY: int = 0, width: int = DROPDOWN_WIDTH, height: int = DROPDOWN_HEIGHT, bg: str = C_button_off, fg: str = C_text_dark, bg_selection: str = C_text_dark, border: int = 2, border_radius: int = DROPDOWN_HEIGHT//2, padding: int = 15, font: str = fontfamily, font_size: int = fontsize_normal, font_bold: bool = False):
        """
        Configures the dropdown menu with the specified properties.
        Args:
            items (list): The list of items to display in the dropdown menu.
            posX (int): The x-coordinate of the dropdown menu's position. Defaults to 0.
            posY (int): The y-coordinate of the dropdown menu's position. Defaults to 0.
            width (int): The width of the dropdown menu. Defaults to 100.
            height (int): The height of the dropdown menu. Defaults to 25.
            bg (str): The background color of the dropdown menu. Defaults to UI_LIGHT_GRAY.
            fg (str): The foreground (text) color of the dropdown menu. Defaults to UI_BLACK.
            bg_selection (str): The background color of the selected item in the dropdown menu. Defaults to UI_GRAY.
            font (str): The font family of the dropdown menu. Defaults to "Lato".
            font_size (int): The font size of the dropdown menu. Defaults to 10.
            font_bold (bool): Whether the font should be bold. Defaults to False.
        """

        if not name == "":
            self.setObjectName(name)
        
        self.addItems(items)
        self.setFixedSize(width, height)
        self.move(posX, posY)
        item_size = DROPDOWN_ITEM_HEIGHT
        
        
        self.setEditable(True)
        set_font = QFont(font, font_size)
        set_font.setBold(font_bold)
        self.setFont(set_font)
        self.setStyleSheet(f"""
                            #{self.objectName()} {{
                                background-color: transparent;  /* Background color */
                                color: {fg};     /* Text color */
                                border: {border}px solid {bg};  /* Border color and width */
                                border-radius: {border_radius}px;         /* Rounded corners */
                                padding-left: {padding}px;               /* Padding for inner spacing */
                            }}

                            #{self.objectName()}::drop-down {{
                                border: none;               /* Remove inner drop-down border */
                            }}

                            #{self.objectName()}::down-arrow {{
                                width: 0px;
                                height: 0px;
                                border-left: 0px solid transparent;
                            }}

                            #{self.objectName()} QAbstractItemView {{
                                background-color: {C_main_background};  /* Background color for the drop-down list */
                                color: {fg};     /* Text color for the drop-down list */
                                border: 0px solid #3C6E71;  /* Border for the drop-down list */
                                selection-background-color: {bg}; /* Highlight color when selecting */
                                selection-color: {bg_selection};   /* Text color for the selected item */
                                border-radius: 4px;         /* Rounded corners for the drop-down */

                            }}

                            #{self.objectName()} QAbstractItemView::item {{                            
                                min-height: 60px;
                            }}
                           """)
        
        self._set_active_style(bg, fg, border, bg,  border_radius, padding)
        self._set_disabled_style(UI_LIGHT_GRAY, UI_GRAY, border, bg, border_radius, padding)

        self.setItemDelegate(FixedHeightDelegate(item_size, self))
        self.setEditable(False)


    def get_selected_item(self) -> str:
        """
        Get the currently selected item in the dropdown menu.
        Returns:
            float: The currently selected item.
        """
        return self.currentText()
        
    def set_index(self, index: int):
        """
        Set the index of the selected item in the dropdown menu.
        Args:
            index (int): The index of the item to select.
        """
        if self.currentIndex() != index:
            self.setCurrentIndex(index)
        
    def set_callback(self, callback, *args, **kwargs):
        """
        Assign a callback function to the button.
        Args:
            callback (function): The function to be called when the button is clicked.
        """
        name = kwargs.get("name", "")
        if callable(callback):
            self.currentIndexChanged.connect(lambda: callback(self.get_selected_item(), name=name))
        else:
            raise ValueError("Provided callback is not callable.")
        
    def _set_active_style(self, bg, fg, border, border_color, border_radius, padding):
        self.active_style = f"""
                            #{self.objectName()} {{
                                background-color: transparent;  /* Background color */
                                color: {fg};     /* Text color */
                                border: {border}px solid {border_color};  /* Border color and width */
                                border-radius: {border_radius}px;         /* Rounded corners */
                                padding-left: {padding}px;               /* Padding for inner spacing */
                            }}

                            #{self.objectName()}::drop-down {{
                                border: none;               /* Remove inner drop-down border */
                            }}
                            """
        
    def _set_disabled_style(self, bg, fg, border, border_color, border_radius, padding):
        self.disabled_style = f"""
                            #{self.objectName()} {{
                                background-color: transparent;  /* Background color */
                                color: {fg};     /* Text color */
                                border: {border}px solid {border_color};  /* Border color and width */
                                border-radius: {border_radius}px;         /* Rounded corners */
                                padding-left: {padding}px;               /* Padding for inner spacing */
                            }}

                            #{self.objectName()}::drop-down {{
                                border: none;               /* Remove inner drop-down border */
                            }}
                            """
        
    def set_enabled(self, enabled: bool):
        self.setEnabled(enabled)
        if enabled:
            self.setStyleSheet(self.active_style)
        else:
            self.setStyleSheet(self.disabled_style)
