"""
A model for TUUT files.
"""
import os
import clang

from utils.misc import include_lib, find_main_function_range, comment_out
from consept_vars import PATH_CONSEPT

# pylint: disable=too-many-nested-blocks
class TuutFile:
    """
    A abstraction for files to be tested. This abstraction is responsible for maintaining 
    local and container paths, as well as generating info about the file, such as the functions 
    it contains.

    Furthermore, specifically the annotating that is required by the FuzzHandler is carried out 
    by this abstraction.

    Attributes:
        file_name (str): The name of the file.
        file_path (str): The absolute path of the file.
        file_extension (str): The extension of the file.

    Methods:
        find_file_path(): Find the file path of a given file name in a directory tree.
        get_file_extension(): Returns the file extension.
        is_valid_file(): Verifies if the file is a valid type to test on.
    """

    def __init__(self, file_path):
        """
        Constructor of the TuutFile object.
        """

        # Initialize path_file attribute, path to the file that is related to self.
        self.path_file = file_path

        # Name of the file that is related to self
        self.file_name = os.path.basename(self.path_file)

        # Path to the annotated version of the file that is related to self
        self.path_fuzz_annotated = os.path.join(PATH_CONSEPT, 'tmp', 'fuzz', self.file_name)

        # file extension of the file that is related to self
        self.file_extension = self.get_file_extension()

        # details of the functions in the file that is related to self
        self.func_details = None

        # dictionary containing the functions and their starting lines
        self.func_dict = None

    def get_file_extension(self):
        """
        Returns the file extension.
        """
        _, file_extension = os.path.splitext(self.path_file)
        if not file_extension:
            raise ValueError(f"Invalid file type for file '{self.file_name}'.")
        return file_extension

    def is_valid_file(self):
        """
        Verifies if file is a valid type to test on.
        """
        valid_extensions = ['.cpp', '.cc', '.cxx', '.h']
        return self.file_extension in valid_extensions

    def gen_func_info(self):
        """
        Function that generates info about the functions in the file that is related to self.
        The function assigns function details (func_details) and function dictionary (func_dict)
        to self. Especially the function dictionary is important for deciding which function can
        be fuzzed by the FuzzHandler.

        Parameters:
            None

        Returns:
            None
        """

        index = clang.cindex.Index.create()
        translation_unit  = index.parse(self.path_file)

        func_decl_lines = []
        functions = []
        self.func_details = {}

        #traverse AST and create 2 dictionaries with the function details:
        #line -> func ; line -> [func name, # params]
        for node in translation_unit.cursor.walk_preorder():
            if not node.location.file is None and "include" not in str(node.location.file):
                if not str(node.location.file).endswith(".h"):
                    if (node.kind == clang.cindex.CursorKind.FUNCTION_DECL and
                        node.spelling != "main"):
                        func_decl_lines.append(node.location.line)
                        functions.append(node.spelling + " " + node.type.spelling)
                        param_count = 0
                        params = []
                        for child in node.get_children():
                            if child.kind == clang.cindex.CursorKind.PARM_DECL:
                                #append type of param and type of array if necessary
                                child_type = str(child.type.kind)
                                params.append([child_type[child_type.index(".") + 1:].lower(),
                                                child.type.get_array_element_type().spelling,
                                                child.type.get_array_size()])
                                param_count += 1
                        self.func_details[node.location.line] = [node.spelling, param_count, params]
        self.func_dict = dict(zip(func_decl_lines, functions))

    def include_fuzz(self):
        """
        This functions includes libraries related to fuzzing to the file corresponding to self.

        Parameters:
            self (TuutFile) : a

        Returns:
            None
        """

        include_lib(self.path_fuzz_annotated, self.path_fuzz_annotated, "#include <string.h>")
        include_lib(self.path_fuzz_annotated, self.path_fuzz_annotated, "#include <stdint.h>")
        include_lib(self.path_fuzz_annotated, self.path_fuzz_annotated, "#include <stddef.h>")

    def comment_out_main(self):
        """
        Function which finds out where the main function is and comments it out if it exists

        Parameters:
            self

        Returns:
            None
        """
        main = find_main_function_range(self.path_fuzz_annotated)
        if main[0]:
            comment_out(self.path_fuzz_annotated, main[1], main[2])

    @property
    def path_container_fuzz(self):
        """
        Propery of self. Returns the path to the file inside the fuzzing container when mounted.
        """
        return f'/home/consept/tmp/fuzz/{self.file_name}'
