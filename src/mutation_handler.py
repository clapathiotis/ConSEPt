"""
Class that handles interactions with Dextool.
"""
import os
import toml

from application_manager import ApplicationManager
from consept_vars import MOUNTED_MUTATION_FOLDER
from tool_handler import ToolHandler

class DextoolHandler(ToolHandler): # pylint: disable=consider-using-enumerate
    """
    Class that handles interactions with Dextool.
    """
    def __init__(self,
                app_man: ApplicationManager = None,
                test: bool = False):
        # Initialize any necessary variables or configurations here
        super().__init__(app_man=app_man, tool='mutation', test=test)

    def start_dextool(self, cmakelists):
        '''
        Sets up Dextool by annotating relevent files and then starting up the docker container
        '''
        project_root = os.path.dirname(cmakelists)
        # self.annotate_cmakelists(project_root)

        # include_paths = self.include_paths(cmakelists)
        self.annotate_config_file()

        command = f'bash {MOUNTED_MUTATION_FOLDER}/run_dextool.sh'

        return super().run_tool(command, project_root)

    def annotate_config_file(self):
        '''
        Edits the dextool_config.toml file depending on the user project.
        '''
        config_file_path = os.path.join(os.path.dirname(__file__), 'tools',
                                        'mutation', 'dextool_config.toml')

        with open(config_file_path, "r", encoding='utf-8') as file:
            config = toml.load(file)

        config["workarea"]["root"] = "."
        config["database"]["db"] = 'dextool_mutate.sqlite3'
        config["analyze"]["exclude"] = ["test/*"]

        with open('./tmp/mutation/.dextool_mutate.toml', "w", encoding='utf-8') as file:
            toml.dump(config, file)

    def annotate_cmakelists(self, cmakelists):
        '''
        Edits the user's CMakeLists.txt file to fit with the relocated project in Docker.
        Adds the annotations in the CMakeLists.txt to link the libraries needed for mutation.
        '''
        new_content = [
            'enable_testing()',
            'set(CMAKE_CXX_STANDARD 14)',
            'set(CMAKE_CXX_STANDARD_REQUIRED ON)',
            '',
            'include(FetchContent)',
            'FetchContent_Declare(',
            '   googletest',
            '   URL https://github.com/google/googletest/archive/' +
                '03597a01ee50ed33e9dfd640b249b4be3799d395.zip'
            ')',
            'FetchContent_MakeAvailable(googletest)',
            '',
            'find_package(GTest REQUIRED)',
            'include_directories(${GTEST_INCLUDE_DIRS})'
        ]
        # search if the new lines are already in the CMakeLists.txt
        with open(cmakelists, 'r', encoding='utf-8') as file:
            content = file.readlines()
            aux = 0
            for content_item in new_content:
                for line in content:
                    if content_item not in line:
                        aux = aux + 1

        # write the new lines in the CMakeLists.txt from the container
        with open(cmakelists, 'w', encoding='utf-8') as file:
            for line in content:
                if ('add_library(gtest ${GTEST_DIR}/gmock-gtest-all.cc ${GTEST_DIR}/main.cc)'
                    in line) or ('target_include_directories(gtest PUBLIC ${GTEST_DIR})'
                    in line ) or ('target_link_libraries(gtest pthread)' in line):
                    pass
                elif 'target_link_libraries(rl_test gtest variant termbox m)' in line:
                    cmakelists = file.writelines('target_link_libraries(rl_test' +
                                                 ' ${GTEST_BOTH_LIBRARIES} ' +
                                                 'pthread variant termbox m)\n')
                else:
                    cmakelists = file.writelines(line)
                if aux <= 500:
                    if 'project(' in line:
                        cmakelists = file.writelines("\n")
                        for content_item in new_content:
                            cmakelists = file.writelines(content_item)
                            cmakelists = file.writelines("\n")
