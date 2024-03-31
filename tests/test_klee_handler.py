"""
Creates test cases for the klee module
"""
import tempfile
import os
import io
import sys
import pprint
import re

from io import StringIO
from unittest.mock import MagicMock, patch
from pathlib import Path
from unittest.mock import patch
from application_manager import ApplicationManager

from src.klee_handler import KLEEHandler
PATH_ABSOLUTE   = str(Path(os.path.realpath(__file__)).parent)
PATH_CONSEPT    = str(Path(PATH_ABSOLUTE).parents[0])
sys.path.append(PATH_CONSEPT)

klee_handler = KLEEHandler(test=True)

FILEFOLDER = "sample_inputs"

def test_annotate_variables_if_statement_1(monkeypatch):
    """
    Tests the `annotate_variables()` function through checking if
    the if_statement_1.cpp file contains the correct annotation
    """
    file_path = os.path.join(FILEFOLDER,"if-statement-1.cpp")
    # "sample_inputs/if-statement-1.cpp"

    # create a temporary output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', encoding='utf-8') as output_file:
        output_file_path = output_file.name

    # call the annotate_variables function on the input file
    monkeypatch.setattr('builtins.input', lambda _: "1")
    klee_handler.annotate_variables(file_path, output_file_path)

    # check that the output file contains the annotated variables
    with open(output_file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()
        assert 'klee_make_symbolic(&x, sizeof(x), "x");' in file_contents
        assert 'klee_make_symbolic(&result, sizeof(result), "result");' in file_contents

    os.remove(output_file_path)


def test_annotate_variables_if_statement_1_2(monkeypatch):
    """
    Tests the `annotate_variables()` function through checking if
    the if_statement_1.cpp file contains the correct annotation
    """
    file_path = os.path.join(FILEFOLDER,"if-statement-1.cpp")
    # tests/test_files/if-statement-1.cpp

    # create a temporary output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', encoding='utf-8', delete=False
                                     ) as output_file:

        output_file_path = output_file.name

        # Test input 2 and line number 15
        inputs = ["2", "13"]
        monkeypatch.setattr(
            'builtins.input', lambda _: inputs.pop(0) if inputs else "")
        klee_handler.annotate_variables(file_path, output_file_path)

        # check that the output file contains the annotated variables
        with open(output_file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()
            assert 'klee_make_symbolic(&x, sizeof(x), "x");' in file_contents

    # remove the temporary file
    os.remove(output_file_path)


def test_annotate_variables_boolean_file(monkeypatch):
    """
    Tests the `annotate_variables()` function by checking if
    the boolean_file.cpp file contains the correct annotation.
    """
    file_path = os.path.join(FILEFOLDER,"boolean_file.cpp")
    # "tests/test_files/boolean_file.cpp"

    # Create a temporary output file
    with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.cpp',
            encoding='utf-8',
            delete=False
    ) as output_file:

        output_file_path = output_file.name

        # Call the annotate_variables function on the input file
        monkeypatch.setattr('builtins.input', lambda _: "1")
        klee_handler.annotate_variables(file_path, output_file_path)

        # Check that the output file contains the annotated variables
        with open(output_file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()
            assert 'klee_make_symbolic(&condition, sizeof(condition), "condition");'\
                in file_contents

    # Remove the temporary output file
    if os.path.exists(output_file_path):
        os.remove(output_file_path)


def test_annotate_variables_array_chars(monkeypatch):
    """
    Tests the `annotate_variables()` function by checking if
    the array_chars.cpp file contains the correct annotation.
    """
    file_path = os.path.join(FILEFOLDER,"array_chars.cpp")
    # "tests/test_files/array_chars.cpp"

    # Create a temporary output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', encoding='utf-8', delete=False
                                     ) as output_file:

        output_file_path = output_file.name

        # Call the annotate_variables function on the input file
        monkeypatch.setattr('builtins.input', lambda _: "1")
        klee_handler.annotate_variables(file_path, output_file_path)

        # Check that the output file contains the annotated variables
        with open(output_file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()
            assert 'klee_make_symbolic(&arr, sizeof(arr), "arr");' in file_contents

    # Remove the temporary output file
    if os.path.exists(output_file_path):
        os.remove(output_file_path)


def test_annotate_variables_long_integer(monkeypatch):
    """
    Tests the `annotate_variables()` function by checking if
    the long_integer.cpp file contains the correct annotation.
    """
    file_path = os.path.join(FILEFOLDER,"long_integer.cpp")
    # "tests/test_files/long_integer.cpp"

    # Create a temporary output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', encoding='utf-8', delete=False
                                     ) as output_file:

        output_file_path = output_file.name

        # Call the annotate_variables function on the input file
        monkeypatch.setattr('builtins.input', lambda _: "1")
        klee_handler.annotate_variables(file_path, output_file_path)

        # Check that the output file contains the annotated variable
        with open(output_file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()
            assert 'klee_make_symbolic(&number, sizeof(number), "number");' in file_contents

    # Remove the temporary output file
    if os.path.exists(output_file_path):
        os.remove(output_file_path)


def test_annotate_variables_string(monkeypatch):
    """
    Tests the `annotate_variables()` function by checking if
    the string_file.cpp file contains the correct annotation.
    """
    file_path = os.path.join(FILEFOLDER,"string_file.cpp")
    # "tests/test_files/string_file.cpp"

    # Create a temporary output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', encoding='utf-8', delete=False
                                     ) as output_file:
        output_file_path = output_file.name

        # Call the annotate_variables function on the input file
        monkeypatch.setattr('builtins.input', lambda _: "1")
        klee_handler.annotate_variables(file_path, output_file_path)

        # Check that the output file contains the annotated variable
        with open(output_file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()
            assert 'klee_make_symbolic(&text, sizeof(text), "text");' in file_contents

    # Remove the temporary output file
    if os.path.exists(output_file_path):
        os.remove(output_file_path)


def test_annotate_variables_user_defined(monkeypatch):
    """
    Tests the `annotate_variables()` function by checking if
    the user_defined.cpp file contains the correct annotation.
    """
    file_path = os.path.join(FILEFOLDER,"user_defined.cpp")
    # "tests/test_files/user_defined.cpp"

    # Create a temporary output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', encoding='utf-8', delete=False
                                     ) as output_file:
        output_file_path = output_file.name

        # Call the annotate_variables function on the input file
        monkeypatch.setattr('builtins.input', lambda _: "1")
        klee_handler.annotate_variables(file_path, output_file_path)
        # Check that the output file contains the annotated variable
        with open(output_file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()
            assert 'klee_make_symbolic(&person, sizeof(person), "person");' in file_contents
    # Remove the temporary output file
    if os.path.exists(output_file_path):
        os.remove(output_file_path)

def test_include_library():
    """
    Tests the `include_library()` function by checking that "#include <klee/klee.h>"
    is in the output file after running include_library method.
    """
    file_path = os.path.join(FILEFOLDER, "if-statement-1.cpp")
    # "tests/test_files/if-statement-1.cpp"
    # create a temporary directory with output file
    temp_file_path = file_path

    # call the include_klee function on the input file
    path_annotated_file = klee_handler.include_library(temp_file_path)

    # check that the output file contains include klee
    with open(path_annotated_file, 'r', encoding='utf-8') as file:
        file_contents = file.read()
        assert '#include <klee/klee.h>' in file_contents

def test_include_library_duplicate():
    """
    Tests the `include_klee()` function by checking that "#include <klee/klee.h>"
    is not duplicated if it is already in the test class.
    """
    file_path = os.path.join(FILEFOLDER,"if-statement-klee-included.cpp")
    # "tests/test_files/if-statement-klee-included.cpp"
    # create a temporary directory with output file

    # call the include_klee function on the input file
    path_annotated_file = klee_handler.include_library(file_path)

    with open(path_annotated_file, 'r', encoding='utf-8') as file:
        file_contents = file.read()
        # check if the include klee line is duplicated
        assert file_contents.count('#include <klee/klee.h>') == 1

def test_get_error_inputs_single_error():
    """
    Tests the `get_error_inputs()` function through checking if
    given outputs from the generated tests match expected values.
    """
    tests = """ktest file 1:\nnum objects: 1\nobject 0: name: 'x'\nobject 0: int : 42
        """
    num_of_errors = 1
    inputs, names, num_of_objects = klee_handler.get_error_inputs(
        tests, num_of_errors)
    expected_inputs = [42]
    expected_names = ['x']
    expected_nr_of_obj = 1

    assert inputs == expected_inputs, "Error in single error with inputs"
    assert names == expected_names, "Error in single error with names"
    assert num_of_objects == expected_nr_of_obj, "Error in single error with nr of Objects"


def test_get_error_inputs_no_errors():
    """
    Tests the `get_error_inputs()` function through checking if
    given outputs from the generated tests match expected values.
    """
    tests = """ktest file 1:\nnum objects: 1\nobject 0: name: 'x'\nobject 0: int : 42
    """
    num_of_errors = 0
    inputs, names, num_of_objects = klee_handler.get_error_inputs(
        tests, num_of_errors)
    expected_inputs = []
    expected_names = []
    expected_nr_of_obj = 0

    assert inputs == expected_inputs, "Error in single error with inputs"
    assert names == expected_names, "Error in single error with names"
    assert num_of_objects == expected_nr_of_obj, "Error in single error with nr of Objects"


def test_get_error_inputs_more_test_than_errors():
    """
    Tests the `get_error_inputs()` function through checking if
    given outputs from the generated tests match expected values.
    """
    tests = """ktest file 1:\nnum objects: 1\nobject 0: name: 'x'\nobject 0: int : 42
    \nktest file 2:\nnum objects: 1\nobject 0: name: 'x'\nobject 0: int : 55
    """
    num_of_errors = 1
    inputs, names, num_of_objects = klee_handler.get_error_inputs(
        tests, num_of_errors)
    expected_inputs = [42]
    expected_names = ['x']
    expected_nr_of_obj = 1

    assert inputs == expected_inputs, "Error in single error with inputs"
    assert names == expected_names, "Error in single error with names"
    assert num_of_objects == expected_nr_of_obj, "Error in single error with nr of Objects"


def test_get_error_inputs_two_objects_two_error():
    """
    Tests the `get_error_inputs()` function through checking if
    given outputs from the generated tests match expected values.
    """
    tests = """ktest file 1:\nnum objects: 2\nobject 0: name: 'x'\nobject 0: int : 42
    \nobject 0: name: 'y'\nobject 0: int : 4\nktest file 2:\nnum objects: 1
    \nobject 0: name: 'x'\nobject 0: int : 55\nobject 0: name: 'y'\nobject 0: int : 2
    """
    num_of_errors = 2
    inputs, names, num_of_objects = klee_handler.get_error_inputs(
        tests, num_of_errors)
    expected_inputs = [42, 4, 55, 2]
    expected_names = ['x', 'y', 'x', 'y']
    expected_nr_of_obj = 2

    assert inputs == expected_inputs, "Error in single error with inputs"
    assert names == expected_names, "Error in single error with names"
    assert num_of_objects == expected_nr_of_obj, "Error in single error with nr of Objects"


def test_ask_for_annotation_choice_klee(monkeypatch):
    """
    Tests the `ask_for_annotation_choice()` function by mocking user input.
    """
    # Mock user input for choice 2 and line numbers 13, 14
    inputs = ["2", "13, 14"]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))
    unique_dict = {13: 'x', 14: 'result'}

    # Capture the printed output
    captured_output = io.StringIO()
    sys.stdout = captured_output

    # Call the function
    klee_handler.ask_for_annotation_choice_klee(unique_dict)

    # Reset the standard output
    sys.stdout = sys.__stdout__

    # Get the printed output as a string
    printed_output = captured_output.getvalue()

    # Check the printed output
    expected_output = (
        "\nChoose what to annotate:\n"
        "1. All variables\n"
        "2. Select specific variables\n"
        "Choose what to annotate:  " + pprint.pformat(unique_dict)
    )
    assert printed_output.strip() == expected_output.strip()


