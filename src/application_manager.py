"""
This module provides the application manager class.

Classes:
    - ApplicationManager(object)
"""

import os
import sys
from pathlib import Path
import logging
import docker

from utils.misc import logs_to_str

# Import all relevant consept variables
from consept_vars import FOLDER_NAME_CONCOLIC, FOLDER_NAME_FUZZ, FOLDER_NAME_MUTATION, \
    MOUNTED_MUTATION_FOLDER, NAME_IMAGE_CONCOLIC, \
    NAME_CONTAINER_CONCOLIC, NAME_CONTAINER_FUZZ, \
    NAME_CONTAINER_MUTATION, PARENT_FOLDER_OF_USER_PROJECT, \
    NAME_IMAGE_FUZZ, NAME_IMAGE_MUTATION

PATH_ABSOLUTE = str(Path(os.path.realpath(__file__)).parent)
PATH_CONSEPT = str(Path(PATH_ABSOLUTE).parent)
PATH_CONCOLIC = os.path.join(PATH_ABSOLUTE, 'tools', FOLDER_NAME_CONCOLIC)
PATH_FUZZ = os.path.join(PATH_ABSOLUTE, 'tools', FOLDER_NAME_FUZZ)
PATH_MUTATION = os.path.join(PATH_ABSOLUTE, 'tools', FOLDER_NAME_MUTATION)

