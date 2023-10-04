import docker
import os
import shutil


def destroy_tangent(name, client, keep_storage=False, config=None):
    try:
        container = client.containers.get(name)
        tangent_id = container.labels.get("tangent_id", "")
        if tangent_id == config.get("tangent_id"):
            container.stop()
            container.remove()
            # Check if a volume is attached to the container
            volume_name = f"volume_{name}"
            volumes = client.volumes.list(filters={"name": volume_name})

            if volumes:
                # Determine the volume path on the host
                volume_host_path = os.path.expanduser(config.get("volume_host_path"))
                volume_path = os.path.join(volume_host_path, volume_name)
                # Determine the cold storage directory
                cold_storage_dir = os.path.join(volume_host_path, "cold_storage")
                # Ensure that the cold storage directory exists
                os.makedirs(cold_storage_dir, exist_ok=True)
                if keep_storage:
                    # Move the volume directory to cold storage with a timestamp
                    created_at = container.attrs.get("Created", "")
                    new_dir_name = f"{volume_name}_{created_at}"
                    new_dir_path = os.path.join(cold_storage_dir, new_dir_name)
                    shutil.move(volume_path, new_dir_path)
                else:
                    shutil.rmtree(volume_path)

                volumes[0].remove()
        else:
            print("This container is not managed by tangent, not removing")
    except docker.errors.NotFound:
        print(f"Error: Container '{name}' not found.")
    except docker.errors.APIError as e:
        print(f"Error: Failed to destroy the environment - {e}")


def stop_tangent(name, client, config=None):
    try:
        container = client.containers.get(name)
        if "tangent_id" in container.labels and container.labels[
            "tangent_id"
        ] == config.get("tangent_id"):
            if container.status == "running":
                container.stop()
            else:
                print("This container is not running, not stopping")

        else:
            print("This container is not managed by tangent, not stopping")
    except docker.errors.NotFound:
        print(f"Error: Container '{name}' not found.")
    except docker.errors.APIError as e:
        print(f"Error: Failed to stop the environment - {e}")