def test_insert_annotations():
    """
    Tests the `insert_annotations()` method.
    """
    # Mocked input
    content = [
        "int main() {",
        "\tint x = 5;",
        "\tint y = 10;",
        "\tint z = x + y;",
        "\treturn z;",
        "}"
    ]
    rows = [2, 3]
    unique_dict = {2: 'x', 3: 'y'}

    # Expected output
    expected_output = [
        "int main() {",
        "\tint x = 5;",
        "\tklee_make_symbolic(&x, sizeof(x), \"x\");\n",
        "\tint y = 10;",
        "\tklee_make_symbolic(&y, sizeof(y), \"y\");\n",
        "\tint z = x + y;",
        "\treturn z;",
        "}"
    ]

    # Call the method
    result = klee_handler.insert_annotations(content, rows, unique_dict)

    # Convert the lists to strings
    result_str = "\n".join(result)
    expected_output_str = "\n".join(expected_output)

    # Compare the strings
    if result_str != expected_output_str:
        print("Actual Output:")
        print(result_str)
        print("Expected Output:")
        print(expected_output_str)

    assert result_str == expected_output_str

def test_extract_errors():
    """
    Tests the `extract_errors` method of a class.
    """
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set the path to the errors directory
        errors_path = os.path.join(temp_dir, 'errors')

        # Create the errors directory
        os.makedirs(errors_path, exist_ok=True)

        # Create a temporary 'messages.txt' file with errors
        messages_file_path = os.path.join(errors_path, 'messages.txt')
        with open(messages_file_path, 'w') as messages_file:
            messages_file.write('KLEE: ERROR: Error 1\n')
            messages_file.write('KLEE: ERROR: Error 2\n')
            messages_file.write('KLEE: WARNING: Warning 1\n')

        # Test the extract_errors method
        errors = klee_handler.extract_errors(errors_path)

        # Verify the extracted errors
        expected_errors = ['KLEE: ERROR: Error 1', 'KLEE: ERROR: Error 2']
        assert errors == expected_errors

