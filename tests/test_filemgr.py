#!/usr/bin/python3

import os
import pytest

try:
    from unittest import mock  # python 3.3+
except ImportError:
    import mock  # python 2.6-3.2

from unitygen import filemgr
from tests import common

__sourcePath1__ = common.createTestPath( 'src1' )
__sourcePath2__ = common.createTestPath( 'src2' )
__includePath1__ = common.createTestPath( 'include1' )
__includePath2__ = common.createTestPath( 'include2' )

def setup_function( ):
    common.setupRoot( )
def teardown_function( ):
    common.cleanupRoot( )

def __setupTestFiles__( ):
    common.setupPath( __sourcePath1__ )
    common.setupPath( __sourcePath2__ )
    common.setupPath( os.path.join( __sourcePath1__, 'folder1' ) )
    common.setupPath( __includePath1__ )
    common.setupPath( __includePath2__ )
    common.setupPath( os.path.join( __includePath1__, 'folder2' ) )

    common.touchFile( os.path.join( __sourcePath1__, 'fileA.c' ) )
    common.touchFile( os.path.join( __sourcePath1__, 'fileB.c' ) )
    common.touchFile( os.path.join( __sourcePath1__, 'fileC.c' ) )
    common.touchFile( os.path.join( __sourcePath1__, 'fileF.c' ) )
    common.touchFile( os.path.join( __sourcePath2__, 'fileG.c' ) )
    common.touchFile( os.path.join( __sourcePath1__, 'folder1', 'fileE.c' ) )

    common.touchFile( os.path.join( __includePath1__, 'fileA.h' ) )
    common.touchFile( os.path.join( __includePath1__, 'fileB.h' ) )
    common.touchFile( os.path.join( __includePath1__, 'fileD.h' ) )
    common.touchFile( os.path.join( __includePath1__, 'fileE.h' ) )
    common.touchFile( os.path.join( __includePath2__, 'fileG.h' ) )
    common.touchFile( os.path.join( __includePath1__, 'folder2', 'fileF.h' ) )

    modules = [ ]
    modules.append( __createTestCModule__( os.path.join( __sourcePath1__, 'fileA.c' ), 'fileA', os.path.join( __includePath1__, 'fileA.h' ) ) )
    modules.append( __createTestCModule__( os.path.join( __sourcePath1__, 'fileB.c' ), 'fileB', os.path.join( __includePath1__, 'fileB.h' ) ) )
    modules.append( __createTestCModule__( os.path.join( __sourcePath1__, 'fileC.c' ), 'fileC', '' ) )
    modules.append( __createTestCModule__( os.path.join( __sourcePath1__, 'folder1/fileE.c' ), 'fileE', os.path.join( __includePath1__, 'fileE.h' ) ) )
    modules.append( __createTestCModule__( os.path.join( __sourcePath1__, 'fileF.c' ), 'fileF', os.path.join( __includePath1__, 'folder2/fileF.h' ) ) )
    modules.append( __createTestCModule__( os.path.join( __sourcePath2__, 'fileG.c' ), 'fileG', os.path.join( __includePath2__, 'fileG.h' ) ) )
    includeFiles = [ ]
    includeFiles.append( os.path.join( __includePath1__, 'fileA.h' ) )
    includeFiles.append( os.path.join( __includePath1__, 'fileB.h' ) )
    includeFiles.append( os.path.join( __includePath1__, 'fileD.h' ) )
    includeFiles.append( os.path.join( __includePath1__, 'fileE.h' ) )
    includeFiles.append( os.path.join( __includePath2__, 'fileG.h' ) )
    includeFiles.append( os.path.join( __includePath1__, 'folder2/fileF.h' ) )

    return [ modules, includeFiles ]
    
def __createTestCModule__( sourceFile, moduleName, includeFile ):
    mod = filemgr.c_module( sourceFile, [ includeFile ] )
    mod.__sourceFile__ = sourceFile
    mod.__moduleName__ = moduleName
    mod.__includeFile__ = includeFile
    return mod

