"""
This module provides the abstraction for all tool handlers.
The ToolHandler parent class is responsible for interfacing with the ApplicationManager,
as well as faciliting the construction of the bash script
that is executed when running a specific tool
"""

import logging
import os
import shutil
import sys
import stat
from datetime import datetime
from pathlib import Path
from pydos2unix import dos2unix

from consept_vars import ARR_ALLOWED_TOOLS
from application_manager import ApplicationManager

PATH_ABSOLUTE = str(Path(os.path.realpath(__file__)).parent)
PATH_CONSEPT = str(Path(PATH_ABSOLUTE).parents[0])

logging.basicConfig(stream=sys.stdout, level=logging.info)


class ToolHandler:
    """
    Class serves as the abstraction for all tool handlers.
    """

    def __init__(self,
                 tool: str,
                 test: bool,
                 app_man: ApplicationManager = None
                 ):
        """"
        Constructor for the ToolHandler class
        This function attributes the application manager and tool parameter to
        the instantiated ToolHandler (self).
        If the test parameter is set to TRUE, the handler is in testing mode and
        no image is built or container is run.

        Parameters:
        tool (str) : The kind of tool this handler is assigned to
        test (bool) : Activation of testing mode
        am (ApplicationManager) : The singleton application manager of consept
        """

        # Confirm the validity of the tool parameter
        assert tool in ARR_ALLOWED_TOOLS, f'tool parameter ({tool})' + \
            f' should be one of {ARR_ALLOWED_TOOLS}'

        self.tool = tool
        self.test = test

        # If not testing mode,
        if not self.test:
            assert app_man is not None, 'If test is false, an ApplicationManager instance \
                is required by the ToolHandler constructor'
            self.app_man = app_man

        if not self.mount_folder_exists:
            self.create_mount_folder()

        # Get the consept logger
        self.logger = logging.getLogger('consept')

        # Initialize the path to the current script
        self.path_cur_script = None

    def run_tool(self, command, user_project_path=None) -> None:
        """
        This function runs the container corresponding to this tool with a
        specific command.
        """
        self.app_man.run_container(self.tool, command, user_project_path)

    @property
    def path_mount_folder(self) -> str:
        """
        Property of a ToolHandler, specifying the path of the folder which will be mounted onto the
        container corresponding to the tool at run-time
        """
        return os.path.join(PATH_CONSEPT, 'tmp', self.tool)

    @property
    def mount_folder_exists(self) -> bool:
        """
        Returns whether the local folder which is mounted onto the container at run-time exists
        """
        return os.path.exists(self.path_mount_folder)

    @property
    def mount_files(self) -> list:
        """
        Property of a ToolHandler, returns the contents of the folder which will be mounted onto the
        container corresponding to the tool at run-time
        """
        return os.listdir(self.path_mount_folder)

    def empty_mount_folder(self) -> None:
        """
        This function empties the folder which will be mounted onto the
        container corresponding to the tool at run-time
        """
        def handle_remove_readonly(func, path, exc):
            # Handle the permission-related error and remove read-only attribute if possible
            if isinstance(exc, PermissionError):
                os.chmod(path, stat.S_IWRITE)
                func(path)

        try:
            if os.path.exists(self.path_mount_folder):
                shutil.rmtree(self.path_mount_folder, onerror=handle_remove_readonly)

            os.mkdir(self.path_mount_folder)
        except PermissionError as exception:
            print(f"Error: {exception}. Failed to empty the mount folder.")

    def open_new_script(self) -> None:
        """
        This container creates a new bash script in the mount folder corresponding to this tool
        """

        # construct the name of the new bash script
        cur_script_name = self.tool + '_' + datetime.now().strftime('%Y%m%d%H%M') + '.sh'

        # define the path at which the new bash script will be stored
        self.path_cur_script = os.path.join(
            PATH_CONSEPT, 'tmp', self.tool, cur_script_name)

        self.logger.debug(f'Opening new script {self.path_cur_script}')

        # create bash script and write the first line
        with open(self.path_cur_script, 'w', encoding='utf8') as cur_script:
            cur_script.writelines('#!/bin/sh\n')

    def add_command(self, line: str) -> None:
        """
        Using this function, new commands can be appended to the current
        bash script of the ToolHandler
        """

        # Confirm that a bash script is available
        assert self.path_cur_script is not None, 'self.open_new_script() needs to be called \
        before any commands can be added'

        # open the bash script and append ('a') the new command to it
        with open(self.path_cur_script, 'a', encoding='utf-8') as cur_script:
            cur_script.writelines(line + '\r\n')

    def create_mount_folder(self) -> None:
        """
        Function that creates folder with path PATH_CONSEPT/tmp/self.tool
        which contains all files to be mounted onto the container corresponding to the tool.
        """
        os.makedirs(self.path_mount_folder)

    def convert_script(self) -> None:
        """
        Function that makes the scripts constructed by the toolhandler Unix-friendly.
        """
        with open(self.path_cur_script, "rb") as src:
            buffer = dos2unix(src)
        with open(self.path_cur_script, "wb") as dest:
            dest.write(buffer)

    def run(self) -> None:
        """
        This function runs a container of the image corresponding to this tool.
        In this container it runs the current script
        Arguments:
            None
        Returns:
            None
        """
        assert self.path_cur_script is not None, 'a script is required to run a container \
            in this fashion'

        self.add_command('echo Now exiting container')

        self.convert_script()

        cur_script_name = os.path.basename(self.path_cur_script)
        path_container_script = f'/home/consept/tmp/{self.tool}/{cur_script_name}'

        command = f'sh {path_container_script}'

        return self.run_tool(command)
