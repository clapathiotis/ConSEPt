FROM joakimbse/dextool-ubuntu
USER root

ARG CMAKE_VERSION=3.26.4
ARG GTEST_VERSION=1.11.0
ARG USER_PROJECT_PATH
ARG EDITED_USER_PROJECT_PATH
ARG MOUNTED_MUTATION_FOLDER
ARG PARENT_FOLDER_OF_USER_PROJECT

ENV USER_PROJECT_PATH=${USER_PROJECT_PATH}
ENV EDITED_USER_PROJECT_PATH=${EDITED_USER_PROJECT_PATH}
ENV MOUNTED_MUTATION_FOLDER=${MOUNTED_MUTATION_FOLDER}
ENV PARENT_FOLDER_OF_USER_PROJECT=${PARENT_FOLDER_OF_USER_PROJECT}

# Download cmake
RUN echo "deb http://archive.ubuntu.com/ubuntu/ focal-proposed main" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y build-essential g++ clang wget && \
    rm -rf /var/lib/apt/lists/* && \
    wget https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}-Linux-x86_64.sh \
      -q -O /tmp/cmake-install.sh && \
    chmod u+x /tmp/cmake-install.sh && \
    mkdir /opt/cmake-${CMAKE_VERSION} && \
    /tmp/cmake-install.sh --skip-license --prefix=/opt/cmake-${CMAKE_VERSION} && \
    rm /tmp/cmake-install.sh && \
    ln -s /opt/cmake-${CMAKE_VERSION}/bin/* /usr/bin

# Download and build google test
RUN wget -q https://github.com/google/googletest/archive/refs/tags/release-${GTEST_VERSION}.tar.gz -O /tmp/gtest.tar.gz \
    && tar -xzf /tmp/gtest.tar.gz -C /opt \
    && rm /tmp/gtest.tar.gz \
    && mkdir -p /opt/googletest-release-${GTEST_VERSION}/build \
    && cd /opt/googletest-release-${GTEST_VERSION}/build \
    && cmake .. \
    && make \
    && make install
