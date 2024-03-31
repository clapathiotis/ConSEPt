"""
Creates test cases for the libfuzzer module
"""
import os
import sys
import string
from pathlib import Path
from src.utils.misc import find_file_path
from src.fuzz_handler import FuzzHandler, ask_for_annotation_choice_fuzz
from src.tuut_file import TuutFile

PATH_ABSOLUTE = str(Path(os.path.realpath(__file__)).parent)
PATH_CONSEPT = str(Path(PATH_ABSOLUTE).parents[0])
sys.path.append(PATH_CONSEPT)

FILEFOLDER = "sample_inputs"


def test_annotate_parameters_address_memory_line_7():
    """
    Tests the `annotate_fuzz()` function through checking if
    the address_memory.cpp file contains the correct annotation
    for the method on line 7
    """
    fuzz_handler = FuzzHandler(test=True)
    tuut = TuutFile(find_file_path("address_memory.cpp"))
    tuut.gen_func_info()

    fuzz_handler.annotate_fuzz(tuut, 7)

    with open(tuut.path_fuzz_annotated, 'r', encoding='utf-8') as file:
        file_contents = file.read()
        assert 'extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size)' in file_contents
        assert 'char a[6];' in file_contents
        assert 'if(Size == 6)' in file_contents
        assert 'memcpy(a, Data + 0, 6);' in file_contents
        assert 'print_elements(a)' in file_contents


def test_annotate_parameters_address_memory_line_14():
    """
    Tests the `annotate_fuzz()` function through checking if
    the address_memory.cpp file contains the correct annotation
    for the method on line 14
    """
    fuzz_handler = FuzzHandler(test=True)
    tuut = TuutFile(find_file_path("address_memory.cpp"))
    tuut.gen_func_info()

    fuzz_handler.annotate_fuzz(tuut, 14)

    with open(tuut.path_fuzz_annotated, 'r', encoding='utf-8') as file:
        file_contents = file.read()
        assert 'extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size)' in file_contents
        assert 'int a[1];' in file_contents
        assert 'if(Size == 1)' in file_contents
        assert 'memcpy(a, Data + 0, 1);' in file_contents
        assert 'uninit_value(a[0])' in file_contents


def test_annotate_parameters_address_memory_line_25():
    """
    Tests the `annotate_fuzz()` function through checking if
    the address_memory.cpp file contains the correct annotation
    for the method on line 25
    """
    fuzz_handler = FuzzHandler(test=True)
    tuut = TuutFile(find_file_path("address_memory.cpp"))
    tuut.gen_func_info()

    fuzz_handler.annotate_fuzz(tuut, 25)

    with open(tuut.path_fuzz_annotated, 'r', encoding='utf-8') as file:
        file_contents = file.read()
        assert 'extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size)' in file_contents
        assert 'int a[1];' in file_contents
        assert 'if(Size == 1)' in file_contents
        assert 'memcpy(a, Data + 0, 1);' in file_contents
        assert 'createAndFreeMemory(a[0])' in file_contents


def test_ask_for_annotation_choice_fuzz_one_input(monkeypatch):
    """
    Tests the `ask_for_annotation_choice_fuzz()` function through
    checking if the method returns the correct choice of the user
    given a predefined input value
    """

    test_func_dict = {6: 'test_method_1 bool (char *)', 14: 'test_method_2 int (int)',
                      22: 'test_method_3 void (short, long, float, char *, int *, double *)',
                      26: 'test_method_4 void ()'}

    test_func_details = {6: ['test_method_1', 1, [['constantarray', 'char', 3]]],
                         14: ['test_method_2', 1, [['int', '', -1]]],
                         22: ['test_method_3', 6, [['short', '', -1], ['long', '', -1],
                                                   ['float', '', -1], ['constantarray',
                                                                       'char', 1000],
                                                   ['constantarray', 'int', 10],
                                                   ['constantarray', 'double', 20]]],
                         26: ['test_method_4', 0, []]}

    monkeypatch.setattr('builtins.input', lambda _: "6")
    result = ask_for_annotation_choice_fuzz(test_func_dict, test_func_details)
    assert result == '6'


def test_ask_for_annotation_choice_fuzz_invalid_input_1(monkeypatch):
    """
    Tests the `ask_for_annotation_choice_fuzz()` function through
    checking if the method returns the correct (second) choice of the user
    given that the first chosen function does not have any parameters
    """

    test_func_dict = {6: 'test_method_1 bool (char *)', 14: 'test_method_2 int (int)',
                      22: 'test_method_3 void (short, long, float, char *, int *, double *)',
                      26: 'test_method_4 void ()'}

    test_func_details = {6: ['test_method_1', 1, [['constantarray', 'char', 3]]],
                         14: ['test_method_2', 1, [['int', '', -1]]],
                         22: ['test_method_3', 6, [['short', '', -1], ['long', '', -1],
                                                   ['float', '', -1], ['constantarray',
                                                                       'char', 1000],
                                                   ['constantarray', 'int', 10],
                                                   ['constantarray', 'double', 20]]],
                         26: ['test_method_4', 0, []]}

    inputs = iter(['26', '14'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = ask_for_annotation_choice_fuzz(test_func_dict, test_func_details)
    assert result == '14'


def test_ask_for_annotation_choice_fuzz_invalid_input_2(monkeypatch):
    """
    Tests the `ask_for_annotation_choice_fuzz()` function through
    checking if the method returns the correct (second) choice of the user
    given that the first provided input is some random line number
    that is not present in the function dictionary
    """

    test_func_dict = {6: 'test_method_1 bool (char *)', 14: 'test_method_2 int (int)',
                      22: 'test_method_3 void (short, long, float, char *, int *, double *)',
                      26: 'test_method_4 void ()'}

    test_func_details = {6: ['test_method_1', 1, [['constantarray', 'char', 3]]],
                         14: ['test_method_2', 1, [['int', '', -1]]],
                         22: ['test_method_3', 6, [['short', '', -1], ['long', '', -1],
                                                   ['float', '', -1], ['constantarray',
                                                                       'char', 1000],
                                                   ['constantarray', 'int', 10],
                                                   ['constantarray', 'double', 20]]],
                         26: ['test_method_4', 0, []]}

    inputs = iter(['13', '22'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = ask_for_annotation_choice_fuzz(test_func_dict, test_func_details)
    assert result == '22'


def test_increase_counter():
    """
    Tests the `increase_counter()` function through checking if
    the counter of the FuzzHandler object is updated correctly
    """
    fuzz_handler = FuzzHandler(test=True)
    for i in range(1, 27):
        fuzz_handler.increase_counter()
        assert fuzz_handler.counter == i


def test_next_letter_all_letters():
    """
    Tests the `next_letter()` function through checking if
    all the 26 lowercase letters of the alphabet are generated
    """
    fuzz_handler = FuzzHandler(test=True)

    for i in range(26):
        assert fuzz_handler.next_letter() == string.ascii_lowercase[i]


def test_next_letter_all_letters_larger_counter():
    """
    Tests the `next_letter()` function through checking if
    all the 26 lowercase letters of the alphabet are generated twice
    by increasing the counter such that it has a larger value than
    the total number of lowercase ASCII characters
    """
    fuzz_handler = FuzzHandler(test=True)

    for i in range(52):
        assert fuzz_handler.next_letter() == string.ascii_lowercase[i % 26]
