import os
import sys

from check_files import *
from models import AnchorsFileReader
from solution import BoardSolution
from dataclasses import dataclass


@dataclass
class ParserArguments:
    PARSER = argparse.ArgumentParser("Shikaku solver")
    PARSER.add_argument('file',
                        type=check_file_extension,
                        help='Puzzle file, which must have a txt '
                             'extension')
    ARGS = PARSER.parse_args()


class Solver:
    @staticmethod
    def solving_shikaku():
        args = ParserArguments.ARGS
        if not os.path.exists(args.file):
            print("Need to transfer an existing file!")
            sys.exit(1)

        with open(args.file, 'r') as file:
            file_content = file.read()
            if not check_file_content(file_content):
                print("The file should contain only numbers!")
                sys.exit(1)

            if not check_max_element(file_content):
                print("Each element must be less than square of board")
                sys.exit(1)
            anchors = BoardSolution(AnchorsFileReader(file_content))
            anchors.print_solution()


if __name__ == '__main__':
    Solver.solving_shikaku()
