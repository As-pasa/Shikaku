import argparse


class Checking:
    @staticmethod
    def check_file_extension(file: str) -> str:
        """Проверка того, что файл передан с расширением txt"""
        if not file.endswith("txt"):
            raise argparse.ArgumentTypeError("File extension should be txt!")
        return file

    @staticmethod
    def check_file_content(file_content: str) -> bool:
        """Проверка содержимого файла"""
        lines = file_content.split('\n')
        matrix = [value for row in lines for value in row.split()]
        return all(value.isdigit() for value in matrix)

    @staticmethod
    def check_max_element(file_content: str) -> bool:
        """Проверка, что в файле нет элементов больших, чем площадь доски"""
        lines = file_content.split('\n')
        size = len(lines)
        square_size = size * size
        matrix = [value for row in lines for value in map(int, row.split())]
        return sum(matrix) <= square_size
