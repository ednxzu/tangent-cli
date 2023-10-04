import argparse
import sys


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
    list_parser.add_argument(
        "--running",
        "-r",
        required=False,
        help="List only the running environments, ignore the stopped ones.",
        action='store_true'
    )
    list_parser.add_argument(
        "--stopped",
        "-s",
        required=False,
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
        required=False,
        help="Specify a custom shell to execute inside the container. Defaults to /bin/bash",
    )

    return parser


# def create_parser():
#     parser = argparse.ArgumentParser(
#         description="Run simple test environments in docker."
#     )
#     parser.add_argument(
#         "action",
#         choices=["create", "destroy", "connect", "list"],
#         help="Action to perform: create, destroy, or list",
#     )
#     parser.add_argument(
#         "--distribution",
#         "-d",
#         required="create" in sys.argv,
#         help="Distribution name for the test environment",
#     )
#     parser.add_argument(
#         "--name",
#         "-n",
#         required=False,
#         help="Specify a custom name for the container. If not provided, a random name will be assigned by Docker.",
#     )
#     parser.add_argument(
#         "--shell",
#         "-s",
#         required=False,
#         help="Specify a custom shell to execute inside the container. Defaults to /bin/bash",
#     )
#     parser.add_argument("--connect", "-c", required="create" in sys.argv, action="store_true")
#     return parser
