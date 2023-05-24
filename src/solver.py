import argparse
import logging
import os
import warnings

from check_files import Checking
from models import AnchorsFileReader
from solution import BoardSolution
from parser import ParserArguments
from RiddleGenerator import DivideRiddleGenerator


def solve_shikaku():
    args = ParserArguments().ARGS
    match args.command:
        case "online":
            board = DivideRiddleGenerator(args.size,
                                          DivideRiddleGenerator.ANCHOR_COUNT[args.size])
            board.compute()
            board = board.convert_to_string()
            print(board)
            anchors = BoardSolution(AnchorsFileReader(board))
            anchors.print_solution()
        case "offline":
            if not os.path.exists(args.file):
                raise argparse.ArgumentTypeError("Need to transfer an existing "
                                                 "file!"
                                                 )
            with open(args.file, 'r') as file:
                file_content = file.read()
                if not Checking.check_file_content(file_content):
                    raise argparse.ArgumentTypeError("The file should contain "
                                                     "only numbers!"
                                                     )

                if not Checking.check_max_element(file_content):
                    raise argparse.ArgumentTypeError("Each element must be "
                                                     "less than square of board"
                                                     )
                anchors = BoardSolution(AnchorsFileReader(file_content))
                anchors.print_solution()


if __name__ == '__main__':
    solve_shikaku()
