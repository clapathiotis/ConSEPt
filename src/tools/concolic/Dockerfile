FROM klee/klee:latest
USER root

RUN mkdir /home/consept
RUN mkdir /home/consept/tmp
RUN mkdir /home/consept/src

RUN pip3 install clang==11
RUN pip3 install libclang==11
RUN pip3 install pytest
# To print the coverage on klee
RUN pip3 install tabulate 
    
ADD . /home/consept/src/concolic
#ADD tests /home/consept/tests

WORKDIR /home/consept
