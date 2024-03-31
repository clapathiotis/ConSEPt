# Consept - An Automated Testing Tool for C++ Developers


## Project Description

Consept is a Windows tool used to perform concolic testing on any class/module coded in C++. In order to perform concolic testing, Consept primarily integrates tools like [KLEE](http://klee.github.io/), [LibFuzzer](https://llvm.org/docs/LibFuzzer.html) and [Dextool](https://github.com/joakim-brannstrom/dextool).
KLEE is used to provide concolic testing capabilities by executing symbolic testing and providing concrete inputs for testing, LibFuzzer is used to provide fuzzing capabilities to the user and Dextool is used to offer the choice of mutation testing to the user.
It has to be noted that even though three different testing techniques are implemented into Consept, there is no interaction between the tools, but each one of them can be used through Consept.

## Install and Run Consept
### Installing
<a name="installation"></a>

To install Consept you need to follow the following steps:

Open a terminal and navigate to the directory where the repository will be cloned to.

```
cd path/to/directory
```

After that, copy the following command in your terminal.

```
git clone https://gitlab.tue.nl/aserebre/conSEPt.git
```

Finally, provide your login details for GitLab to authenticate and continue with the cloning of the repository.

### Running 
To run Consept you need to follow the following steps:

Ensure that you have a [Python3](https://www.python.org/downloads/) version installed (we used 3.10.11)  and [Docker](https://www.docker.com/) running in the background, we used version v4.20.1 for docker.
Version 16.0.0 of [LLVM](https://github.com/llvm/llvm-project/releases/tag/llvmorg-16.0.0) for installation.

Copy the json/cpp/MakeLists.txt file that you want to test into the sample_inputs folder.

Open a terminal and go to the project's directory where the repository has been cloned to.

```
cd path/to/directory/consept
```

Before you start working with consept you need to install all the libraries:

```
pip3 install -r requirements.txt
```

Copy and run the on of the following commands from the root directory in a terminal:

```
python3 src/consept.py -h
```

A help menu shall show up indicating all the possible flags that can be used.

## Project Example
Before you try these examples, please make sure that you have completed the full installation process by following the instructions at the [Install and Run Consept](#installation) section.

To verify that the project has been successfully installed, you can run the following examples:

### KLEE

NOTE: KLEE only works with compile_commands.json files

From the root directory run the following command and when prompted, choose which variables to annotate:

```
python3 src/conspet.py name_of_compile_commands.json -k
```

You can use `-tl [NUMBER]` to change the time limit for generating tests (in seconds). Default is 1 hour.
You can use `-s` to save the tests generated in the consept directory folder.

### LibFuzzer
NOTE: LibFuzzer works with cpp files

From the root directory run the following command and when prompt, choose which function to fuzz:

```
python3 src/consept.py file.cpp -fa
```

### Dextool
NOTE: Dextool works with MakeLists.txt files

From the root directory run the following command:

```
python3 src/consept.py /path/to/MakeLists.txt -m
```

More tests can be found in the ATP of our tool.

## General Use
For you own code to work with consept, you need to include the path to your file in the commands as displayed above, also use the help command as mentioned above for a detailed explanation of the tool's functions.


## Overview
Consept is a tool for creating concolic tests for C++ programs. Concolic testing combines concrete and symbolic execution to generate inputs that explore multiple paths through a program's execution. Consept allows you to easily define symbolic inputs and constraints, and automatically generates concrete test cases that satisfy those constraints.

Consept has the following capabilities:

- **Integrated with CMake:** Consept integrates with the CMake build system, so you can easily add concolic tests to your existing projects.

- **Support for popular C++ testing frameworks:** Consept supports popular C++ testing frameworks like Google Test and Catch2, so you can easily incorporate concolic tests into your existing test suites.


With Consept, you can improve the quality of your C++ programs by generating more thorough and efficient tests.


# Project structure
The following tree displays the files that have been created by our team.
```
Consept/
├── README.md
├── .gitlab-ci.yml
├── .gitignore
├── pylint_plugins
│   ├── check_cbo.py
│   └── comment_ratio.py
├── requirements.txt
├── src
│   ├── application_manager.py
│   ├── consept.py
│   ├── consept_vars.py
│   ├── fuzz_handler.py
│   ├── klee_handler.py
│   ├── mutation_handler.py
│   ├── tool_handler.py
│   ├── tools
│   │   ├── concolic
│   │   │   └── Dockerfile
│   │   ├── fuzz
│   │   │   └── Dockerfile
│   │   └── mutation
│   │       ├── Dockerfile
│   ├── tuut_file.py
│   └── utils
│       └── misc.py
├── tests
│   ├── __init__.py
│   ├── test_fuzz_handler.py
│   ├── test_klee_handler.py
│   ├── test_misc.py
│   ├── test_mutation_handler.py
│   └── test_tuut_file.py
└── tmp
    ├── concolic
    └── mutation
        ├── build.sh
        ├── run_dextool.sh
        └── test.sh
```

## Third Party Sources
The following files are origionally generated by third party tools and then have been edited by our team.
- `src/tools/mutation/dextool_config.toml` is a config file for Dextool 
- `.pylintrc` is autogenerated by pylint and then edited to meet Consept's needs.
- `.vscode/settings.json`

Additionally, everything within `sample_inputs/` is taken from third parties to use as test inputs to Consept.

## Auto-Generated Files
When running Consept `__pycache__` and `.pytest_cache` folders are auto-generated, as well as outputs from using mutation, fuzzing and concolic testing tools.

For mutation a HTML folder will be generated within `tmp/mutation` that displays Dextool's findings. Concolic testing will generate multiple files and place them within `tmp/concolic`. This consists of:
- `annotated_file.cpp` the annotated version of the file under test
- `klee-out-0` folder which contains: 
    - `.ktest` files that the tests are stored in
    - `run.stats` fetched by KLEE to display the coverage
    - `warnings.txt` which displays all the warning/error messages
- `test.bc` the bitcode of the annotated file 
- A shell script with a randomly generated name

Alternitavely, when running fuzzing the following files are generated within `tmp/fuzzing`:
- An annotated file to be fed to the fuzzer sharing the same name as the input file
- `crash-[NUMBER]` the crash report
- A shell script with a randomly generated name

## Checking Code
When checking code with third party tools we kindly ask to only check the files within the `src/` and `tests/` folders as those contain the source code code to Consept.

# Authors and acknowledgment
#### Matthias M.M Barendse
#### Tudor Dascălu
#### Clinton Emok
#### Timon Heuwekemeijer
#### Stavros Kannavas
#### Christoforos Lapathiotis
#### Chetan Laungani
#### Arjen van der Meer
#### Habeeb Mohammed
#### Horia Pivniceru
#### Alexander Serebrenik
#### Athanasios Tsalafoutas
#### Tanja de Winter