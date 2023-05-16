from check_files import check_file_extension


def preparation_for_offline_solution(subparser):
    """Парсер аргументов для команды offline"""
    arg_subparser = subparser.add_parser("offline")
    arg_subparser.add_argument('file',
                               type=check_file_extension,
                               help='Puzzle file, which must have a txt '
                                    'extension')
