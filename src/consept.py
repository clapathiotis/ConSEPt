"""
This module provides a utility to run KLEE on a given file. It includes functions to
analyze a file with KLEE, save or display the test cases, and find the file path.

Functions:
    - start_consept()
    - find_file_path(file_name, start_dir=".")
"""

# pylint: disable=wrong-import-position
import argparse
import json
import os
from pathlib import Path

from application_manager import ApplicationManager

from klee_handler import KLEEHandler
from mutation_handler import DextoolHandler
from fuzz_handler import FuzzHandler, ask_for_annotation_choice_fuzz

from tuut_file import TuutFile
from utils.misc import find_file_path
from consept_vars import PATH_CONSEPT

def start_consept():
    """
    Run testing tools on a given file and optionally save and display
    the test cases.

    It expects a compile_command.json file as a positional argument to optionally use KLEE
    to analyze the file, save the test cases to a file, or display the test
    cases on the console. Can also use other tools like Dextool and Libfuzzer as mentioned below.

    Examples:
    To analyze a file named "example.cpp" with KLEE and save the test cases to a file, run:
    $ python3 src/consept.py example_compile_commands.json -k -s

    To analyze a file named "address_memory_error.cpp" with libFuzzer in order to search for
    an address related error, run:
    $ python3 src/consept.py address_memory_error.cpp -fa

    To analyze a file named "address_memory_error.cpp" with libFuzzer in order to search for
    a memory related error, run:
    $ python3 src/consept.py address_memory_error.cpp -fm

    To analyze a project named "game_tutorial" with Dextool for mutation testing, run:
    $ python3 src/consept.py path/to/the/folder/of/the/poject/conatining/CMakeLists.txt -m 
    """
    parser = create_parser()
    args = parser.parse_args()
    cmakelists = args.file
    user_project = os.path.dirname(cmakelists)
    errors = None
    tests = None

    if args.use_mutation:
        tool_am = ApplicationManager(['mutation'], user_project)
        handler = DextoolHandler(tool_am)
        handler.annotate_cmakelists(cmakelists)
        handler.start_dextool(cmakelists)

    if args.use_klee:
        compile_commands = find_file_path(args.file)
        _file_paths, file_name_tested, annotated_filename = get_file_paths(compile_commands)

        if args.time_limit <= 0:
            parser.error("The time limit must be a positive integer.")
        if not _file_paths:
            parser.error("Invalid path")

        # Initialize KLEEHandler
        tool_app_man = ApplicationManager(['concolic'])
        kleeh = KLEEHandler(app_man=tool_app_man)

        # Empty the mount folder
        kleeh.empty_mount_folder()

        # Get the test file and annotate variables
        test_file_name = file_name_tested
        testfile_path = find_file_path(test_file_name)
        kleeh.annotate_variables(testfile_path)

        # Set the path to annotated file
        annotated_file_path = os.path.join(PATH_CONSEPT, 'tmp', 'concolic', annotated_filename)

        # Include in the annotated file the KLEE library
        kleeh.include_library(annotated_file_path)

        # Run KLEE
        kleeh.run_klee(compile_commands, annotated_file_path, args.time_limit)

        # Get the errors found by KLEE and output them nicely
        errors = kleeh.output_errors()

        # Set the directory path for the generated tests
        ktests_directory = 'tmp/concolic/klee-out-0/'

        # Analyze the ktest files to extract test information
        tests = kleeh.analyze_ktest_files(ktests_directory)

        if errors:
            # Print error inputs
            kleeh.print_error_inputs(tests, errors)
        else:
            print("\nNo errors found by the generated tests")

    if args.use_libFuzzer_with_address_sanitizer | args.use_libFuzzer_with_memory_sanitizer:

        assert args.file.endswith('.cpp'), 'For fuzzing, one specific cpp file needs to be entered'

        path_file = Path(args.file)

        if len(path_file.parts) == 1: # only the basename was provided
            path_file = find_file_path(args.file)
        else: # path to the file is just the path that was provided
            path_file = str(path_file)

        # init ApplicationManager, FuzzHandler and TuutFile
        tool_am = ApplicationManager(['fuzz'])
        fuzh = FuzzHandler(app_man=tool_am)
        tuut = TuutFile(path_file)

        # generate function information about the file to be tested
        tuut.gen_func_info()

        # ask which function in the file to be tested will be the fuzzing target
        choice = ask_for_annotation_choice_fuzz(tuut.func_dict, tuut.func_details)

        # annotate specifically the funciton of this file
        fuzh.annotate_fuzz(tuut, choice)

        # comment out the main function
        tuut.comment_out_main()

        #include fuzzing libraries in the to be tested file
        tuut.include_fuzz()

        # start a new script that will be executed inside the fuzzing container
        fuzh.open_new_script()

        if args.use_libFuzzer_with_address_sanitizer:
            fuzh.add_command(
                f'clang++ -g -fsanitize=address,fuzzer -o tmp/fuzz/fuzz_output \
                    {tuut.path_container_fuzz}')
        elif args.use_libFuzzer_with_memory_sanitizer:
            fuzh.add_command(
                f'clang++ -g -fsanitize=memory,fuzzer -o tmp/fuzz/fuzz_output \
                    {tuut.path_container_fuzz}')

        fuzh.add_command('tmp/fuzz/fuzz_output -runs=1000')

        # run the container and the script inside of it
        fuzh.run()

    if args.save_tests:
        # Save tests to a file in the Consept folder directory
        file_name = input("Enter the name of the file to save the tests to: ")
        file_name = file_name + ".txt"
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(tests)
        print(f"Tests saved to file: {file_name}")

