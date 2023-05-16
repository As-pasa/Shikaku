import argparse


def check_file_extension(file: str) -> str:
    """Проверка того, что файл передан с расширением txt"""
    if not file.endswith("txt"):
        raise argparse.ArgumentTypeError("File extension should be txt!")
    return file


def check_file_content(file_content: str) -> bool:
    """Проверка содержимого файла"""
    line_content = filter(lambda x: x, map(str.strip, file_content))
    return all(value.isdigit() for value in line_content)


def check_size_board(file_content: str) -> bool:
    """Проверка, что в файле нахидится квадратная матрица"""
    lines = file_content.split('\n')
    matrix = [[value for value in row.split()] for row in lines]
    return all(len(row) == len(matrix) for row in matrix)