def test_constructorNoSourcePath( ):
    common.setupPath( __includePath1__ )
    common.setupPath( __includePath2__ )
    
    with pytest.raises( Exception ):
        assert filemgr.filemgr( [ __sourcePath1__, __sourcePath2__ ], [ __includePath1__, __includePath2__ ] )
def test_constructorNoIncludePath( ):
    common.setupPath( __sourcePath1__ )
    common.setupPath( __sourcePath2__ )
    
    with pytest.raises( Exception ):
        assert filemgr.filemgr( [ __sourcePath1__, __sourcePath2__ ], [ __includePath1__, __includePath2__ ] )
def test_constructorNoFiles( ):
    common.setupPath( __sourcePath1__ )
    common.setupPath( __sourcePath2__ )
    common.setupPath( __includePath1__ )
    common.setupPath( __includePath2__ )

    mgr = filemgr.filemgr( [ __sourcePath1__, __sourcePath2__ ], [ __includePath1__, __includePath2__ ] )
    assert not mgr.__modules__
    assert not mgr.__includeFiles__
def test_constructor( ):
    [ testModules, includeFiles ] = __setupTestFiles__( )

    mgr = filemgr.filemgr( [ __sourcePath1__, __sourcePath2__ ], [ __includePath1__, __includePath2__ ] )
    assert len( mgr.__modules__ ) == len( testModules )
    for mod in testModules:
        assert mod in mgr.__modules__  
        print( mod ) 
    
    assert len( mgr.__includeFiles__ ) == len( includeFiles )
    for file in includeFiles:
        assert file in mgr.__includeFiles__

def test_createTestStubs( ):
    testRootPath = common.createTestPath( 'testRoot' )
    [ testModules, includeFiles ] = __setupTestFiles__( )

    mgr = filemgr.filemgr( [ __sourcePath1__, __sourcePath2__ ], [ __includePath1__, __includePath2__ ] )
    mgr.createTestStubs( testRootPath )

    for mod in testModules:
        assert os.path.exists( mod.testStubPath( testRootPath ) )
def test_createTestStubsPathExists( ):
    testRootPath = common.createTestPath( 'testRoot' )
    common.setupPath( testRootPath )
    [ testModules, includeFiles ] = __setupTestFiles__( )
    for mod in testModules:
        os.makedirs( os.path.dirname( mod.testStubPath( testRootPath ) ) )

    mgr = filemgr.filemgr( [ __sourcePath1__, __sourcePath2__ ], [ __includePath1__, __includePath2__ ] )
    mgr.createTestStubs( testRootPath )

    for mod in testModules:
        assert os.path.exists( mod.testStubPath( testRootPath ) )
def test_createTestStubsFileExists( ):
    testRootPath = common.createTestPath( 'testRoot' )
    common.setupPath( testRootPath )
    [ testModules, includeFiles ] = __setupTestFiles__( )
    for mod in testModules:
        os.makedirs( os.path.dirname( mod.testStubPath( testRootPath ) ) )
        common.touchFile( mod.testStubPath( testRootPath ) )

    mgr = filemgr.filemgr( [ __sourcePath1__, __sourcePath2__ ], [ __includePath1__, __includePath2__ ] )
    mgr.createTestStubs( testRootPath )

    for mod in testModules:
        assert os.path.exists( mod.testStubPath( testRootPath ) )

def test_createTestCMakeList( ):
    testRootPath = common.createTestPath( 'testRoot' )
    common.setupPath( testRootPath )
    [ testModules, includeFiles ] = __setupTestFiles__( )

    mgr = filemgr.filemgr( [ __sourcePath1__, __sourcePath2__ ], [ __includePath1__, __includePath2__ ] )
    mgr.createTestCMakeList( testRootPath )

    assert os.path.exists( os.path.join( testRootPath, 'CMakeLists.txt' ) )
    
    mgr.createTestCMakeList( testRootPath )

    assert os.path.exists( os.path.join( testRootPath, 'CMakeLists.txt' ) )
