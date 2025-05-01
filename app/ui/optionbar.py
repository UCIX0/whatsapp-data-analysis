import hydralit_components as hc


OPTION_DATA = [
    {'icon': "fa fa-table", 'label': "Tables"},
    {'icon': "fa fa-chart-line", 'label': "Visualization"},
]


THEME = {
    'txc_inactive': '#06202B',
    'menu_background': '#F5EEDD',
    'txc_active': '#F5EEDD',
    'option_active': '#06202B'
}


def draw_optionbar():
    return hc.option_bar(
        option_definition=OPTION_DATA,
        title='',
        key='NavBarOption',
        override_theme=THEME,
        horizontal_orientation=True
    )
