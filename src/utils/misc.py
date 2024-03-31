'''
Contains all the miscellaneous functions
'''
import os
import sys
import clang

def find_file_path(name, start_dir="."):
    """
    Find the file path of a given file name in a directory tree.

    Arguments:
        start_dir (str, optional): The directory to start searching in.
            Defaults to the current working directory.

    Returns:
        str: The absolute path of the first file with the given name found
            in the directory tree.
    """
    parent_dir = os.path.dirname(os.path.abspath(start_dir))
    for root, _, files in os.walk(parent_dir):
        if name in files:
            return os.path.join(root, name)
    error_message = f"\n\n***File '{name}' not found - Incorrect file path in compile_commands***"
    print(error_message)
    sys.exit(1)

def logs_to_str(build_logs: dict) -> str:
    """
    Parses building and running logs from the Docker API into strings.
    """
    ret_str = ''

    for entry in list(build_logs):
        if isinstance(entry, dict):
            for line in entry.values():
                if (line == '\n') | (not isinstance(line, str)):
                    continue
                if line.endswith('\n'):
                    ret_str += line
                else:
                    ret_str += line + '\n'
        else:
            ret_str += str(entry) + '\n'

    return ret_str

def comment_out(file_path, start_line, end_line):
    """
    Comments out the main method in the TUUT

    Parameters:
    file_path (str): The path to the input C++ file.
    start_line (int): The line where the main method starts
    end_line (int): The line where the main method ends

    Returns:
    None
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    lines[start_line - 1] = '/*' + lines[start_line - 1]
    lines[end_line - 1] = lines[end_line - 1].rstrip() + '*/ \n'

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def include_lib(file_path, output_file_path, library):
    """
    Includes the libraries needed for libFuzzer to work, in the specified C++ file.

    Parameters:
    file_path (str): The path to the input C++ file.
    output_file_path (str): The path to write the modified C++ file.
    library (str): The name of the library needed

    Returns:
    None
    """
    include_pos = None

    # Open initial cpp file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    if library not in content:
        # Find the position to insert the include line
        include_pos = content.find("#include")
        if include_pos != -1:
            # Find the end of the line after the last include
            include_end_pos = content.find('\n', include_pos)
            if include_end_pos == -1:
                include_end_pos = len(content)
            # Insert the include line
            content = (
                content[:include_end_pos] + '\n' +
                library + '\n' +
                content[include_end_pos:]
            )

        else:
            # If no existing includes are found, add the include line at the top of the file
            content = library + '\n' + content

    # Write the modified content back to the file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def find_main_function_range(file_path):
    """
    Finds the main method in the TUUT

    Parameters:
    file_path (str): The path to the input C++ file.

    Returns:
    True, main start line, main end line - if the main method exists in the TUUT
    or
    False, 0, 0 - if the main function does not exists in the TUUT
    """
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)

    for node in translation_unit.cursor.walk_preorder():
        # chech to see if the method found is "main"
        if node.kind == clang.cindex.CursorKind.FUNCTION_DECL and node.spelling == 'main':
            return True, node.extent.start.line, node.extent.end.line
    return False, 0, 0
