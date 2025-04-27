import hydralit_components as hc


OPTION_DATA = [
    {'icon': "fa fa-table", 'label': "Tables"},
    {'icon': "fa fa-chart-line", 'label': "Visualization"},
]


THEME = {
    'txc_inactive': '#ffe6e6',
    'menu_background': '#393356',
    'txc_active': '#393356',
    'option_active': '#ffe6e6'
}


def draw_optionbar():
    return hc.option_bar(
        option_definition=OPTION_DATA,
        title='',
        key='NavBarOption',
        override_theme=THEME,
        horizontal_orientation=True
    )
