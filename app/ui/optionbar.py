import hydralit_components as hc


OPTION_DATA = [
    {'icon': "fa fa-table", 'label': "Tables"},
    {'icon': "fa fa-chart-line", 'label': "Visualization"},
]


THEME = {
    'txc_inactive': '#FFFFFF',
    'menu_background': '#FF4B4B',
    'txc_active': '#FF4B4B',
    'option_active': '#FFFFFF'
}


def draw_optionbar():
    return hc.option_bar(
        option_definition=OPTION_DATA,
        title='',
        key='NavBarOption',
        override_theme=THEME,
        horizontal_orientation=True
    )
