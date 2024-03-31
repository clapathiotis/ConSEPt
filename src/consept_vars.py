"""
This module contains all definitions consept variables.
"""
import os
from pathlib import Path

PATH_ABSOLUTE = str(Path(os.path.realpath(__file__)).parent)
PATH_CONSEPT = str(Path(PATH_ABSOLUTE).parent)

NAME_CONTAINER_CONCOLIC = 'container_consept_concolic'
NAME_IMAGE_CONCOLIC = 'image_consept_concolic'
FOLDER_NAME_CONCOLIC = 'concolic'

NAME_CONTAINER_FUZZ = 'container_consept_fuzz'
NAME_IMAGE_FUZZ = 'image_consept_fuzz'
FOLDER_NAME_FUZZ = 'fuzz'

NAME_CONTAINER_MUTATION = 'container_consept_mutation'
NAME_IMAGE_MUTATION = 'image_consept_mutation'
FOLDER_NAME_MUTATION = 'mutation'

ARR_ALLOWED_TOOLS = ['concolic', 'fuzz', 'mutation']

PARENT_FOLDER_OF_USER_PROJECT = '/editedUserProject'
MOUNTED_MUTATION_FOLDER = '/home/consept/tmp/mutation'
