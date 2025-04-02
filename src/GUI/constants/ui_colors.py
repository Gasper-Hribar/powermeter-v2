
UI_BLACK = "#070F0A"
UI_WHITE = "#FFFFFF"
UI_OCHRE = "#E27616"
UI_SMOKY_BLACK = "#14160A"
UI_SHAMROCK_GREEN = "#3C9B71"
UI_EMERALD_GREEN = "#6CD381"
UI_PALE_DOGWOOD = "#E4CCC7"
UI_LIGHTER_GRAY = "#E7E7E8"
UI_LIGHT_GRAY = "#C9C1CA"
UI_GRAY = "#8A8D91"
UI_DARK_GRAY = "#3E403F"
UI_RED = '#EE4539'  # "#F23A22"
UI_ORANGE = "#FF7F11"
UI_LIGHT_GREEN = "#6CD381"
UI_DARK_GREEN = "#3C9B71"
alpha = "AF"
PLOT_RED = UI_RED+alpha
PLOT_VIOLET = "#9467bd"+alpha
PLOT_GREEN = "#2ca02c"+alpha
PLOT_ORANGE = "#ff7f0e"+alpha
PLOT_CYAN = "#17becf"+alpha
PLOT_BLUE = "#1f77b4"+alpha
PLOT_BROWN = "#8c564b"+alpha
PLOT_PINK = "#e377c2"+alpha

COLOR_SCHEME = {
    "LIGHT": {
        "BACKGROUND": UI_WHITE,
        "TEXT": UI_BLACK,
        "TEXT_LIGHT": UI_WHITE,
        "TEXT_DARK": UI_BLACK,
        "OVERVIEW_BG": UI_DARK_GRAY,
        "TAB_SELECTED_L1": UI_RED,
        "TAB_UNSELECTED_L1": UI_LIGHT_GRAY,
        "TAB_SELECTED_L2": UI_LIGHTER_GRAY,
        "TAB_UNSELECTED_L2": UI_DARK_GRAY,
        "ALARM": UI_RED,
        "BUTTON_OFF": UI_LIGHT_GRAY,
        "BUTTON_ON": UI_RED,
        "ADC_LABEL_BG": UI_WHITE,
        "ADC_LABEL_FG": UI_BLACK,
        "ADC_LABEL_BORDER": UI_GRAY,
        "DAC_LABEL_BG": UI_WHITE,
        "DAC_LABEL_FG": UI_BLACK,
        "DAC_LABEL_BORDER": UI_RED,
        "PLOT_RED": PLOT_RED,
        "PLOT_VIOLET": PLOT_VIOLET,
        "PLOT_GREEN": PLOT_GREEN,
        "PLOT_ORANGE": PLOT_ORANGE,
        "PLOT_CYAN": PLOT_CYAN,
        "PLOT_BLUE": PLOT_BLUE,
        "PLOT_BROWN": PLOT_BROWN,
        "PLOT_PINK": PLOT_PINK
    },
    "DARK": {
        "BACKGROUND": UI_WHITE,
        "TEXT": UI_BLACK,
        "TEXT_LIGHT": UI_WHITE,
        "TEXT_DARK": UI_BLACK,
        "OVERVIEW_BG": UI_BLACK,
        "TAB_SELECTED_L1": UI_ORANGE,
        "TAB_UNSELECTED_L1": UI_LIGHT_GRAY,
        "TAB_SELECTED_L2": UI_WHITE,
        "TAB_UNSELECTED_L2": UI_BLACK,
        "ALARM": UI_RED,
        "BUTTON_OFF": UI_LIGHT_GRAY,
        "BUTTON_ON": UI_RED,
        "ADC_LABEL_BG": UI_WHITE,
        "ADC_LABEL_FG": UI_BLACK,
        "ADC_LABEL_BORDER": UI_GRAY,
        "DAC_LABEL_BG": UI_WHITE,
        "DAC_LABEL_FG": UI_BLACK,
        "DAC_LABEL_BORDER": UI_RED,
        "PLOT_RED": PLOT_RED,
        "PLOT_VIOLET": PLOT_VIOLET,
        "PLOT_GREEN": PLOT_GREEN,
        "PLOT_ORANGE": PLOT_ORANGE,
        "PLOT_CYAN": PLOT_CYAN,
        "PLOT_BLUE": PLOT_BLUE,
        "PLOT_BROWN": PLOT_BROWN,
        "PLOT_PINK": PLOT_PINK
    }}

def get_color(color_name, color_scheme: str = "LIGHT"):
    return COLOR_SCHEME[color_scheme][color_name]

C_main_text = get_color("TEXT")
C_main_background = get_color("BACKGROUND")
C_button_off = get_color("BUTTON_OFF")
C_button_on = get_color("BUTTON_ON")
C_tab_selected = get_color("TAB_SELECTED_L1")
C_tab_unselected = get_color("TAB_UNSELECTED_L1")
C_tab_selected_l2 = get_color("TAB_SELECTED_L2")
C_tab_unselected_l2 = get_color("TAB_UNSELECTED_L2")
C_alarm_color = get_color("ALARM")
C_text_light = get_color("TEXT_LIGHT")
C_text_dark = get_color("TEXT_DARK")
C_overview_background = get_color("OVERVIEW_BG")
C_alarm = get_color("ALARM")
C_adc_label_bg = get_color("ADC_LABEL_BG")
C_adc_label_fg = get_color("ADC_LABEL_FG")
C_adc_label_border = get_color("ADC_LABEL_BORDER")
C_dac_label_bg = get_color("DAC_LABEL_BG")
C_dac_label_fg = get_color("DAC_LABEL_FG")
C_dac_label_border = get_color("DAC_LABEL_BORDER")
C_delayline_entry_border = get_color("DAC_LABEL_BORDER")
C_plot_channel0 = get_color("PLOT_RED")
C_plot_channel1 = get_color("PLOT_ORANGE")
C_plot_channel2 = get_color("PLOT_CYAN")
C_plot_channel3 = get_color("PLOT_VIOLET")
C_plot_channel4 = get_color("PLOT_GREEN")
C_plot_channel5 = get_color("PLOT_BLUE")
C_plot_channel6 = get_color("PLOT_BROWN")
C_plot_channel7 = get_color("PLOT_PINK")
c_plot_channel_list = [C_plot_channel0, C_plot_channel1, C_plot_channel2, C_plot_channel3, C_plot_channel4, C_plot_channel5, C_plot_channel6, C_plot_channel7]