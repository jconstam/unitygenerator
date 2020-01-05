#!/usr/bin/python3

import os
import json
import pytest

try:
    from unittest import mock  # python 3.3+
except ImportError:
    import mock  # python 2.6-3.2

from unitygen import config
from tests import common

__testFilePath__ = common.createTestPath( 'testFile.json' )
__testData__ = { 'paths': { 'root': 'rootPath', 'sources': [ 'sourcePath1', 'sourcePath2' ], 'includes': [ 'includePath1', 'includePath2' ], 'test': 'testPath' } }

def setup_function( ):
    common.setupRoot( )
def teardown_function( ):
    common.cleanupRoot( )

def makePath( subPaths ):
    return os.path.abspath( os.path.join( *subPaths ) )

@pytest.fixture
def testObject( ):
    with open( __testFilePath__, 'w+' ) as file:
        json.dump( __testData__, file )

    return config.configfile( __testFilePath__ )

def test_constructor( testObject ):
    assert testObject.__data__ == __testData__

def test_getters_good( testObject ):
    assert testObject.getRootPath( ) == makePath( [ 'rootPath' ] )
    assert testObject.getSourcesRoots( ) == [ makePath( [ 'rootPath', 'sourcePath1' ] ), makePath( [ 'rootPath', 'sourcePath2' ] ) ]
    assert testObject.getIncludeRoots( ) == [ makePath( [ 'rootPath', 'includePath1' ] ), makePath( [ 'rootPath', 'includePath2' ] ) ]
    assert testObject.getTestRoot( ) == makePath( [ 'rootPath', 'testPath' ] )

def test_getters_bad( testObject ):
    testObject.__data__ = { }
    
    with pytest.raises( Exception ):
        assert testObject.getRootPath( )

    testObject.__data__[ 'paths' ] = { 'root': 'rootPath' }
    
    with pytest.raises( Exception ):
        assert testObject.getSourcesRoots( )
    with pytest.raises( Exception ):
        assert testObject.getIncludeRoots( )
    with pytest.raises( Exception ):
        assert testObject.getTestRoot( )
