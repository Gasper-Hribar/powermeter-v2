from src.configs import gui_settings

def get_screen_size() -> tuple[int,int,int]:
    from app import app
    screen = app.primaryScreen()
    if screen:
        w = screen.size().width()
        h = screen.size().height()
    else:
        w = gui_settings.WINDOW_WIDTH
        h = gui_settings.WINDOW_HEIGHT
    return w, h, 1 if gui_settings.FULLSCREEN else 0

width, height, fullscreen= get_screen_size()

if not gui_settings.FULLSCREEN == 1:
    width = gui_settings.WINDOW_WIDTH
    height = gui_settings.WINDOW_HEIGHT

if width <= 800:
    add_to_font = 0
elif width <= 1400:
    add_to_font = 4
else:
    add_to_font = 6

fontfamily = gui_settings.FONT
fontsize_tiny = round(add_to_font + gui_settings.FONTSIZES["fontsize_tiny"])
fontsize_normal = round(add_to_font + gui_settings.FONTSIZES["fontsize_normal"])
fontsize_large = round(add_to_font + gui_settings.FONTSIZES["fontsize_large"])
fontsize_small = round(add_to_font + gui_settings.FONTSIZES["fontsize_small"])
fontsize_huge = round(add_to_font + gui_settings.FONTSIZES["fontsize_huge"])

normal = "Lato 18"
titles = "Lato 22 bold"
outputfont = "Lato 36 bold"
outputminifont = "Lato 16 bold"
normalminifont = "Lato 16"
menufont = "Lato 16 bold"
settingsfont = "Lato 14"
ampfont = "Lato 12"