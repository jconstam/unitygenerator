#!/usr/bin/python3

import os
import pytest
import argparse

try:
    from unittest import mock  # python 3.3+
except ImportError:
    import mock  # python 2.6-3.2

from unitygen import misc
from tests import common

def setup_function( ):
    common.setupRoot( )
def teardown_function( ):
    common.cleanupRoot( )

@mock.patch( 'argparse.ArgumentParser.parse_args', return_value=argparse.Namespace( sourceRoot='rootPath', includeRoot='includePath', testRoot='testPath' ) )
def test_parseArgs( mock_args ):
    args = misc.parseArgs( )

    assert args.sourceRoot == 'rootPath'
    assert args.includeRoot == 'includePath'
    assert args.testRoot == 'testPath'

def test_findFilesSinglePath( ):
    common.touchFile( common.createTestPath( 'testFile1.x' ) )
    common.touchFile( common.createTestPath( 'testFile2.x' ) )
    common.touchFile( common.createTestPath( 'testFile3.y' ) )

    fileList = misc.findFiles( common.rootPath, '.x' )
    assert 'testFile1.x' in fileList
    assert 'testFile2.x' in fileList
    assert not 'testFile3.y' in fileList
def test_findFilesMultiplePaths( ):
    common.setupPath( common.createTestPath( 'folder1' ) )
    common.setupPath( common.createTestPath( 'folder2' ) )

    common.touchFile( common.createTestPath( 'testFile1.x' ) )
    common.touchFile( common.createTestPath( 'folder1/testFile2.x' ) )
    common.touchFile( common.createTestPath( 'folder2/testFile3.y' ) )
    
    fileList = misc.findFiles( common.rootPath, '.x' )
    assert 'testFile1.x' in fileList
    assert 'folder1/testFile2.x' in fileList
    assert not 'folder1/testFile3.y' in fileList
    assert not 'testFile3.y' in fileList
def test_findFilesInvalidPath( ):
    common.touchFile( common.createTestPath( 'testFile1.x' ) )
    common.touchFile( common.createTestPath( 'testFile2.x' ) )
    common.touchFile( common.createTestPath( 'testFile3.y' ) )

    fileList = misc.findFiles( '/a/test/path', '.x' )
    assert not 'testFile1.x' in fileList
    assert not 'testFile2.x' in fileList
    assert not 'testFile3.y' in fileList
    
def test_createTemplateFiles( capsys ):
    common.setupPath( common.createTestPath( 'folder1' ) )
    common.setupPath( common.createTestPath( 'folder2' ) )

    common.touchFile( common.createTestPath( 'template1' ) )
    common.touchFile( common.createTestPath( 'template2' ) )
    common.touchFile( common.createTestPath( 'folder2/template2' ) )

    misc.copyTemplateFile( 'template1', common.rootPath, common.createTestPath( 'folder1' ) )
    assert os.path.exists( common.createTestPath( 'folder1/template1' ) )
    captured = capsys.readouterr( )
    assert captured.out == 'Copying template file {} to {}\n'.format( common.createTestPath( 'template1' ), common.createTestPath( 'folder1/template1' ) )

    misc.copyTemplateFile( 'template2', common.rootPath, common.createTestPath( 'folder2' ) )
    assert os.path.exists( common.createTestPath( 'folder2/template2' ) )
    captured = capsys.readouterr( )
    assert captured.out == 'Template file {} already exists\n'.format( common.createTestPath( 'folder2/template2' ) )

def test_checkFileContentsSame( ):
    testString1 = 'This string is for testing!'
    testString2 = 'This string is also for testing!'

    with open( common.createTestPath( 'testFile1' ), 'w+' ) as writeFile:
        writeFile.write( testString1 )
    with open( common.createTestPath( 'testFile2' ), 'w+' ) as writeFile:
        writeFile.write( testString2 )

    assert misc.checkFileContentsSame( common.createTestPath( 'testFile1' ), testString1 )
    assert not misc.checkFileContentsSame( common.createTestPath( 'testFile2' ), testString1 )
    assert not misc.checkFileContentsSame( common.createTestPath( 'testFile3' ), testString1 )
