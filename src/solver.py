import argparse
import logging
import os
import warnings

from check_files import Checking
from models import AnchorsFileReader
from solution import BoardSolution
from parser import ParserArguments


def solve_shikaku():
    args = ParserArguments.ARGS
    if not os.path.exists(args.file):
        logging.critical("Need to transfer an existing file!")

    with open(args.file, 'r') as file:
        file_content = file.read()
        if not Checking.check_file_content(file_content):
            raise argparse.ArgumentTypeError("The file should contain "
                                             "only numbers!")

        if not Checking.check_max_element(file_content):
            raise argparse.ArgumentTypeError("Each element must be less than "
                                             "square of board")
        anchors = BoardSolution(AnchorsFileReader(file_content))
        anchors.print_solution()


if __name__ == '__main__':
    solve_shikaku()