def test_print_error_inputs(capsys):
    """
    Tests the `print_error_inputs()` function by capturing the printed output
    and comparing it with the expected output.
    """
    # Mock the data for tests and errors
    tests = "\n".join([
        "args       : ['/home/consept/tmp/concolic/test.bc']",
        "num objects: 1",
        "object 0: name: 'x'",
        "object 0: size: 4",
        "object 0: data: b'\\xff\\xff\\xff\\xff'",
        "object 0: hex : 0xffffffff",
        "object 0: int : -1",
        "object 0: uint: 4294967295",
        "object 0: text: ....",
        "ktest file : 'tmp/concolic/klee-out-0/test000002.ktest'",
        "args       : ['/home/consept/tmp/concolic/test.bc']",
        "num objects: 2",
        "object 0: name: 'x'",
        "object 0: size: 4",
        "object 0: data: b'\\x00\\x00\\x00\\x00'",
        "object 0: hex : 0x00000000",
        "object 0: int : 0",
        "object 0: uint: 0",
        "object 0: text: ....",
        "object 1: name: 'result'",
        "object 1: size: 4",
        "object 1: data: b'\\x00\\x00\\x00\\x00'",
        "object 1: hex : 0x00000000",
        "object 1: int : 0",
        "object 1: uint: 0",
        "object 1: text: ....",
        "ktest file : 'tmp/concolic/klee-out-0/test000003.ktest'",
        "args       : ['/home/consept/tmp/concolic/test.bc']",
        "num objects: 2",
        "object 0: name: 'x'",
        "object 0: size: 4",
        "object 0: data: b'\\xff\\xff\\xff\\x7f'",
        "object 0: hex : 0xffffff7f",
        "object 0: int : 2147483647",
        "object 0: uint: 2147483647",
        "object 0: text: ....",
        "object 1: name: 'result'",
        "object 1: size: 4",
        "object 1: data: b'\\x00\\x00\\x00\\x00'",
        "object 1: hex : 0x00000000",
        "object 1: int : 0",
        "object 1: uint: 0",
        "object 1: text: ....",
    ])

    errors = ["KLEE: ERROR: tmp/concolic/annotated_if-statement-1.cpp:10: divide by zero"]

    # Expected output
    expected_output = "CODE ERRORS AND INPUTS\nERROR NUMBER 1: KLEE: ERROR: tmp/concolic/annotated_if-statement-1.cpp:10: divide by zero\nCAUSING INPUT:\nx = -1\n\n"

    # Call the function
    klee_handler.print_error_inputs(tests, errors)

    # Capture the printed output
    captured_output = capsys.readouterr()
    printed_output = captured_output.out

    # Compare the printed output with the expected output
    assert printed_output == expected_output

