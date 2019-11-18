#!/bin/bash

rm -rf output
./unityGenerator.py -s ../lazybox/src -i ../lazybox/src/include -t output

rm -rf build
mkdir -p build
cd build && cmake ../output && make