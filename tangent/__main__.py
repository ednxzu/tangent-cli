from . import utils
from .functions.create import create_tangent, connect_tangent
from .functions.list import list_tangent
from .functions.destroy import destroy_tangent
from .parser import create_parser
from tabulate import tabulate


def main(args):
    config = utils.load_config()
    tangent_id = config.get('tangent_id')
    if args.action == "create":
        print(args.connect)
        test_env_id = create_tangent(
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
    elif args.action == "list":
        list_tangent(
            tangent_id=tangent_id,
            running=args.running,
            stopped=args.stopped
        )
    elif args.action == "connect":
        connect_tangent(
            container_name=args.name,
            tangent_id=tangent_id
        )
    elif args.action == "destroy":
        destroy_tangent(
            name=args.name,
            keep_storage=args.keep_storage,
            config=config
        )

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    main(args)
