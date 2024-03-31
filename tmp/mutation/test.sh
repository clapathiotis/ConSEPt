#!/bin/bash
# make check

set -e
cd $EDITED_USER_PROJECT_PATH/build
ctest --output-on-failure

