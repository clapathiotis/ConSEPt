#!/bin/bash
set -e
cd $EDITED_USER_PROJECT_PATH/build
cmake --build . --parallel $(nproc)
