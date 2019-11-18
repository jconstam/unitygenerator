#!/usr/bin/python3

import os
import sys
import shutil
import hashlib

from pathlib import Path
from argparse import ArgumentParser

def collectArguments( ):
    parser = ArgumentParser( 'Unity Test Skeleton Generator', add_help=True )
    parser.add_argument( '-s', '--sourceRoot', type=str, required=True, help='Path where the source files are located' )
    parser.add_argument( '-i', '--includeRoot', type=str, required=True, help='Path where the include files are located' )
    parser.add_argument( '-t', '--testRoot', type=str, required=True, help='Path where the test files are to be output' )
    return parser.parse_args( )

def findFiles( root, extension ):
    fileList = [ ]
    for path, subdirs, files in os.walk( root ):
        for x in files:
            if x.endswith( extension ):
                relPath = path.replace( root, '' )
                if relPath.startswith( '/' ):
                    relPath = relPath[ 1: ]
                fileList.append( os.path.join( relPath, x ) )
    return fileList 
def findSourceFiles( sourceRoot ):
    return findFiles( sourceRoot, '.c' )
def findHeaderFiles( includeRoot ):
    return findFiles( includeRoot, '.h' )
def copyTemplateFile( fileName, templatesPath, destPath ):
    templateFilePath = os.path.join( templatesPath, fileName )
    destFilePath = os.path.join( destPath, fileName )
    if os.path.exists( destFilePath ):
        print( 'Template file {} already exists'.format( destFilePath ) )
    else:
        print( 'Copying template file {} to {}'.format( templateFilePath, destFilePath ) )
        shutil.copy2( templateFilePath, destFilePath )

def checkFileContentsSame( filePath, contents ):
    contentsMD5 = hashlib.md5( contents.encode( ) )

    fileMD5 = hashlib.md5( )
    if os.path.exists( filePath ):
        with open( filePath, 'rb' ) as inFile:
            for chunk in iter( lambda: inFile.read( 4096 ), b'' ):
                fileMD5.update( chunk )

    return contentsMD5.hexdigest( ) == fileMD5.hexdigest( )

