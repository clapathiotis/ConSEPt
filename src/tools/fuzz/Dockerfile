FROM ubuntu:18.04
USER root

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install sudo
RUN sudo apt-get --yes install git
RUN git clone https://github.com/google/fuzzing.git fuzzing

RUN ./fuzzing/tutorial/libFuzzer/install-deps.sh  
RUN ./fuzzing/tutorial/libFuzzer/install-clang.sh 

RUN mkdir /home/consept
RUN mkdir /home/consept/tmp
RUN mkdir /home/consept/src

ADD . /home/consept/src/fuzz

WORKDIR /home/consept