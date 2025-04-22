import re
import yaml
import pandas as pd

import os


# Ruta basada en la ubicación de este script
base_dir = os.path.dirname(os.path.abspath(__file__))
yaml_path = os.path.join(base_dir, 'config.yaml')


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina filas con valores faltantes y mensajes de sistema definidos en un YAML.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame de entrada, debe contener al menos la columna 'message'.

    Returns
    -------
    pd.DataFrame
        Nuevo DataFrame sin filas con NaN y sin los mensajes de sistema.

    Raises
    ------
    Exception
        Para cualquier otro error durante el proceso.
    """
    try:
        df = df.copy()

        df.dropna(inplace=True)

        with open(yaml_path, encoding="utf-8") as f:
            config_yaml = yaml.safe_load(f)

        skip_dict = config_yaml.get("skip_messages", {})
        patterns = []
        for entry in skip_dict.values():
            patterns.extend(entry.values())
        if not patterns:
            return df.reset_index(drop=True)

        escaped = [re.escape(p) for p in patterns]
        regex = r"(?:" + "|".join(escaped) + r")"

        mask = df["message"].str.contains(regex, case=False, na=False, regex=True)
        df_filtered = df[~mask].reset_index(drop=True)

        return df_filtered

    except Exception as e:
        raise Exception(f"Error al limpiar el DataFrame: {e}") from e