def generateTestStub( sourceFilePath, sourceFile, includeFiles ):
    testFilePath = sourceFilePath.replace( '.c', '_tests.c' )
    testFile = os.path.basename( testFilePath )
    includeFile = os.path.basename( sourceFilePath ).replace( '.c', '.h' )
    testName = testFile.replace( '.c', '' )
    testFunction = 'runAll_{}'.format( testName )

    if os.path.exists( testFilePath ):
        print( 'Test file {} for source file {} already exists'.format( sourceFilePath, sourceFile ) )
    else:
        print( 'Generating test file {} for source file {}'.format( sourceFilePath, sourceFile ) )

        with open( testFilePath, 'w' ) as outFile:
            outFile.write( '/*\n' )
            outFile.write( ' * =======================\n' )
            outFile.write( ' * @file {}\n'.format( os.path.basename( sourceFilePath ) ) )
            outFile.write( ' * @brief Unit test file for source file {}\n'.format( sourceFile ) )
            outFile.write( ' * =======================\n' )
            outFile.write( ' */\n' )
            outFile.write( '\n' )
            outFile.write( '// ===== INCLUDES =====\n' )
            outFile.write( '#include <stdbool.h>\n' )
            outFile.write( '\n' )
            outFile.write( '#include "unity.h"\n' )
            if includeFile in includeFiles:
                outFile.write( '#include "{}"\n'.format( includeFile ) )
            else:
                outFile.write( '// Include the header file associated with the C file being tested here.\n' )
            outFile.write( '\n' )
            outFile.write( '// ===== PRE-PROCESSOR DEFINES =====\n' )
            outFile.write( '\n' )
            outFile.write( '// ===== STRUCTS ENUMS AND TYPEDEFS =====\n' )
            outFile.write( '\n' )
            outFile.write( '// ===== FILE GLOBAL VARIABLES =====\n' )
            outFile.write( '\n' )
            outFile.write( '// ===== STATIC FUNCTION DECLARATIONS =====\n' )
            outFile.write( '\n' )
            outFile.write( '// ===== UNIT TEST MANAGEMENT FUNCTIONS =====\n' )
            outFile.write( '// @brief Initialize unit tests for {}\n'.format( testFile ) )
            outFile.write( '// Runs before every test function.\n' )
            outFile.write( 'void setUp( void )\n' )
            outFile.write( '{\n' )
            outFile.write( '    \n' )
            outFile.write( '}\n' )
            outFile.write( '\n' )
            outFile.write( '// @brief Finalize unit tests for {}\n'.format( testFile ) )
            outFile.write( '// Runs after every test function.\n' )
            outFile.write( 'void tearDown( void )\n' )
            outFile.write( '{\n' )
            outFile.write( '    \n' )
            outFile.write( '}\n' )
            outFile.write( '\n' )
            outFile.write( '// ===== TEST FUNCTIONS =====\n' )
            outFile.write( '// @brief Dummy unit test for {}\n'.format( testFile ) )
            outFile.write( 'static void test_{}Compiles( void )\n'.format( testName ) )
            outFile.write( '{\n' )
            outFile.write( '    TEST_ASSERT_TRUE( true );\n' )
            outFile.write( '}\n' )
            outFile.write( '\n' )
            outFile.write( '// Add new test functions here.  Each function\'s name should start with "test_".\n' )
            outFile.write( '\n' )
            outFile.write( '// ===== TEST MAIN =====\n' )
            outFile.write( '// @brief Run all unit tests for {}\n'.format( testFile ) )
            outFile.write( '// Runs after every test function.\n' )
            outFile.write( 'void {}( void )\n'.format( testFunction ) )
            outFile.write( '{\n' )
            outFile.write( '    RUN_TEST( test_{}Compiles );\n'.format( testName ) )
            outFile.write( '    // Call other test functions here by passing the test function into the RUN_TEST macro.\n' )
            outFile.write( '}\n' )
            outFile.write( '\n' )
            outFile.write( '// ===== END OF FILE =====\n' )
            outFile.write( '\n' )
    return [ testFilePath, testName, testFunction ]
def createTestStubs( testRootPath, sourceFiles, includeFiles ):
    if not os.path.exists( testRootPath ):
        os.makedirs( testRootPath )
    testData = { }
    for sourceFile in sourceFiles:
        sourceFilePath = os.path.join( testRootPath, sourceFile )
        if not os.path.exists( os.path.dirname( sourceFilePath ) ):
            os.makedirs( os.path.dirname( sourceFilePath ) )
        [ testFilePath, testName, testFunc ] = generateTestStub( sourceFilePath, sourceFile, includeFiles )
        testData[ testName ] = { 'testFile': testFilePath, 'sourceFile': sourceFile, 'testFunc': testFunc }
    return testData

def createMains( testRootPath, testData ):
    for testName in testData:
        mainFilePath = os.path.join( testRootPath, 'main_{}.c'.format( testName ) )
        testData[ testName ][ 'mainFile' ] = mainFilePath

        output = ''
        output += '/*\n'
        output += ' * =======================\n'
        output += ' * @file {}\n'.format( os.path.basename( mainFilePath ) )
        output += ' * @brief Unit test main for {}\n'.format( testName )
        output += ' * =======================\n'
        output += ' */\n'
        output += '\n'
        output += '#include "unity.h"\n'
        output += '\n'
        output += 'extern void {}( void );\n'.format( testData[ testName ][ 'testFunc' ] )
        output += '\n'
        output += 'int main( void )\n'
        output += '{\n'
        output += '\tUNITY_BEGIN( );\n'
        output += '\tif( TEST_PROTECT( ) )\n'
        output += '\t{\n'
        output += '\t\t{}( );\n'.format( testData[ testName ][ 'testFunc' ] )
        output += '\t}\n'
        output += '\t\n'
        output += '\treturn UNITY_END( );\n'
        output += '}\n'
    
        if checkFileContentsSame( mainFilePath, output ):
            print( 'Main file {} has not changed'.format( mainFilePath ) )
        else:
            print( 'Main file {} has changed and is being generated'.format( mainFilePath ) )
            with open( mainFilePath, 'w' ) as outFile:
                outFile.write( output )

