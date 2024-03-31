import os
import tempfile
import pytest

from src.utils.misc import find_file_path
from src.fuzz_handler import FuzzHandler
from src.tuut_file import TuutFile


def helper_generate_file(extension, new_dir):
    """
    Generates file at 'new_dir' with the according extension. and returns the TuutFile.
    """
    file_name = "file." + extension
    file_path = os.path.join(new_dir, file_name)
    with open(file_path, 'a', encoding='utf-8'):
        pass
    test_file = TuutFile(file_path)
    return test_file


def test_valid_file_extension_1():
    """
    Tests the functions get_file_extension() and is_valid_file().
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file_1 = helper_generate_file("txt", temp_dir)
        assert test_file_1.file_extension == ".txt"
        assert not test_file_1.is_valid_file()

        test_file_2 = helper_generate_file("cpp", temp_dir)
        assert test_file_2.file_extension == ".cpp"
        assert test_file_2.is_valid_file()

        test_file_3 = helper_generate_file("c", temp_dir)
        assert test_file_3.file_extension == ".c"
        assert not test_file_3.is_valid_file()

        test_file_4 = helper_generate_file("cc", temp_dir)
        assert test_file_4.file_extension == ".cc"
        assert test_file_4.is_valid_file()


def test_valid_file_extension_2():
    """
    Tests the is_valid_file() with a real file.
    """
    file_path = "if-statement-1.cpp"
    test_file = TuutFile(file_path)

    assert test_file.is_valid_file()


def test_valid_file_extension_3():
    """
    Tests if the exception arises when a file with no extension is given.
    """
    file_name = "h"
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, file_name)
        with open(file_path, 'a', encoding='utf-8'):
            pass
        with pytest.raises(Exception):
            TuutFile(file_path)


def test_get_file_extension_cpp():
    """
    Tests the `get_file_extension()` function through checking if
    the extension of the if-statement-1.cpp file is '.cpp'
    """
    tuut = TuutFile(find_file_path("if-statement-1.cpp"))
    assert tuut.get_file_extension() == '.cpp'


def test_get_file_extension_json():
    """
    Tests the `get_file_extension()` function through checking if
    the extension of the loops_compile_commands.json file is '.json'
    """
    tuut = TuutFile(find_file_path("loops_compile_commands.json"))
    assert tuut.get_file_extension() == '.json'


def test_get_file_extension_h():
    """
    Tests the `get_file_extension()` function through checking if
    the extension of the calculator.h file is '.h'
    """
    tuut = TuutFile(find_file_path("calculator.h"))
    assert tuut.get_file_extension() == '.h'


def test_get_file_extension_txt():
    """
    Tests the `get_file_extension()` function through checking if
    the extension of the CMakeLists.txt file is '.txt'
    """
    tuut = TuutFile(find_file_path("CMakeLists.txt"))
    assert tuut.get_file_extension() == '.txt'


def test_include_fuzz():
    """
    Tests the `include_fuzz()` function through checking if
    the if-statement-1.cpp file contains the correct library imports
    """
    fuzz_handler = FuzzHandler(test=True)
    tuut = TuutFile(find_file_path("if-statement-1.cpp"))
    tuut.gen_func_info()
    fuzz_handler.annotate_fuzz(tuut, 3)
    tuut.include_fuzz()
    with open(tuut.path_fuzz_annotated, 'r', encoding='utf-8') as file:
        file_contents = file.read()
        assert '#include <stddef.h>' in file_contents
        assert '#include <stdint.h>' in file_contents
        assert '#include <string.h>' in file_contents


def test_get_func_info():
    """
    Tests the `get_func_info()` function through checking if
    the address_memory.cpp method details are stored accordingly
    """
    test_func_dict = {7: 'print_elements void (char *)',
                      14: 'uninit_value int (int)',
                      25: 'createAndFreeMemory int (int)'}

    test_func_details = {7: ['print_elements', 1, [['constantarray', 'char', 6]]],
                         14: ['uninit_value', 1, [['int', '', -1]]],
                         25: ['createAndFreeMemory', 1, [['int', '', -1]]]}

    tuut = TuutFile(find_file_path("address_memory.cpp"))
    tuut.gen_func_info()
    assert tuut.func_dict == test_func_dict
    assert tuut.func_details == test_func_details


def test_comment_out_main():
    """
    Tests the `comment_out_main()` function through checking if
    the 'main()' method inside if-statement-1.cpp is commented out
    """
    fuzz_handler = FuzzHandler(test=True)
    tuut = TuutFile(find_file_path("if-statement-1.cpp"))
    tuut.gen_func_info()
    fuzz_handler.annotate_fuzz(tuut, 3)
    tuut.comment_out_main()
    with open(tuut.path_fuzz_annotated, 'r', encoding='utf-8') as file:
        file_contents = file.readlines()
        assert '/*int main()' in file_contents[11]
        assert '}*/' in file_contents[16]


def test_path_container_fuzz():
    """
    Tests the `path_container_fuzz()` function through checking if
    the path_container_fuzz is updated accordingly
    """
    tuut = TuutFile(find_file_path("address_memory.cpp"))
    assert tuut.path_container_fuzz == '/home/consept/tmp/fuzz/address_memory.cpp'