def create_parser():
    """
    Create and configure the command-line argument parser for the Consept utility.

    Returns:
        argparse.ArgumentParser: The configured argument parser.

    The parser is configured to accept the following arguments:

    Positional arguments:
        file: Absolute path to the file (e.g., CMakeLists.txt).

    Optional arguments:
        -k, --use-klee: Use KLEE to analyze the file.
        -m, --use-mutation: Use DexTool to analyze the file.
        -s, --save-tests: Save the test cases to a file.
        -tl, --time-limit: Set a custom time limit in seconds (default: 3600).
        -fa, --use-libFuzzer-with-address-sanitizer: Use libFuzzer to analyze the file
                and detect address related issues.
        -fm, --use-libFuzzer-with-memory-sanitizer: Use libFuzzer to analyze the file
                and detect memory related issues.
    """
    parser = argparse.ArgumentParser(
        description='Utility to run KLEE on a given file.')
    parser.add_argument('file', metavar='CMakeLists.txt', type=str,
                        help='Absolute path to the file')
    parser.add_argument('-k', '--use-klee', action='store_true',
                        help='Use KLEE to analyze the file')
    parser.add_argument('-m', '--use-mutation', action='store_true',
                        help='Use DexTool to analyze the file')
    parser.add_argument('-s', '--save-tests', action='store_true',
                        help='Save the test cases to a file')
    parser.add_argument('-tl', '--time-limit', type=int, default=3600,
                        help='Set a custom time limit in seconds')
    parser.add_argument('-fa', '--use-libFuzzer-with-address-sanitizer', action='store_true',
                        help='Use libFuzzer to analyze the file and detect address related issues')
    parser.add_argument('-fm', '--use-libFuzzer-with-memory-sanitizer', action='store_true',
                        help='Use libFuzzer to analyze the file and detect memory related issues')
    return parser


def get_file_paths(compile_commands_file):
    '''
    Retrieves the file paths from the compile_commands.json
    '''
    with open(compile_commands_file, 'r', encoding='utf-8') as file:
        compile_commands = json.load(file)

    file_paths = []

    for command in compile_commands:
        file_path = command['file']
        # Checks if file ends with .cpp
        annotated_filename = os.path.basename(file_path)
        # Remove the "annotated_" part from the file to display
        # file name being tested before annotation
        file_name = annotated_filename.replace("annotated_", "")
        print("Current file being tested:" , file_name)
        if file_path.endswith('.cpp'):
            file_paths.append(file_path)
        else:
            print(f"\n\nError: Invalid file path or not a CPP file: {file_path}")
            return None, None, None
    return file_paths, file_name, annotated_filename

if __name__ == '__main__':
    start_consept()
