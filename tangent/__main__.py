from . import utils
from .functions.create import create_container, connect_container
from .functions.list import list_containers_by_uuid
from .functions.destroy import destroy_environment
from .parser import create_parser
from tabulate import tabulate


def main(args):
    config = utils.load_config()
    tangent_id = config.get('tangent_id')
    if args.action == "create":
        if args.distribution:
            print(args.connect)
            test_env_id = create_container(
                distribution=args.distribution,
                tangent_id=tangent_id,
                connect=args.connect,
                name=args.name,
                shell=args.shell,
                config=config,
                create_volume=args.volume
            )
            if test_env_id:
                print(f"Test environment created with ID: {test_env_id}")
            else:
                return 1
        else:
            print(
                "Error: Distribution name is required when creating a test environment."
            )
            return 1
    elif args.action == "list":
        list_containers_by_uuid(tangent_id=tangent_id, running=args.running, stopped=args.stopped)
    elif args.action == "connect":
        if args.name:
            connect_container(container_name=args.name, tangent_id=tangent_id)
        else:
            print("Error: Specify the name of the environment to connect to using the '--name' flag.")
    elif args.action == "destroy":
        if args.name:
            destroy_environment(name=args.name, keep_storage=args.keep_storage, config=config)
        else:
            print("Error: Specify the name of the environment to connect to using the '--name' flag.")


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    main(args)
