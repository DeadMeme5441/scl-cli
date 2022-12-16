# scl-cli

This repository was created to move the basic building blocks of SCL - Sanskrit Computational Linguistic Tools, and make it into a dockerized REST API.

This was to improve accessibility and build on top of it. The steps involved were:
1. Understand .lex and .yacc file interactions and compilability.
2. Understand perl file interactions with inputs and streamline it.
3. Build a Python logic layer to link everything and make it accessible.
4. Build a NodeJS server layer that queries the python layer and returns outputs after taking inputs.

This project took me a week to complete. Any contributions to improve features are welcome.

The original repository for scl can be found at
https://github.com/ambaji57/scl_2018 by Amba Kulkarni. The entire project of
SCL-CLI was to make the tools within SCL accessible to a CLI environment, and
the implementation might be seemingly convoluted, but is very straight forward
when understood from a requirements perspective. The binaries are executed with
a single word input, and generate an output written to STDOUT. These scripts are
executed by a nodejs layer as a server layer, so bulk and parallel execution can
be enabled. After these API's are made available, a python script was written to
make the bulk processing of inputs possible, for each type of operation - Morph,
Convert etc.

The server is dockerized so deployment is just one execution of the docker run
statement and the python scripts can be utilized to query the server for bulk
processing of the words as required.
