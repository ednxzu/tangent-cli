import docker
from tabulate import tabulate
from termcolor import colored


def list_containers_by_uuid(tangent_id, running=False, stopped=False):
    try:
        client = docker.from_env()
        filters = {"label": f"tangent_id={tangent_id}"}
        containers = client.containers.list(all=True, filters=filters)

        if running and stopped:
            print("Error: You cannot use both --running and --stopped flags simultaneously.")
            return

        if running:
            containers = [container for container in containers if container.status == "running"]
        elif stopped:
            containers = [container for container in containers if container.status != "running"]

        if not containers:
            print("No environments managed by tangent.")
            return

        table_data = []
        for container in containers:
            container_info = {
                "Name": container.name,
                "Status": container.status,
                "Created": container.attrs["Created"],
            }
            status_colored = (
                colored("✔", "green")
                if container.status == "running"
                else colored("✘", "red")
            )
            container_info["Status"] = status_colored + " " + container_info["Status"]
            table_data.append(container_info)

        table = tabulate(table_data, headers="keys", tablefmt="pretty")
        print(table)
    except docker.errors.APIError as e:
        print(f"Error: Failed to list containers - {e}")
