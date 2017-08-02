#!/usr/bin/python

import os


class InputParser(object):
    """docstring for InputParser"""
    def __init__(self, input_path):
        self.__input_path = input_path

    def parse_it(self):
        parsed_data = {}
        dir_files = os.listdir(self.__input_path)
        for selected_file in dir_files:
            selected_file_key = selected_file.replace('.txt', '')
            parsed_data[selected_file_key] = self.read_file(selected_file)
        return parsed_data

    def read_file(self, doc_name):
        file_name = self.__input_path + doc_name
        with open(file_name) as f:
            file_lines = f.read().splitlines()
            file_lines.pop(0)
            final_array = []
            for current_line in file_lines:
                final_array.append(eval(current_line))
            return final_array


def get_input(dirpath='../user_input/'):
    d = InputParser(dirpath).parse_it()
    return d['vertexes'], d['edges']

# if __name__ == '__main__':
#     parser = InputParser("../user_input/")

#     parser.parse_it()
