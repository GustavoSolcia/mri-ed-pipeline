"""Functions for configuration management."""

import pathlib
import yaml


def load_config(config_path: pathlib.Path) -> dict:
    """Safe loads configuration file structured as yaml file.

    Args:
        config_path (pathlib.Path): Configuration path.

    Returns:
        config_dict (dict): Configuration dictionary.
    """

    with open(config_path) as stream:
        try:
            config_dict = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return config_dict
