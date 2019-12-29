#!/usr/bin/python3

import os
import pytest
import argparse

try:
    from unittest import mock  # python 3.3+
except ImportError:
    import mock  # python 2.6-3.2

from unitygen import misc

@mock.patch( 'argparse.ArgumentParser.parse_args', return_value=argparse.Namespace( sourceRoot='rootPath', includeRoot='includePath', testRoot='testPath' ) )
def test_parseArgs( mock_args ):
    args = misc.parseArgs( )

    assert args.sourceRoot == 'rootPath'
    assert args.includeRoot == 'includePath'
    assert args.testRoot == 'testPath'

def test_findFilesSinglePath( ):
    fileList = misc.findFiles( os.path.dirname( os.path.abspath( __file__ ) ), '.py' )

    assert os.path.basename( __file__ ) in fileList
def test_findFilesMultiplePaths( ):
    path = os.path.abspath( os.path.join( os.path.dirname( os.path.abspath( __file__ ) ), '..' ) )
    fileList = misc.findFiles( path, '.py' )

    assert os.path.join( os.path.basename( os.path.dirname( os.path.abspath( __file__ ) ) ), os.path.basename( __file__ ) ) in fileList
def test_findFilesInvalidPath( ):
    fileList = misc.findFiles( '/a/test/path' , '.py' )

    assert not os.path.basename( __file__ ) in fileList