"""
Creates test cases for the mutation module
"""
import tempfile
import os
import toml
from mutation_handler import DextoolHandler

FILEFOLDER = "sample_inputs"
mutation_handler = DextoolHandler(test=True)


def test_annotate_cmakelists_1():
    '''
    Method to test if the CMakeLists.txt has enable testing activated
    '''
    file_path = os.path.abspath(os.path.join(FILEFOLDER, "CMakeLists-1.txt"))

    # Create a temporary output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', encoding='utf-8', delete=False
                                     ) as output_file:
        output_file_path = output_file.name

    # Read contents of the target file
    with open(file_path, 'r', encoding='utf-8') as file:
        contents = file.readlines()

    # Copy contents of the target file into the temporary file we test
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.writelines(contents)

    # Annotate the temporary file
    mutation_handler.annotate_cmakelists(output_file_path)

    # Check that the output file contains the annotated links
    with open(output_file_path, 'r', encoding='utf-8') as file:
        file_contents = file.readlines()
        assert 'enable_testing()\n' in file_contents

    # Remove the temporary output file
    if os.path.exists(output_file_path):
        os.remove(output_file_path)


def test_annotate_cmakelists_2():
    '''
    Method to test if CMakeLists.txt is setting cmake to the right version
    '''
    file_path = os.path.abspath(os.path.join(FILEFOLDER, "CMakeLists-1.txt"))

    # Create a temporary output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', encoding='utf-8', delete=False
                                     ) as output_file:
        output_file_path = output_file.name

    # Read contents of the target file
    with open(file_path, 'r', encoding='utf-8') as file:
        contents = file.readlines()

    # Copy contents of the target file into the temporary file we test
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.writelines(contents)

    # Annotate the temporary file
    mutation_handler.annotate_cmakelists(output_file_path)

    # Check that the output file contains the annotated links
    with open(output_file_path, 'r', encoding='utf-8') as file:
        file_contents = file.readlines()
        assert 'set(CMAKE_CXX_STANDARD 14)\n' in file_contents
        assert 'set(CMAKE_CXX_STANDARD_REQUIRED ON)\n' in file_contents

    # Remove the temporary output file
    if os.path.exists(output_file_path):
        os.remove(output_file_path)


def test_annotate_cmakelists_3():
    '''
    Method to test for fetching google test in the cmakelists.txt
    '''
    file_path = os.path.abspath(os.path.join(FILEFOLDER, "CMakeLists-1.txt"))

    # Create a temporary output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', encoding='utf-8', delete=False
                                     ) as output_file:
        output_file_path = output_file.name

    # Read contents of the target file
    with open(file_path, 'r', encoding='utf-8') as file:
        contents = file.readlines()

    # Copy contents of the target file into the temporary file we test
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.writelines(contents)

    # Annotate the temporary file
    mutation_handler.annotate_cmakelists(output_file_path)

    # Check that the output file contains the annotated links
    with open(output_file_path, 'r', encoding='utf-8') as file:
        file_contents = file.readlines()
        assert 'include(FetchContent)\n' in file_contents
        assert 'FetchContent_Declare(\n' in file_contents
        assert '   googletest\n' in file_contents
        assert ('   URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip)\n' in file_contents)
        assert 'FetchContent_MakeAvailable(googletest)\n' in file_contents

    # Remove the temporary output file
    if os.path.exists(output_file_path):
        os.remove(output_file_path)


def test_annotate_cmakelists_4():
    '''
    Method to test if google test is fetched in the CMakeLIsts.txt
    '''
    file_path = os.path.abspath(os.path.join(FILEFOLDER, "CMakeLists-1.txt"))

    # Create a temporary output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', encoding='utf-8', delete=False
                                     ) as output_file:
        output_file_path = output_file.name

    # Read contents of the target file
    with open(file_path, 'r', encoding='utf-8') as file:
        contents = file.readlines()

    # Copy contents of the target file into the temporary file we test
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.writelines(contents)

    # Annotate the temporary file
    mutation_handler.annotate_cmakelists(output_file_path)

    # Check that the output file contains the annotated links
    with open(output_file_path, 'r', encoding='utf-8') as file:
        file_contents = file.readlines()
        assert 'find_package(GTest REQUIRED)\n' in file_contents
        assert 'include_directories(${GTEST_INCLUDE_DIRS})\n' in file_contents

    # Remove the temporary output file
    if os.path.exists(output_file_path):
        os.remove(output_file_path)


def test_annotate_cmakelists_5():
    '''
    Method to check for link libraries of gtest
    '''
    file_path = os.path.abspath(os.path.join(FILEFOLDER, "CMakeLists-1.txt"))

    # Create a temporary output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', encoding='utf-8', delete=False
                                     ) as output_file:
        output_file_path = output_file.name

    # Read contents of the target file
    with open(file_path, 'r', encoding='utf-8') as file:
        contents = file.readlines()

    # Copy contents of the target file into the temporary file we test
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.writelines(contents)

    # Annotate the temporary file
    mutation_handler.annotate_cmakelists(output_file_path)

    # Check that the output file contains the annotated links
    with open(output_file_path, 'r', encoding='utf-8') as file:
        file_contents = file.readlines()
        assert 'target_link_libraries(rl_test ${GTEST_BOTH_LIBRARIES} pthread variant termbox m)\n' in file_contents

    # Remove the temporary output file
    if os.path.exists(output_file_path):
        os.remove(output_file_path)


def test_annotate_cmakelists_6():
    '''
    Method to ccheck if the old links to gtest are deleted
    '''
    file_path = os.path.abspath(os.path.join(FILEFOLDER, "CMakeLists-1.txt"))

    # Create a temporary output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', encoding='utf-8', delete=False
                                     ) as output_file:
        output_file_path = output_file.name

    # Read contents of the target file
    with open(file_path, 'r', encoding='utf-8') as file:
        contents = file.readlines()

    # Copy contents of the target file into the temporary file we test
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.writelines(contents)

    # Annotate the temporary file
    mutation_handler.annotate_cmakelists(output_file_path)

    # Check that the output file does not contain the old links to gtest
    with open(output_file_path, 'r', encoding='utf-8') as file:
        file_contents = file.readlines()
        assert 'add_library(gtest ${GTEST_DIR}/gmock-gtest-all.cc ${GTEST_DIR}/main.cc)\n' not in file_contents
        assert 'target_include_directories(gtest PUBLIC ${GTEST_DIR})\n' not in file_contents
        assert 'target_link_libraries(gtest pthread)\n' not in file_contents

    # Remove the temporary output file
    if os.path.exists(output_file_path):
        os.remove(output_file_path)

def test_annotate_config_file():
    '''
    Method to test if the configuration file is annotated good
    '''
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src',
                             'tools', 'mutation', 'dextool_config.toml')

    mutation_handler.annotate_config_file()

    # Check that the output file does not contain the old links to gtest
    with open(file_path, 'r', encoding='utf-8') as file:
        config = toml.load(file)
        assert config["workarea"]["root"] == "."
        assert config["database"]["db"] == 'dextool_mutate.sqlite3'
