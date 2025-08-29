from argparse import ArgumentParser


def debug_argument() -> bool:
    parser = ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    return parser.parse_args().debug
