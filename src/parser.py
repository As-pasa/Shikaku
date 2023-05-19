import argparse
from dataclasses import dataclass
from check_files import Checking


@dataclass
class ParserArguments:
    PARSER = argparse.ArgumentParser("Shikaku solver")
    PARSER.add_argument('file',
                        type=Checking.check_file_extension,
                        help='Puzzle file, which must have a txt '
                             'extension')
    ARGS = PARSER.parse_args()
