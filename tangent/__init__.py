import os


def create_config_directory():
    config_dir = os.path.expanduser("~/.config/tangent-cli")
    os.makedirs(config_dir, exist_ok=True)


create_config_directory()