def createTestCMakeList( testRootPath, sourceRootPath, sourceFiles, testData, includeRootPath ):
    filePath = os.path.join( testRootPath, 'CMakeLists.txt' )

    output = ''
    output += '# File {} automatically generated\n'.format( filePath )
    output += '# ==========================================\n'
    output += '# CMake Setup\n'
    output += 'enable_testing( )\n'
    output += 'cmake_minimum_required( VERSION 3.5 )\n'
    output += 'set( CMAKE_CXX_STANDARD 17 )\n'
    output += '\n'
    output += '# ==========================================\n'
    output += '# Download and unpack unity at configure time\n'
    output += 'configure_file( CMakeLists.txt.in unity-download/CMakeLists.txt )\n'
    output += 'execute_process( COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" . RESULT_VARIABLE result WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/unity-download )\n'
    output += 'if( result )\n'
    output += '\tmessage( FATAL_ERROR "CMake step for unity failed: ${result}" )\n'
    output += 'endif()\n'
    output += 'execute_process( COMMAND ${CMAKE_COMMAND} --build . RESULT_VARIABLE result WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/unity-download )\n'
    output += 'if(result)\n'
    output += '\tmessage( FATAL_ERROR "Build step for unity failed: ${result}" )\n'
    output += 'endif()\n'
    output += '# ==========================================\n'
    output += '# Compile flags\n'
    output += 'set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-arcs -ftest-coverage -fno-inline -O0" )\n'
    for testName in testData:
        testFilePath = testData[ testName ][ 'testFile' ]
        mainFilePath = testData[ testName ][ 'mainFile' ]
        sourceFilePath = os.path.join( sourceRootPath, testData[ testName ][ 'sourceFile' ] )
        projectName = 'unittests_unity_c_{}'.format( testName.lower( ) )

        output += '# ==========================================\n'
        output += '# Setup project for {}\n'.format( testName )
        output += 'include_directories( {}\n'.format( projectName )
        output += '\t${CMAKE_CURRENT_BINARY_DIR}/unity-src/src\n'
        output += '\t{}\n'.format( includeRootPath )
        output += ')\n'
        output += '# Source files\n'
        output += 'add_executable( {}\n'.format( projectName )
        output += '\t${CMAKE_CURRENT_BINARY_DIR}/unity-src/src/unity.c\n'
        output += '\n'
        output += '\t{}\n'.format( sourceFilePath )
        output += '\n'
        output += '\t{}\n'.format( testFilePath )
        output += '\t{}\n'.format( mainFilePath )
        output += ')\n'
        output += 'add_test( {}\n'.format( projectName )
        output += '\tbash {}/runUnityTest.sh\n'.format( testRootPath )
        output += '\t{}\n'.format( projectName )
        output += '\t${CMAKE_CURRENT_BINARY_DIR}\n'
        output += ')\n'
        output += '\n'
    output += '# ==========================================\n'
    output += '\n'
    
    if checkFileContentsSame( filePath, output ):
        print( 'CMakeLists file {} has not changed'.format( filePath ) )
    else:
        print( 'CMakeLists file {} has changed and is being generated'.format( filePath ) )
        with open( filePath, 'w' ) as outFile:
            outFile.write( output )

if __name__ == "__main__":
    args = collectArguments( )

    basePath = os.path.dirname( sys.argv[ 0 ] )
    templatesPath = os.path.join( basePath, 'templates' )

    sourceRootPath = os.path.abspath( args.sourceRoot )
    includeRootPath = os.path.abspath( args.includeRoot )
    testRootPath = os.path.abspath( args.testRoot )

    sourceFiles = findSourceFiles( sourceRootPath )
    includeFiles = findHeaderFiles( includeRootPath )

    testData = createTestStubs( testRootPath, sourceFiles, includeFiles )
    createMains( testRootPath, testData )
    createTestCMakeList( testRootPath, sourceRootPath, sourceFiles, testData, includeRootPath )

    copyTemplateFile( 'CMakeLists.txt.in', templatesPath, testRootPath )
    copyTemplateFile( 'runUnityTest.sh', templatesPath, testRootPath )