def test_output_errors(capsys):
    """
    Tests the `output_errors` method by mocking the extract_errors method and capturing the printed output.
    """
    # Mock the errors returned by the extract_errors method
    errors = [
        "KLEE: ERROR: tmp/concolic/annotated_array_chars.cpp:37: memory error: object read only",
        "KLEE: ERROR: tmp/concolic/annotated_array_chars.cpp:37: memory error: out of bound pointer"
    ]
    klee_handler.extract_errors = lambda _: errors

    # Call the method
    returned_errors = klee_handler.output_errors()

    # Capture the printed output
    with patch('sys.stdout', new=StringIO()) as mock_stdout:
        klee_handler.output_errors()
        printed_output = mock_stdout.getvalue().strip()  # Strip trailing newline

    # Expected output
    expected_output = "========= ERROR OUTPUTS =========\n" \
                      "KLEE: ERROR: tmp/concolic/annotated_array_chars.cpp:37: memory error: object read only\n" \
                      "KLEE: ERROR: tmp/concolic/annotated_array_chars.cpp:37: memory error: out of bound pointer\n" \
                      "========= END OF ERROR OUTPUTS ========="

    # Remove whitespaces from the printed output and expected output
    printed_output = re.sub(r'\s', '', printed_output)
    expected_output = re.sub(r'\s', '', expected_output)

    # Compare the modified printed output with the modified expected output
    assert printed_output == expected_output

    # Check if the returned errors match the expected errors
    assert returned_errors == errors