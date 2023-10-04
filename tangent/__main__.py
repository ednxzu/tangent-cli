from . import utils
from .functions.create import create_tangent, start_tangent, connect_tangent
from .functions.list import list_tangent
from .functions.destroy import destroy_tangent, stop_tangent
from .parser import create_parser
import docker


def main(args):
    config = utils.load_config()
    client = docker.from_env()

    if args.action == "create":
        create_tangent(
            distribution=args.distribution,
            client=client,
            connect=args.connect,
            name=args.name,
            shell=args.shell,
            config=config,
            create_volume=args.volume
        )
    elif args.action == "list":
        list_tangent(
            client=client,
            config=config,
            name=args.name,
            running=args.running,
            stopped=args.stopped
        )
    elif args.action == "connect":
        connect_tangent(
            name=args.name,
            config=config,
            client=client,
            shell=args.shell
        )
    elif args.action == "destroy":
        destroy_tangent(
            name=args.name,
            client=client,
            keep_storage=args.keep_storage,
            config=config
        )
    elif args.action == "stop":
        stop_tangent(
            name=args.name,
            client=client,
            config=config
        )
    elif args.action == "start":
        start_tangent(
            name=args.name,
            config=config,
            client=client,
            connect=args.connect,
            shell=args.shell
        )


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    main(args)
