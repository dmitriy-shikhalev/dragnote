import argparse

from dragnote.enums import Choice


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        choices=[value.value for value in Choice._member_map_.values()],
        dest="command",
    )
    parser.add_argument(
        "--composition-name",
        dest="composition_name",
        type=str,
        required=False,
    )
    parser.add_argument(
        "--lesson-num",
        dest="lesson_num",
        type=int,
        required=False,
    )
    parser.add_argument(
        "--synth-num",
        dest="synth_num",
        type=int,
        required=False,
    )
    return parser.parse_args()
