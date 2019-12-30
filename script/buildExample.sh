#!/bin/bash

echo "====================="
echo "CLEAN UP"
echo "====================="
rm -rfv example/build
rm -rfv example/unittest
echo "====================="
echo "CREATING DIRECTORIES"
echo "====================="
mkdir -pv example/build
mkdir -pv example/unittest
echo "====================="
echo "GENERATING PROJECT"
echo "====================="
python3 unitygen.py -c example/unittest_config.json
echo "====================="
echo "RUNNING CMAKE"
echo "====================="
cd example/build
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
