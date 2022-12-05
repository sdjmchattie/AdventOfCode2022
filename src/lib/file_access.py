from os import path


def default_input_file(script_file_path):
    script_root = path.splitext(script_file_path)
    file_root = path.basename(script_root[0])

    return f"../input/{file_root}.txt"


def read_input_lines(script_file_path):
    with open(default_input_file(script_file_path), "r") as file:
        return [line.strip("\n") for line in file.readlines()]
