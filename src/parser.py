import argparse
from dataclasses import dataclass

import check_files
from check_files import Checking


@dataclass
class ParserArguments:
    def __init__(self):
        self.PARSER = argparse.ArgumentParser("Shikaku solver")
        self.SUBPARSER = \
            self.PARSER.add_subparsers(title="Variants",
                                       dest="command",
                                       description="Solution online or "
                                                   "offline Shikaku"
                                       )
        self.SUBPARSER.required = True
        self.random_board()
        self.file_board()
        self.ARGS = self.PARSER.parse_args()

    def random_board(self):
        arg_subparser = self.SUBPARSER.add_parser("online")
        arg_subparser.add_argument('size',
                                   type=int,
                                   choices=[5, 10, 15],
                                   help="The size of the shikaku board you "
                                        "want to solve"
                                   )

    def file_board(self):
        arg_subparser = self.SUBPARSER.add_parser("offline")
        arg_subparser.add_argument('file',
                                   type=Checking.check_file_extension,
                                   help='Puzzle file, which must have a txt '
                                        'extension')


