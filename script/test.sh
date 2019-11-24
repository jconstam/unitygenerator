#!/bin/bash

mkdir -p test/build
mkdir -p test/unittest
python3 unityGenerator.py -s test/src -i test/include -t test/unittest
cd test/build
cmake ../unittest
make