#!/usr/bin/python3

import os
import pytest

try:
    from unittest import mock  # python 3.3+
except ImportError:
    import mock  # python 2.6-3.2

from unitygen import filemgr
from tests import common

def setup_function( ):
    common.setupRoot( )
def teardown_function( ):
    common.cleanupRoot( )

def createTestCModule( sourceFile, moduleName, includeFile ):
    mod = filemgr.c_module( sourceFile, [ includeFile ] )
    mod.__sourceFile__ = sourceFile
    mod.__moduleName__ = moduleName
    mod.__includeFile__ = includeFile
    return mod

sourcePath = common.createTestPath( 'src' )
includePath = common.createTestPath( 'include' )

def test_constructorNoSourcePath( ):
    common.setupPath( includePath )
    
    with pytest.raises( Exception ):
        assert filemgr.filemgr( sourcePath, includePath )
def test_constructorNoIncludePath( ):
    common.setupPath( sourcePath )
    
    with pytest.raises( Exception ):
        assert filemgr.filemgr( sourcePath, includePath )
def test_constructorNoFiles( ):
    common.setupPath( sourcePath )
    common.setupPath( includePath )

    mgr = filemgr.filemgr( sourcePath, includePath )
    assert not mgr.__modules__
    assert not mgr.__includeFiles__
def test_constructor( ):
    common.setupPath( sourcePath )
    common.setupPath( os.path.join( sourcePath, 'folder1' ) )
    common.setupPath( includePath )
    common.setupPath( os.path.join( includePath, 'folder2' ) )

    common.touchFile( os.path.join( sourcePath, 'fileA.c' ) )
    common.touchFile( os.path.join( sourcePath, 'fileB.c' ) )
    common.touchFile( os.path.join( sourcePath, 'fileC.c' ) )
    common.touchFile( os.path.join( sourcePath, 'fileF.c' ) )
    common.touchFile( os.path.join( sourcePath, 'folder1', 'fileE.c' ) )

    common.touchFile( os.path.join( includePath, 'fileA.h' ) )
    common.touchFile( os.path.join( includePath, 'fileB.h' ) )
    common.touchFile( os.path.join( includePath, 'fileD.h' ) )
    common.touchFile( os.path.join( includePath, 'fileE.h' ) )
    common.touchFile( os.path.join( includePath, 'folder2', 'fileF.h' ) )

    fileAModule = createTestCModule( 'fileA.c', 'fileA', 'fileA.h' )
    fileBModule = createTestCModule( 'fileB.c', 'fileB', 'fileB.h' )
    fileCModule = createTestCModule( 'fileC.c', 'fileC', '' )
    fileDModule = createTestCModule( 'fileD.c', 'fileD', 'fileD.h' )
    fileEModule = createTestCModule( 'folder1/fileE.c', 'fileE', 'fileE.h' )
    fileFModule = createTestCModule( 'fileF.c', 'fileF', 'folder2/fileF.h' )

    mgr = filemgr.filemgr( sourcePath, includePath )
    assert len( mgr.__modules__ ) == 5
    assert fileAModule in mgr.__modules__
    assert fileBModule in mgr.__modules__
    assert fileCModule in mgr.__modules__
    assert not fileDModule in mgr.__modules__
    assert fileEModule in mgr.__modules__
    assert fileFModule in mgr.__modules__
    
    assert len( mgr.__includeFiles__ ) == 5
    assert 'fileA.h' in mgr.__includeFiles__
    assert 'fileB.h' in mgr.__includeFiles__
    assert 'fileD.h' in mgr.__includeFiles__
    assert 'fileE.h' in mgr.__includeFiles__
    assert 'folder2/fileF.h' in mgr.__includeFiles__