logging.basicConfig(
    stream = sys.stdout,
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

class ApplicationManager():  # pylint: disable=too-few-public-methods
    """
    Class that is in charge of managing Docker images and containers for consept.
    Any automated image-building and container-running of the tools that consept
    relies on is done by the ApplicationManager.
    """

    client: docker.client

    def __init__(self, init_tools: list = None, user_project_path : str = None) -> None:
        """
        Constructor of the ApplicationManager class.
        The class has a logger attribute which

        Parameters:
        init_tools (list) : List of tools for which the Docker image should be built

        Returns:
        None
        """

        # Fetch Docker client from environment
        self.client = docker.from_env()

        # Initialize logger
        self.logger = logging.getLogger('consept')
        self.logger.setLevel(logging.INFO)

        # Initialize the images of the specified tools
        assert isinstance(init_tools, list) & (init_tools is not None), 'init_tools \
            is required to be a non-empty list'
        for tool in init_tools:
            self._build_tool_image(tool, user_project_path)

        self.logger.debug('Finished constructing ApplicationManager')

    def _build_tool_image(
            self,
            tool : str,
            user_project_path : str,
            redo : bool = False,
        ) -> None:
        """
        Builds the image for a specific tool. This tool is specified by paramater tool.
        It checks whether a Dockerfile can be found for this specific image and throw
        an AssertionError if this is not the case.

        Parameters:
        tools (str) : tool for which a Docker image will be built. Should be either 'concolic',
        'fuzz', 'mutation'.

        Returns:
        None

        Raises:
        AssertionError : tool given as output is not recognized. See parameters.
        """
        build_args = None

        # Process tool parameter
        if tool == 'concolic':
            path_folder_tool = PATH_CONCOLIC
            name_image = NAME_IMAGE_CONCOLIC
        elif tool == 'fuzz':
            path_folder_tool = PATH_FUZZ
            name_image = NAME_IMAGE_FUZZ
        elif tool == 'mutation':
            path_folder_tool = PATH_MUTATION
            name_image = NAME_IMAGE_MUTATION
            user_project_name = os.path.basename(user_project_path)
            edited_user_project_path = PARENT_FOLDER_OF_USER_PROJECT + "/" + user_project_name
            build_args = {
                "USER_PROJECT_PATH": user_project_path.replace(os.sep, '/'),
                "EDITED_USER_PROJECT_PATH": edited_user_project_path,
                "MOUNTED_MUTATION_FOLDER": MOUNTED_MUTATION_FOLDER,
                "PARENT_FOLDER_OF_USER_PROJECT": PARENT_FOLDER_OF_USER_PROJECT,
            }
        else:
            raise AssertionError(f'Toolname not recognized ({tool})')

        # Check existence of Dockerfile for this tool
        assert os.path.exists(
            path_folder_tool), f'No Dockerfile found in {path_folder_tool}'

        # Check if we are creating an image that has the same name as an existing image
        if name_image in self._available_images:
            if redo:
                self.logger.info(
                    f'Image {name_image} exists already, will build anyway')
            else:
                self.logger.info(
                    f'Image {name_image} exists already, will not build')
                return

        self.logger.info(f'Will now build image {name_image} from path \'{path_folder_tool}\'' +
                         f' for {tool}')

        # Build image
        _, build_logs = self.client.images.build(
            path=path_folder_tool,
            quiet=False,
            tag=name_image,
            buildargs=build_args,
            )

        # Log the build_logs
        self.logger.info(f'=== IMAGE BUILDING LOGS for {name_image} ===')
        self.logger.info(logs_to_str(build_logs))

    @property
    def _available_images(self) -> list:
        """
        Lists all currently available image by name

        Parameters:
        None

        Returns:
        List of available images by name

        Raises:
        None
        """

        # flatten images list
        unflattened_tags = [img.tags for img in self.client.images.list()]
        flattened_tags = sum(unflattened_tags, [])

        # return only image names, no tags
        return [tag[:-7] for tag in flattened_tags if tag[-7:] == ':latest']

    @property
    def _available_containers(self) -> list:
        """
        Lists all currently available containers by name

        Parameters:
        None

        Returns:
        List of available containers

        Raises:
        None
        """

        # return all container names
        ret_list = [
            container.name for container in self.client.containers.list(all=True)]
        return ret_list

    def run_container(self,
                      tool,
                      command,
                      user_project_path=None,
                      remove_afterwards = False,
                      ) -> None:
        """
        Run the container of a specific tool with a set of commands

        Parameters:
        tool (str) : tool on which the commands should be run
        command (str/list) : (set of) command(s) to be run inside the container
        of the specified tool

        Returns:
        None

        Raises:
        AssertionError : If the name of the tool is not recognized
        docker.errors.APIError : If an error is raised by the the Docker API
        that is used by this function.
        """

        # Process tool parameter
        if tool == 'concolic':
            name_image = NAME_IMAGE_CONCOLIC
            name_container = NAME_CONTAINER_CONCOLIC

        elif tool == 'fuzz':
            name_image = NAME_IMAGE_FUZZ
            name_container = NAME_CONTAINER_FUZZ
        elif tool == 'mutation':
            name_image = NAME_IMAGE_MUTATION
            name_container = NAME_CONTAINER_MUTATION
        else:
            raise AssertionError(f'Toolname not recognized ({tool})')

        # Make sure the image the container is based on is built
        if not name_image in self._available_images:
            self._build_tool_image(tool, user_project_path)

        if name_container in self._available_containers:
            self.client.containers.get(name_container).remove()

        # define source and target paths for the tmp folder
        path_local_tmp_tool = os.path.join(PATH_CONSEPT, 'tmp', tool)
        path_external_tmp_target = f'/home/consept/tmp/{tool}'

        # Log the source and target paths of the tmp folder
        self.logger.info(f'Will mount temporary files from source \'{path_local_tmp_tool}\' to' +
                         f' target \'{path_external_tmp_target}\'')

        # create mount object which mounts the tmp folder on the container that is about to be ran
        tmp_mount = docker.types.Mount(
            target=path_external_tmp_target,
            source=path_local_tmp_tool,
            type='bind'
        )

        project_mount = None
        if tool == 'mutation':
            source_path = os.path.abspath(user_project_path)
            self.logger.info(f'Will mount user project files from source \'{source_path}\' to ' + \
            f'target \'{user_project_path}\'')
            project_mount = docker.types.Mount(
                target=user_project_path,
                source=source_path,
                type='bind'
            )

        self.logger.info(f'Will now run container {name_container} from image {name_image}')

        # run the contiainer
        container = self.client.containers.run(
            image = f'{name_image}:latest',
            command = command,
            stdout = True,
            stderr = True,
            remove = remove_afterwards,
            detach = True,
            name = name_container,
            mounts = [tmp_mount] if tool != "mutation" else [tmp_mount, project_mount],
            tty=True,
        )

        # get output by attaching the container to the local terminal
        # accumulate output chunks into a byte string
        output_bytes = b""
        for chunk in container.attach(stdout=True, stream=True):
            output_bytes += chunk

        # log the output of the container that was just run
        self.logger.info(f'\n\n ========= START CONTAINER OUTPUT for {name_container} =========')
        try:
            self.logger.info(output_bytes.decode("utf-8"))
        except UnicodeDecodeError:
            print('cannot decode output bytes')

        self.logger.info(f'\n ========= END CONTAINER OUTPUT for {name_container} =========')

        return container, output_bytes
