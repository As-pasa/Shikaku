import os
import sys

from parse_argument import *
from check_files import *
from models import AnchorsFileReader
from solution import BoardSolution
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class ParserArguments:
    PARSER: ClassVar = argparse.ArgumentParser("Shikaku solver")
    SUBPARSER: ClassVar = \
        PARSER.add_subparsers(title="Variants",
                              dest="command",
                              description="Solution offline Shikaku")
    SUBPARSER.required = True
    preparation_for_offline_solution(SUBPARSER)
    ARGS = PARSER.parse_args()


class Solver:
    @staticmethod
    def solving_shikaku():
        args = ParserArguments.ARGS
        match args.command:
            case "offline":
                if not os.path.exists(args.file):
                    print("Need to transfer an existing file!")
                    sys.exit(1)

                with open(args.file, 'r') as file:
                    file_content = file.read()
                    if not check_file_content(file_content):
                        print("The file should contain only numbers!")
                        sys.exit(1)

                    if not check_size_board(file_content):
                        print("The matrix in the file must be square!")
                        sys.exit(1)
                    anchors = BoardSolution(AnchorsFileReader(file_content))
                    anchors.print_solution()


if __name__ == '__main__':
    Solver.solving_shikaku()
