import docker

# Create a Docker client
client = docker.from_env()

# Specify the container ID or name
container_id = "haproxy-03"

# Get a reference to the container
container = client.containers.get(container_id)

# Get information about the container
container_info = container.attrs

# Get the volumes attached to the container
volumes = container_info["HostConfig"]['VolumeDriver']

volume_name = f"volume_{container_id}"
volumes = client.volumes.list(filters={"name": volume_name})
print(volumes[0])

# Print the list of volumes
for volume in volumes:
    #if "/home/lanson/.tangent-cli.d/volume_haproxy-03" in volume:
    print(volume)