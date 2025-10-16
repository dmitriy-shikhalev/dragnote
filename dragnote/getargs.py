import argparse

from dragnote.enums import Choice


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        choices=[value.value for value in Choice._member_map_.values()],
        dest="command",
    )
    parser.add_argument(
        "--synth-num",
        dest="synth_num",
        type=int,
        required=False,
    )
    return parser.parse_args()
