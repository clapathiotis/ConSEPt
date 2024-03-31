"""
This module provides a utility to run libfuzzer on a given file to be tested. This includes 
functions which ask for the fuzzing target and automatically annotate the file to enable fuzzing.  
"""

import string

from tuut_file import TuutFile
from application_manager import ApplicationManager
from tool_handler import ToolHandler

def generate_next_letter(counter):
    """
    Generates a letter for the initialization of new varaibles within the fuzz target.

    Parameters:
    None

    Returns:
    letter (int): the ascii code of the new generated letter
    """
    letter = string.ascii_lowercase[counter]
    counter = (counter + 1) % 26
    return letter

def ask_for_annotation_choice_fuzz(func_dict, func_details) -> int:
    """
    Prompt the user for the choice of variable annotation for fuzzing.

    Args:
        unique_dict (dict): Dictionary of declaration line and variable correspondence for fuzzing.

    Returns:
        List[int]: List of valid row numbers of variable locations for fuzzing.
    """

    # Ask user for input
    while True:
        print("\nChoose which function to fuzz:")
        print(func_dict)
        choice = input("Enter your choice (only one line number): ")

        row = int(choice)
        # check for invalid line and function with no params
        if row not in func_dict.keys() or func_details.get(row)[1] == 0:
            print("Invalid input")
            continue
        return choice


class FuzzHandler(ToolHandler):
    """
    Class that handles interactions with the LibFuzzer tool 
    """

    def __init__(self,
                 app_man: ApplicationManager = None,
                 test: bool = False):
        super().__init__(tool='fuzz', test=test, app_man=app_man)

        # initialize the counter responisble for generating unique variable names
        self.counter = 0

    def increase_counter(self):
        """
        This function increases the counter
        """

        self.counter += 1

    def next_letter(self):
        """
        Generates a letter for the initialization of new varaibles within the fuzz target.

        Parameters:
            None

        Returns:
            letter (int): the ascii code of the new generated letter
        """
        letter = string.ascii_lowercase[self.counter]
        self.counter = (self.counter + 1) % 26
        return letter

    def annotate_fuzz(self, tuut : TuutFile, choice):
        """
        Functions which automatically annotates the file that is to be tested based on the choice 
        parameter.

        Parameters:
            tuut (TuutFile): To be tested file abstraction
            choice (int): row of the choice function to be targeted by fuzzing

        Returns: 
            None
        """

        content = []
        row = int(choice)

        #open file to be annotated and read its contents
        with open(tuut.path_file, 'r', encoding='utf-8') as file:
            content = file.readlines()

        #write annotations to a new file
        with open(tuut.path_fuzz_annotated, 'w', encoding='utf-8') as output_file:
            output_file.writelines(content)
            output_file.write(
            '\nextern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {\n\n')

            #create list store the names of variables(the vars we feed as params)
            var_names = []
            #count the total size of the params
            size_counter = 0

            #declare variables to be fed as params
            for param in tuut.func_details.get(row)[2]:
                if str(param[0]) == 'constantarray':
                    name = str(self.next_letter())
                    var_names.append(name)
                    size_counter += int(param[2])
                    output_file.write("    " + str(param[1]) + " " +
                                        name + "[" + str(param[2]) + "];\n")
                else:
                    name = str(self.next_letter())
                    var_names.append(name)
                    size_counter += 1
                    output_file.write("    " + str(param[0]) + " " + name + "[1];\n")

            #check size of input of the fuzzer
            output_file.write("\n    if(Size == " + str(size_counter) + "){\n\n")

            #keep count of how memory to allocate to each param
            memory = 0

            #perform memcpy from data given by fuzzer to declared vars
            for index, param in enumerate(tuut.func_details.get(row)[2]):
                #check to see if the parameter is an array or not
                if str(param[0]) == 'constantarray':
                    output_file.write(
                        f'        memcpy({var_names[index]}, Data + {memory}, {param[2]});\n')
                    memory += param[2]
                else:
                    output_file.write(
                        f'        memcpy({var_names[index]}, Data + {memory}, 1);\n')
                    memory += 1

            #call the function to be fuzzed
            output_file.write(f'        {tuut.func_details.get(row)[0]}(')

            #pass the params to the function to be fuzzed
            for index, param in enumerate(tuut.func_details.get(row)[2]):
                if index != len(var_names) - 1:
                    if str(param[0]) == 'constantarray':
                        output_file.write(f'{var_names[index]}, ')
                    else:
                        output_file.write(f'{var_names[index]}[0], ')
                else:
                    if str(param[0]) == 'constantarray':
                        output_file.write(f'{var_names[index]});')
                    else:
                        output_file.write(f'{var_names[index]}[0]);')

            #return 0 and close the square brackets of the main function
            output_file.write("\n\n    }")
            output_file.write("\n    return 0;\n}")

    def run(self):
        """
        This function runs a container of the image corresponding to this tool.
        In this container it runs the current script
        Before calling the run() function of the super class, it adds the command to move all 
        crash file to the mount folder such that these can be accessed from outside the container.

        Arguments:
            None
        Returns:
            None
        """

        self.add_command('cp ./crash* /home/consept/tmp/fuzz')
        super().run()
