import src.configs.gui_settings as gui_settings
from src.configs.settings import INTERFACE_CHAIN_DRIVER_PATH_TO_EXCEL
# import src.GUI.init_ui as ui
fullscreen = gui_settings.FULLSCREEN

def get_screen_size() -> tuple[int,int,int]:
    # from PySide6.QtGui import QGuiApplication
    from app import app
    screen = app.primaryScreen()
    if screen:
        w = screen.size().width()
        h = screen.size().height()
    else:
        w = gui_settings.WINDOW_WIDTH
        h = gui_settings.WINDOW_HEIGHT
    return w, h, 1 if gui_settings.FULLSCREEN else 0
    
    

    return width, height, 1 if gui_settings.FULLSCREEN else 0

width, height, _ = get_screen_size()

button_size_default = [100, 28]
label_size_default = [100, 25]
tab_size_default = [75, 35]
signal_light_size_default = [100, 28]
checkbox_size_default = [100, 28]
dropdown_size_default = [100, 22]
dropdown_item_size_default = 35
menu_button_size_default = [150, 22]
operator_button_size_default = [25, 25]
plotwidget_size_default = [140, 28]
text_entry_size_default = [70, 22]
dac_group_size_default = [150, 60]
adc_group_size_default = [150, 30]
pulse_gen_plot_size_default = [630, 140]
pulse_param_setter_size_default = [500, 400]
numpad_size_default = [240, 200]
overview_row_height = 25
safety_console_output_size_default = [500, 300]
dac_group_delayline_size_default = [0, 70]
icon_size_default = [7, 7]
icon_size_large = [16, 16]

# Define the geometry by views for screens of 800px, 1400px and 1920px wide
if not fullscreen == 1:
    width = gui_settings.WINDOW_WIDTH
    height = gui_settings.WINDOW_HEIGHT

if width < 801:
    scale_factor = 1
    OVERVIEW_PANEL_WIDTH = 152
elif width < 1401:
    scale_factor = 1.4
    OVERVIEW_PANEL_WIDTH = 216
else:
    scale_factor = 1.6
    OVERVIEW_PANEL_WIDTH = 244

MAIN_WINDOW_WIDTH = width
MAIN_WINDOW_HEIGHT = height
MAIN_VIEW_HEIGHT = MAIN_WINDOW_HEIGHT

OVERVIEW_PANEL_HEIGHT = MAIN_WINDOW_HEIGHT

SETTINGS_WINDOW_WIDTH = width - int(scale_factor * 250)
SETTINGS_WINDOW_HEIGHT = height - int(scale_factor * 100)
SETTINGS_VIEW_HEIGHT = SETTINGS_WINDOW_HEIGHT - 100
SETTINGS_VIEW_WIDTH = SETTINGS_WINDOW_WIDTH - 30

POWERMETER_WINDOW_WIDTH = int(scale_factor * 200)
POWERMETER_WINDOW_HEIGHT = int(scale_factor * 220)
POWERMETER_VIEW_HEIGHT = POWERMETER_WINDOW_HEIGHT
POWERMETER_VIEW_WIDTH = POWERMETER_WINDOW_WIDTH

MAIN_VIEW_WIDTH = MAIN_WINDOW_WIDTH - OVERVIEW_PANEL_WIDTH

OVERVIEW_LOGO_WIDTH = OVERVIEW_PANEL_WIDTH
OVERVIEW_LOGO_HEIGHT = round(scale_factor * 100)

OVERVIEW_MENU_HEIGHT = round(scale_factor * 90)

OVERVIEW_ROW_HEIGHT = round(scale_factor * overview_row_height)

OVERVIEW_WIDGET_WIDTH = OVERVIEW_PANEL_WIDTH
OVERVIEW_WIDGET_HEIGHT = OVERVIEW_PANEL_HEIGHT - OVERVIEW_LOGO_HEIGHT - OVERVIEW_MENU_HEIGHT

BUTTON_WIDTH = round(scale_factor * button_size_default[0])
BUTTON_HEIGHT = round(scale_factor * button_size_default[1])

LABEL_WIDTH = round(scale_factor * label_size_default[0])
LABEL_HEIGHT = round(scale_factor * label_size_default[1])

TAB_WIDTH = round(scale_factor * tab_size_default[0])
TAB_HEIGHT = tab_size_default[1]
if height > 480:
    TAB_HEIGHT = 55
elif height > 720:
    TAB_HEIGHT = 70

SIGNAL_LIGHT_WIDTH = round(scale_factor * signal_light_size_default[0])
SIGNAL_LIGHT_HEIGHT = round(scale_factor * signal_light_size_default[1])

