import docker
from tabulate import tabulate
from termcolor import colored


def list_tangent(client, config=None, name=None, running=False, stopped=False):
    try:
        tangent_id = config.get("tangent_id")
        filters = {"label": f"tangent_id={tangent_id}"}
        containers = client.containers.list(all=True, filters=filters)

        if running:
            containers = [container for container in containers if container.status == "running"]
        elif stopped:
            containers = [container for container in containers if container.status != "running"]
        elif name:
            containers = [container for container in containers if container.name == name]

        if not containers:
            print("No environments managed by tangent.")
            return

        table_data = []
        for container in containers:
            container_info = {
                "Name": container.name,
                "Status": container.status,
                "IP Address": container.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]
                    if "bridge" in container.attrs["NetworkSettings"]["Networks"]
                    else "N/A",
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