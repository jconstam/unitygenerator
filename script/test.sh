#!/bin/bash

echo "====================="
echo "CLEAN UP"
echo "====================="
rm -rfv test/build
rm -rfv test/unittest
echo "====================="
echo "CREATING DIRECTORIES"
echo "====================="
mkdir -pv test/build
mkdir -pv test/unittest
echo "====================="
echo "GENERATING PROJECT"
echo "====================="
python3 unityGenerator.py -s test/src -i test/include -t test/unittest
echo "====================="
echo "RUNNING CMAKE"
echo "====================="
cd test/build
cmake ../unittest
echo "====================="
echo "BUILDING"
echo "====================="
make
echo "====================="
echo "TESTING"
echo "====================="
ctest
echo "====================="
echo "DONE"
echo "====================="