CHECKBOX_WIDTH = round(scale_factor * checkbox_size_default[0])
CHECKBOX_HEIGHT = round(scale_factor * checkbox_size_default[1])

DROPDOWN_WIDTH = round(scale_factor * dropdown_size_default[0])
DROPDOWN_HEIGHT = round(scale_factor * dropdown_size_default[1])

DROPDOWN_ITEM_HEIGHT = round(scale_factor * dropdown_item_size_default)

MENU_BUTTON_WIDTH = round(scale_factor * menu_button_size_default[0])
MENU_BUTTON_HEIGHT = round(scale_factor * menu_button_size_default[1])

OPERATOR_BUTTON_WIDTH = round(scale_factor * operator_button_size_default[0])
OPERATOR_BUTTON_HEIGHT = round(scale_factor * operator_button_size_default[1])

PLOTWIDGET_WIDTH = round(scale_factor * plotwidget_size_default[0])
PLOTWIDGET_HEIGHT = round(scale_factor * plotwidget_size_default[1])

TEXT_ENTRY_WIDTH = round(scale_factor * text_entry_size_default[0])
TEXT_ENTRY_HEIGHT = round(scale_factor * text_entry_size_default[1])

DAC_GROUP_WIDTH = round(scale_factor * dac_group_size_default[0])
DAC_GROUP_HEIGHT = round(scale_factor * dac_group_size_default[1])

ADC_GROUP_WIDTH = round(scale_factor * adc_group_size_default[0])
ADC_GROUP_HEIGHT = round(scale_factor * adc_group_size_default[1])

PULSE_GEN_PLOT_WIDTH = round(scale_factor * pulse_gen_plot_size_default[0])
PULSE_GEN_PLOT_HEIGHT = round(scale_factor * pulse_gen_plot_size_default[1])

LEVEL_1_TAB_WIDGET_WIDTH = MAIN_VIEW_WIDTH
LEVEL_1_TAB_WIDGET_HEIGHT = MAIN_VIEW_HEIGHT - (TAB_HEIGHT + round(scale_factor * 5))

LEVEL_2_TAB_WIDGET_WIDTH = MAIN_VIEW_WIDTH
LEVEL_2_TAB_WIDGET_HEIGHT = MAIN_VIEW_HEIGHT - 2 * (TAB_HEIGHT + round(scale_factor * 5))

# DELAYLINE
DELAYLINE_WINDOW_WIDTH = (MAIN_VIEW_WIDTH-round(scale_factor * 20))//3

DAC_GROUP_DELAYLINE_HEIGHT = round(scale_factor * dac_group_delayline_size_default[1])

# PULSE GENERATOR
PULSE_PARAM_GROUP_WIDTH = round(scale_factor * pulse_gen_plot_size_default[0])
PULSE_PARAM_GROUP_HEIGHT = round(scale_factor * pulse_gen_plot_size_default[1])

PULSE_GEN_CHANNEL_SELECT_WIDTH = 5 * LABEL_WIDTH + round(scale_factor * 5)
PULSE_GEN_CHANNEL_SELECT_HEIGHT = PULSE_PARAM_GROUP_HEIGHT

# ADC CONTROL
ADC_TABVIEW_WIDTH = LEVEL_1_TAB_WIDGET_WIDTH - int(scale_factor*200)
ADC_TABVIEW_HEIGHT = LEVEL_1_TAB_WIDGET_HEIGHT - int(scale_factor*100)

ADC_PLOT_WIDTH = ADC_TABVIEW_WIDTH - round(scale_factor * 40)
ADC_PLOT_HEIGHT = ADC_TABVIEW_HEIGHT - round(scale_factor * 100)

NUMPAD_WIDGET_WIDTH = round(scale_factor * numpad_size_default[0])
NUMPAD_WIDGET_HEIGHT = round(scale_factor * numpad_size_default[1])

#SAFETY
SAFETY_CONSOLE_WIDTH = round(scale_factor * safety_console_output_size_default[0])
SAFETY_CONSOLE_HEIGHT = round(scale_factor * safety_console_output_size_default[1])

#OTHER

ICON_WIDTH = round(scale_factor * icon_size_default[0])
ICON_HEIGHT = round(scale_factor * icon_size_default[1])

ICON_WIDTH_LARGE = round(scale_factor * icon_size_large[0])
ICON_HEIGHT_LARGE = round(scale_factor * icon_size_large[1])

SCROLLBAR_WIDTH = int(scale_factor*8)