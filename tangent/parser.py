import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        prog="tangent",
        description="Run simple test environments in docker."
    )
    subparsers = parser.add_subparsers(title="subcommands", dest="action")

    # Create subparser for the 'create' subcommand
    create_parser = subparsers.add_parser("create", help="Create a test environment")
    create_parser.add_argument(
        "--distribution",
        "-d",
        required=True,
        help="Distribution name for the test environment",
    )
    create_parser.add_argument(
        "--name",
        "-n",
        required=False,
        help="Specify a custom name for the container. If not provided, a random name will be assigned by Docker.",
    )
    create_parser.add_argument(
        "--shell",
        "-s",
        default="/bin/bash",
        type=str,
        required=False,
        help="Specify a custom shell to execute inside the container. Defaults to /bin/bash",
    )
    create_parser.add_argument(
        "--connect",
        "-c",
        required=False,
        action="store_true",
        help="Connect to the created environment",
    )
    create_parser.add_argument(
        "--volume",
        "-v",
        required=False,
        help="Create a storage volume in the specified data path (default ~/.tangent-cli.d/) to share data with the environment.",
        action='store_true'
    )

    # Create subparser for the 'destroy' subcommand
    destroy_parser = subparsers.add_parser("destroy", help="Destroy a test environment")
    destroy_parser.add_argument("name", help="Name of the environment to destroy")
    destroy_parser.add_argument(
        "--keep-storage",
        "-k",
        required=False,
        help="Do not wiped the ephemeral volume when deleting the environment",
        action='store_true'
    )

    # Create subparser for the 'list' subcommand
    list_parser = subparsers.add_parser("list", help="List test environments")
    group = list_parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--name",
        "-n",
        help="Name of the environment to stop"
    )
    group.add_argument(
        "--running",
        "-r",
        help="List only the running environments, ignore the stopped ones.",
        action='store_true'
    )
    group.add_argument(
        "--stopped",
        "-s",
        help="List only the stopped environments, ignore the running ones.",
        action='store_true'
    )

    # Create subparser for the 'connect' subcommand
    connect_parser = subparsers.add_parser(
        "connect", help="Connect to a test environment"
    )
    connect_parser.add_argument("name", help="Name of the environment to connect to")
    connect_parser.add_argument(
        "--shell",
        "-s",
        default="/bin/bash",
        type=str,
        required=False,
        help="Specify a custom shell to execute inside the container. Defaults to /bin/bash",
    )

    # Create subparser for the 'stop' subcommand
    stop_parser = subparsers.add_parser(
        "stop", help="Stop a test environment"
    )
    stop_parser.add_argument("name", help="Name of the environment to stop")

    # Create subparser for the 'start' subcommand
    start_parser = subparsers.add_parser(
        "start", help="Stop a test environment"
    )
    start_parser.add_argument("name", help="Name of the environment to stop")
    start_parser.add_argument(
        "--connect",
        "-c",
        required=False,
        action="store_true",
        help="Connect to the environment after starting it",
    )
    start_parser.add_argument(
        "--shell",
        "-s",
        default="/bin/bash",
        type=str,
        required=False,
        help="Specify a custom shell to execute inside the container. Defaults to /bin/bash",
    )
    return parser
