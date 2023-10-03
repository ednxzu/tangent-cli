import os
import yaml
import uuid

default_config = {
    "volume_host_path": "~/.tangent-cli.d",
    "volume_container_path": "/mnt/host",
}


def get_or_generate_tangent_id(config_path):
    if os.path.exists(config_path):
        with open(config_path, "r") as config_file:
            config_data = yaml.safe_load(config_file)
            if "tangent_id" in config_data:
                tangent_id = config_data["tangent_id"]
                if is_valid_uuid(tangent_id):
                    return tangent_id

    new_uuid = str(uuid.uuid4())
    with open(config_path, "w") as config_file:
        yaml.dump({"tangent_id": new_uuid}, config_file)

    return new_uuid


def is_valid_uuid(uuid_str):
    try:
        uuid.UUID(uuid_str)
        return True
    except ValueError:
        return False


def load_config():
    config = default_config.copy()
    config_dir = os.path.expanduser("~/.config/tangent-cli")
    os.makedirs(config_dir, exist_ok=True)  # Create ~/.config/tangent-cli if it doesn't exist

    config_path = os.path.join(config_dir, "config.yml")

    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            user_config = yaml.safe_load(f)
            if user_config:
                config.update(user_config)

    tangent_id = get_or_generate_tangent_id(config_path)
    config["tangent_id"] = tangent_id

    volume_host_path = os.path.expanduser(config.get('volume_host_path'))
    os.makedirs(volume_host_path, exist_ok=True)

    return config
