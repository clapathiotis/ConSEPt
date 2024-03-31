"""
This module provides a utility to run KLEE on a given file to be tested. It includes functions to
start KLEE, process errors and output them in a readable format, inlude the KLEE library, 
annotate the c++ with symbolic functions on the variables to be tested.

Functions:
    - run_klee(annotated_file_path)
    - output_errors()
    - analyze_ktest_files(ktests_directory)
    - print_error_inputs(tests, errors)
    - extract_errors(errors_path)
    - get_error_inputs(tests, num_of_errors)
    - include_library(file_path, target_output_file_path)
    - annotate_variables(file_path, output_file_path)
    - insert_annotations(content, rows, unique_dict)
    - ask_for_annotation_choice_klee(unique_dict)
"""
import os
import re
import json
import docker
import clang.cindex

from consept_vars import PATH_CONSEPT
from tool_handler import ToolHandler
from application_manager import ApplicationManager
from utils.misc import include_lib

class KLEEHandler(ToolHandler):
    """
    Class that handles interactions with KLEE symbolic execution tool.
    """
    def __init__(self,
                 app_man: ApplicationManager = None,
                 test: bool = False):
        # Initialize any necessary variables or configurations here
        super().__init__(app_man=app_man, tool='concolic', test=test)

    def run_klee(self, compile_commands_path, annotated_file_path, time_limit) -> None:
        """
        This function runs the klee commands in order to generate the tests on the annotated
        variables set by the user.
        Output test statistics using 'klee-stats' inside a container.
        Parameters: File path of the annotated file from the compile_commands_path, timelimit
        Returns: None
        """
        # Retrieve the compile command from compile_commands.json
        with open(compile_commands_path, 'r', encoding='utf-8') as f:
            compile_commands = json.load(f)
        compile_command = next(
            (cmd['command'] for cmd in compile_commands),
            None
        )
        if compile_command is None:
            self.logger.error(f'No compile command found for file: {annotated_file_path}')
            return

        # Start new shell script to add KLEE commands
        self.open_new_script()
        self.logger.info(f'Created new script {self.path_cur_script}, will now run KLEE')

        # Extract the directory path from the annotated file path
        annotated_file_dir = os.path.dirname(annotated_file_path)

        # Adjust the compile command to include the correct directory path
        compile_command = compile_command.replace(annotated_file_dir, '/home/consept/tmp/concolic')
        self.add_command(f'{compile_command} -o /home/consept/tmp/concolic/test.bc')
        self.add_command('klee --external-calls=all '
                        f'--max-time={time_limit} /home/consept/tmp/concolic/test.bc')
        self.run()

        # Output stats regarding coverage
        command = "klee-stats tmp/concolic/klee-out-0"
        self.app_man.run_container(self.tool, command=command, remove_afterwards=False)


    def output_errors(self) -> list:
        """
        Extract and print the errors from the KLEE output folder.
        Returns:
            errors (list): List of error messages.
        """
        name_output_folder = 'klee-out-0'
        # Extract the errors and print
        local_errors_path = os.path.join(PATH_CONSEPT, 'tmp', self.tool, name_output_folder)
        errors = self.extract_errors(local_errors_path)
        if errors:
            print("\n ========= ERROR OUTPUTS =========")
            for line in errors:
                print(line)
        print("\n ========= END OF ERROR OUTPUTS =========")

        return errors

    def extract_errors(self, errors_path) -> list:
        """
        This method reads the 'messages.txt' file located in the specified errors path and extracts
        any lines that start with 'KLEE: ERROR:' and are returned as a list of strings.
        Parameters:
            errors_path (str): Path to the errors directory containing the 'messages.txt' file.
        Returns:
            errors (list): A list of strings representing the extracted errors.
        """
        errors = []
        # Construct the path to the 'messages.txt' file
        messages_file = errors_path + '/messages.txt'

        with open(messages_file, 'r', encoding='utf-8') as f:
            # Iterate over each line in the 'messages.txt' file and check for any errors
            for line in f:
                if line.startswith('KLEE: ERROR:'):
                    errors.append(line.strip())
        return errors

    def analyze_ktest_files(self, ktests_directory):
        """
        This method analyzes the ktest files present in the given directory using the
        'ktest-tool' command inside a container on all .ktest files.
        It captures the generated tests and returns them as a string.

        Parameters:
            ktests_directory (str): Directory containing the ktest files.
        Returns:
            tests (array): A string array containing the fetched tests if successful,
                            None otherwise.
        """
        # Find all the .ktest files and append them into an array
        ktest_files = []
        for root, _dirs, files in os.walk(ktests_directory):
            for file in files:
                if file.endswith('.ktest'):
                    ktest_file = os.path.join(root, file)
                    ktest_files.append(ktest_file)

        # Construct the command
        ktest_command = 'ktest-tool ' + ' '.join(ktest_files)
        # Execute ktest-tool command and capture generated tests
        try:
            container, output_stream = self.app_man.run_container(self.tool, ktest_command,
                                                                   remove_afterwards=False)
            # Fetching and saving of tests in array tests[str]
            output_bytes = b''
            self.logger.info("Fetching tests\n")
            for chunk in output_stream:
                if isinstance(chunk, int):
                    chunk = bytes([chunk])
                output_bytes += chunk
            tests = output_bytes.decode('utf-8')
            self.logger.info("Tests generated successfuly\n")
            container.remove()
            return tests
        except docker.errors.APIError as execption:
            print(f"\nError executing ktest-tool: {execption}")
            return None

    def print_error_inputs(self, tests, errors):
        """
        Print the code errors and corresponding inputs causing the error.
        Args:
            tests (array): Array of string error tests generated by KLEE.
            errors (list): List of error messages.
        Returns:
            None
        """
        inputs, names, num_of_objects = self.get_error_inputs(tests, len(errors))
        error_string = "CODE ERRORS AND INPUTS"
        input_counter = 0

        for i, error in enumerate(errors):
            error_string += f'\nERROR NUMBER {i+1}: {error}\nCAUSING INPUT:\n'
            for _ in range(num_of_objects):
                # Handle cases where the number of objects is greater than
                # the available names and inputs
                if input_counter >= len(names) or input_counter >= len(inputs):
                    break
                error_string += f'{names[input_counter]} = {inputs[input_counter]}\n'
                input_counter += 1
        print(error_string)

    def get_error_inputs(self, tests, num_of_errors):
        """
        Finds the inputs and related symbols that cause errors from the generated tests.
        Parameters:
        tests (array): The string array of tests generated by klee.
        num_of_errors (int): Number of errors found by klee.
        Returns:
        inputs (int): the inputs leading to errors in file under test
        names (string): names of the symbols related to error causing inputs
        num_of_objects (int): number of symbolic variables
        """
        inputs = []
        indices = []
        names = []
        name_pattern = r"^object\s(\d+):\sname:\s'([^']+)'\s*$"
        input_pattern = r'^object\s(\d+):\sint\s:\s(-?\d+)\s*$'
        num_of_objects_pattern = r'^num objects:\s(\d+)$'
        num_of_objects = 0
        # Locate start and end of tests related to errors
        for i, line in enumerate(tests.splitlines()):
            if "ktest file" in line.lower() or i == len(tests.splitlines())-1:
                indices.append(i)
            if len(indices) > num_of_errors:
                break

        # Parse error related tests for their inputs and symbols using regex
        found = False
        for i, line in enumerate(tests.splitlines()):
            if i > indices[num_of_errors]:
                break

            input_match = re.match(input_pattern, line)
            if input_match:
                inputs.append(int(input_match.group(2)))

            name_match = re.match(name_pattern, line)
            if name_match:
                names.append(name_match.group(2))

            objects = re.match(num_of_objects_pattern, line)
            if objects and (not found):
                num_of_objects = objects.group(1)
                found = True

        return inputs, names, int(num_of_objects)

    def include_library(self, file_path, target_output_file_path = None) -> str:
        """
        Includes the KLEE library in the specified C++ file in the compile_commands.

        Parameters:
        annotated_file_path (str): The path to the input, annotated C++ file.

        Returns:
        output_file_path (str): path of the annotated file.
        """
        include_line = "#include <klee/klee.h>"

        annotated_filename = os.path.basename(file_path)
        if target_output_file_path is not None:
            output_file_path = target_output_file_path
        else:
            output_file_path = os.path.join(
                PATH_CONSEPT, 'tmp', 'concolic', annotated_filename)

        self.logger.info(f'Will now include klee in file {file_path}')
        include_lib(file_path, output_file_path, include_line)

        return output_file_path

    def annotate_variables(self, file_path, target_output_file_path=None) -> str:
        """
        Annotates variables in the given file with KLEE symbolic execution annotations,
        and saves the annotated file as a new file.
        Args:
            file_path (str): Path to the input file stored anywhere in Consept.
            output_file_path (str): Path to the annotated, output file.
        Returns:
            output_file_path (str) : Path to the annotated file.
        """
        # Load the translation unit
        index = clang.cindex.Index.create()
        translation_unit = index.parse(file_path)

        # Collect variable names and line numbers of variable declarations
        variables = []
        var_decl_lines = []
        for node in translation_unit.cursor.walk_preorder():
            # Verify whether the declared variable is present in main method of source file
            if (node.kind == clang.cindex.CursorKind.VAR_DECL and
                node.semantic_parent.kind == clang.cindex.CursorKind.FUNCTION_DECL and
                    node.semantic_parent.spelling == 'main'):
                # Append variables and their declaration lines in arrays variables, var_decl_lines
                variables.append(node.spelling)
                var_decl_lines.append(node.extent.start.line)

        # Create dictionary with declaration line and variable correspondence
        dictionary = dict(zip(var_decl_lines, variables))
        # Remove duplicate declared variables while maintaining original order
        unique_dict = {
            key: value
            for key, value in dictionary.items()
            if list(dictionary.values()).count(value) == 1
        }
        rows = self.ask_for_annotation_choice_klee(unique_dict)
        # Read the original file content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()

        annotated_content = self.insert_annotations(content, rows, unique_dict)
        # Write the annotated content to the output file
        annotated_filename = 'annotated_' + os.path.basename(file_path)
        if target_output_file_path is not None:
            output_file_path = target_output_file_path
        else:
            output_file_path = os.path.join(
                PATH_CONSEPT, 'tmp', 'concolic', annotated_filename)
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.writelines(annotated_content)
        return output_file_path

    def insert_annotations(self, content, rows, unique_dict):
        """
        Insert annotations into the original content based on the selected rows.

        Args:
            content (list): List of lines in the original content.
            rows (list): List of valid row numbers to annotate.
            unique_dict (dict): Dictionary of declaration line and variable correspondence.
        Returns:
            list: List of lines with annotations.
        """
        annotated_content = []
        for line_number, line in enumerate(content, start=1):
            annotated_content.append(line)
            if line_number in rows:
                variable = unique_dict[line_number]
                self.logger.info(
                    f'Making variable {variable} at line {line_number} symbolic')
                # Create annotation and append it to the new annotated file
                annotation = (
                    f'\tklee_make_symbolic(&{variable}, sizeof({variable}), '
                    f'"{variable}");\n'
                )
                annotated_content.append(annotation)
        return annotated_content

    def ask_for_annotation_choice_klee(self, unique_dict):
        """
        Prompt the user for the choice of variable annotation for klee.

        Args:
            unique_dict (dict): Dictionary of declaration line and variable correspondence for klee.
        Returns:
            List[int]: List of valid row numbers of variable locations for klee.
        """
        while True:
            print("\nChoose what to annotate:")
            print("1. All variables")
            print("2. Select specific variables")
            choice = input("Enter your choice (1 or 2): ")

            if choice == "1":
                return list(unique_dict.keys())  # Annotate all variables
            if choice == "2":
                # Display variables and their line numbers to the user
                print("Choose what to annotate: ", unique_dict)
                # Receive input and extract the code lines
                to_be_annotated = input("Enter rows here (comma-separated): ")
                rows = [int(row.strip()) for row in to_be_annotated.split(",")]

                invalid_rows = False
                if not rows:
                    print("\nInvalid input provided")
                    invalid_rows = True

                # Check if all forws exist in dictionary of variables
                if not all(row in unique_dict for row in rows):
                    print("\nInvalid row(s) provided")
                    invalid_rows = True

                if not invalid_rows:
                    return rows

            # Print message to user for invalid characters in the input
            print("\nInvalid choice")
