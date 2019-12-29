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

def setupTestFiles( ):
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

    modules = [ ]
    modules.append( createTestCModule( 'fileA.c', 'fileA', 'fileA.h' ) )
    modules.append( createTestCModule( 'fileB.c', 'fileB', 'fileB.h' ) )
    modules.append( createTestCModule( 'fileC.c', 'fileC', '' ) )
    modules.append( createTestCModule( 'folder1/fileE.c', 'fileE', 'fileE.h' ) )
    modules.append( createTestCModule( 'fileF.c', 'fileF', 'folder2/fileF.h' ) )
    includeFiles = [ ]
    includeFiles.append( 'fileA.h' )
    includeFiles.append( 'fileB.h' )
    includeFiles.append( 'fileD.h' )
    includeFiles.append( 'fileE.h' )
    includeFiles.append( 'folder2/fileF.h' )

    return [ modules, includeFiles ]
    
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
    [ testModules, includeFiles ] = setupTestFiles( )

    mgr = filemgr.filemgr( sourcePath, includePath )
    assert len( mgr.__modules__ ) == len( testModules )
    for mod in testModules:
        assert mod in mgr.__modules__
    
    assert len( mgr.__includeFiles__ ) == len( includeFiles )
    for file in includeFiles:
        assert file in mgr.__includeFiles__

def test_createTestStubs( ):
    testRootPath = common.createTestPath( 'testRoot' )
    [ testModules, includeFiles ] = setupTestFiles( )

    mgr = filemgr.filemgr( sourcePath, includePath )
    mgr.createTestStubs( testRootPath )

    for mod in testModules:
        assert os.path.exists( mod.testStubPath( testRootPath ) )
def test_createTestStubsPathExists( ):
    testRootPath = common.createTestPath( 'testRoot' )
    common.setupPath( testRootPath )
    [ testModules, includeFiles ] = setupTestFiles( )
    for mod in testModules:
        os.makedirs( os.path.dirname( mod.testStubPath( testRootPath ) ) )

    mgr = filemgr.filemgr( sourcePath, includePath )
    mgr.createTestStubs( testRootPath )

    for mod in testModules:
        assert os.path.exists( mod.testStubPath( testRootPath ) )
def test_createTestStubsFileExists( ):
    testRootPath = common.createTestPath( 'testRoot' )
    common.setupPath( testRootPath )
    [ testModules, includeFiles ] = setupTestFiles( )
    for mod in testModules:
        os.makedirs( os.path.dirname( mod.testStubPath( testRootPath ) ) )
        common.touchFile( mod.testStubPath( testRootPath ) )

    mgr = filemgr.filemgr( sourcePath, includePath )
    mgr.createTestStubs( testRootPath )

    for mod in testModules:
        assert os.path.exists( mod.testStubPath( testRootPath ) )

def test_createTestCMakeList( ):
    testRootPath = common.createTestPath( 'testRoot' )
    common.setupPath( testRootPath )
    [ testModules, includeFiles ] = setupTestFiles( )

    mgr = filemgr.filemgr( sourcePath, includePath )
    mgr.createTestCMakeList( testRootPath, sourcePath, includePath )

    assert os.path.exists( os.path.join( testRootPath, 'CMakeLists.txt' ) )
    
    mgr.createTestCMakeList( testRootPath, sourcePath, includePath )

    assert os.path.exists( os.path.join( testRootPath, 'CMakeLists.txt' ) )
