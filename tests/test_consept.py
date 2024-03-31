from consept import get_file_paths, create_parser

def test_get_file_paths_valid():
    """
    Test case: Valid compile_commands.json file

    This test case verifies the behavior of the get_file_paths function when provided with a valid compile_commands.json file.

    Expected behavior:
    - The function should retrieve the file paths from the compile_commands.json file.
    - Only file paths ending with '.cpp' should be included in the result.
    - The file name and annotated filename should be extracted correctly.
    """
    compile_commands_file = 'sample_inputs/array_chars_compile_commands.json'
    file_path, file_name, annotated_filename = get_file_paths(compile_commands_file)

    expected_file_path = ['/home/consept/tmp/concolic/annotated_array_chars.cpp']
    expected_file_name = 'array_chars.cpp'
    expected_annotated_filename = 'annotated_array_chars.cpp'

    print(file_path)
    print(file_name)
    print(annotated_filename)

    assert file_path == expected_file_path
    assert file_name == expected_file_name
    assert annotated_filename == expected_annotated_filename

def test_get_file_paths_invalid(capsys):
    """
    Test case: Invalid file path or compile_commands.json

    This test case verifies the behavior of the get_file_paths function when provided with an invalid file path or compile_commands.json.

    Expected behavior:
    - The function should handle the invalid file path or compile_commands.json and print the error message.
    - The function should return None values for file_path, file_name, and annotated_filename.

    Steps:
    1. Provide an invalid file path or compile_commands.json.
    2. Call the get_file_paths function with the invalid input.
    3. Verify that the function returns None for file_path, file_name, and annotated_filename.
    4. Verify that the function prints the error message.
    """

    # Step 1: Provide an invalid file path or compile_commands.json
    compile_commands_file = 'sample_inputs/invalid_path_compile_commands.json'

    # Step 2: Call the get_file_paths function with the invalid input
    file_path, file_name, annotated_filename = get_file_paths(compile_commands_file)

    # Step 3: Verify that the function returns None for file_path, file_name, and annotated_filename
    expected_file_path = None
    expected_file_name = None
    expected_annotated_filename = None
    assert file_path == expected_file_path
    assert file_name == expected_file_name
    assert annotated_filename == expected_annotated_filename

    # Step 4: Verify that the function prints the error message
    captured = capsys.readouterr()
    expected_error_message = "Error: Invalid file path or not a CPP file"
    assert expected_error_message in captured.out

def test_create_parser():
    parser = create_parser()

    # Test case 1: Only required argument provided
    argv = ['CMakeLists.txt']
    args = parser.parse_args(argv)
    assert args.file == 'CMakeLists.txt'
    assert not args.use_klee
    assert not args.use_mutation
    assert not args.save_tests
    assert args.time_limit == 3600
    assert not args.use_libFuzzer_with_address_sanitizer
    assert not args.use_libFuzzer_with_memory_sanitizer

    # Test case 2: All flags provided
    argv = [
        'CMakeLists.txt',
        '-k',
        '-m',
        '-s',
        '-tl', '1800',
        '-fa',
        '-fm'
    ]
    args = parser.parse_args(argv)
    assert args.file == 'CMakeLists.txt'
    assert args.use_klee
    assert args.use_mutation
    assert args.save_tests
    assert args.time_limit == 1800
    assert args.use_libFuzzer_with_address_sanitizer
    assert args.use_libFuzzer_with_memory_sanitizer

    # Test case 3: Custom values for time limit
    argv = [
        'CMakeLists.txt',
        '-tl', '1200'
    ]
    args = parser.parse_args(argv)
    assert args.file == 'CMakeLists.txt'
    assert not args.use_klee
    assert not args.use_mutation
    assert not args.save_tests
    assert args.time_limit == 1200
    assert not args.use_libFuzzer_with_address_sanitizer
    assert not args.use_libFuzzer_with_memory_sanitizer
