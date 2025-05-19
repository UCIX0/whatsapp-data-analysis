import hydralit_components as hc

# Opciones disponibles en la barra de navegación
OPTION_DATA = [
    {'icon': "fa fa-table", 'label': "Tables"},
    {'icon': "fa fa-chart-line", 'label': "Visualization"},
]

# Tema personalizado para los colores de la barra de navegación
THEME = {
    'txc_inactive': '#06202B',       # Texto inactivo
    'menu_background': '#F5EEDD',    # Fondo del menú
    'txc_active': '#F5EEDD',         # Texto activo
    'option_active': '#06202B'       # Fondo de opción activa
}


def draw_optionbar() -> str:
    """
    Dibuja una barra de navegación horizontal usando Hydralit Components.

    Retorna:
    -------
    str
        Opción seleccionada por el usuario ('Tables' o 'Visualization').
        Esta cadena se puede usar para controlar qué sección de la app mostrar.
    """
    return hc.option_bar(
        option_definition=OPTION_DATA,
        title='',
        key='NavBarOption',
        override_theme=THEME,
        horizontal_orientation=True
    )
