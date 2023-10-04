import docker
import dockerpty
import os
from names_generator import generate_name
from tangent.functions.list import list_tangent


def tangent_name_is_unique(client, tangent_id, name):
    existing_containers = client.containers.list(
        all=True, filters={"label": f"tangent_id={tangent_id}"}
    )
    existing_container_names = [container.name for container in existing_containers]
    return name not in existing_container_names


def create_tangent(
    distribution,
    client,
    connect=False,
    name=None,
    shell="/bin/bash",
    config=None,
    create_volume=False,
):
    try:
        container_image_name = f"geerlingguy/docker-{distribution}-ansible"
        container_image = client.images.pull(container_image_name)

        if name:
            if not tangent_name_is_unique(client, config.get("tangent_id"), name):
                print(f"Error: Container name '{name}' is not unique.")
                return None
        else:
            name = generate_name()

        volumes = {"/sys/fs/cgroup": {"bind": "/sys/fs/cgroup", "mode": "rw"}}

        volume_path = None

        if create_volume:
            volume_host_path = os.path.expanduser(config.get("volume_host_path"))
            os.makedirs(volume_host_path, exist_ok=True)
            volume_name = f"volume_{name}"
            volume_path = os.path.join(volume_host_path, volume_name)
            client.volumes.create(name=volume_name)
            volumes[volume_path] = {
                "bind": config.get("volume_container_path"),
                "mode": "rw",
            }

        container = client.containers.create(
            container_image,
            name=name,
            detach=True,
            privileged=True,
            volumes=volumes,
            cgroupns="host",
            labels={"tangent_id": config.get("tangent_id")},
        )

        start_tangent(name=name, config=config, client=client, connect=connect, shell=shell)

        return container, volume_path
    except docker.errors.APIError as e:
        print(f"Error: Failed to create the test environment - {e}")
        return None, None


def start_tangent(name, config, client, connect=False, shell="/bin/bash"):
    try:
        container = client.containers.get(name)

        if (
            "tangent_id" in container.labels
            and container.labels["tangent_id"] == config.get("tangent_id")
        ):
            if container.status != "running":
                container.start()
                list_tangent(client=client, config=config, name=name)
                if connect:
                    connect_tangent(name=name, config=config, client=client, shell=shell)
            else:
                print(f"Error: Container '{name}' is already running.")
    except docker.errors.APIError as e:
        print(f"Error: Failed to start to the container - {e}")


def connect_tangent(name, config, client, shell="/bin/bash"):
    try:
        container = client.containers.get(name)

        if (
            "tangent_id" in container.labels
            and container.labels["tangent_id"] == config.get("tangent_id")
        ):
            if container.status == "running":
                dockerpty.exec_command(client.api, container.id, shell)
            else:
                print(f"Error: Container '{name}' is not running.")
        else:
            print(
                f"Error: Container '{name}' either does not have the 'tangent_id' label or the label value does not match the specified 'tangent_id'."
            )
    except docker.errors.APIError as e:
        print(f"Error: Failed to connect to the container - {e}")


def create_volumes_directory():
    config_dir = os.path.expanduser("~/.config/tangent-cli")
    volumes_dir = os.path.join(config_dir, "volumes")

    if not os.path.exists(volumes_dir):
        os.makedirs(volumes_dir)
