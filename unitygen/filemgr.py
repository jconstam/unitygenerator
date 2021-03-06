#!/usr/bin/python

import os

from unitygen import misc

class c_module:
    def __init__( self, sourceFile, includeFiles ):
        self.__sourceFile__ = sourceFile
        self.__moduleName__ = os.path.basename( os.path.splitext( sourceFile )[ 0 ] )
        self.__includeFile__ = ''
        for file in includeFiles:
            if file.endswith( '{}.h'.format( self.__moduleName__ ) ):
                self.__includeFile__ = file
    
    def __eq__( self, obj ):
        try:
            assert self.__sourceFile__ == obj.__sourceFile__
            assert self.__moduleName__ == obj.__moduleName__
            assert self.__includeFile__ == obj.__includeFile__
            return True
        except:
            return False

    def __str__( self ):
        return '{}: {} - {}'.format( self.__moduleName__, self.__sourceFile__, self.__includeFile__ )

    def getSourceFile( self ):
        return self.__sourceFile__
    def getIncludeFile( self ):
        return self.__includeFile__
    def getModuleName( self ):
        return self.__moduleName__

    def testStubPath( self, testRootPath ):
        return os.path.join( testRootPath, os.path.basename( self.__sourceFile__ ).replace( '.c', '' ), os.path.basename( self.__sourceFile__ ) ).replace( '.c', '_tests.c' )
    def dummyTestFuncName( self ):
        return 'test_{}_compiles'.format( self.__moduleName__ )
    def projectName( self ):
        return 'unittests_unity_c_{}'.format( self.__moduleName__ )

    def hasAMock( self ):
        return not self.__includeFile__ == ''
    def mockFileName( self ):
        if self.hasAMock( ):
            return 'Mock{}'.format( os.path.basename( self.__sourceFile__ ) )
        else:
            return ''

class filemgr:
    def __init__( self, sources, includes ):
        self.__includeRoots__ = includes
        self.__sourceRoots__ = sources
        self.__includeFiles__ = [ ]
        for includePath in includes:
            includePathAbs = os.path.abspath( includePath )
            assert os.path.exists( includePathAbs )
            includeFiles = misc.findFiles( includePathAbs, '.h' )
            for includeFile in includeFiles:
                self.__includeFiles__.append( os.path.join( includePath, includeFile ) )

        self.__modules__ = [ ]
        for sourcePath in sources:
            sourcePathAbs = os.path.abspath( sourcePath )
            assert os.path.exists( sourcePathAbs )
            sourceFiles = misc.findFiles( sourcePathAbs, '.c' )
            for file in sourceFiles:
                self.__modules__.append( c_module( os.path.join( sourcePathAbs, file ), self.__includeFiles__ ) )

    def createTestStubs( self, testRootPath ):
        if not os.path.exists( testRootPath ):
            os.makedirs( testRootPath )
        for mod in self.__modules__:
            self.__generateTestStub__( mod, testRootPath )

            
    def __generateTestStub__( self, mod, testRootPath ):
        testStubPath = mod.testStubPath( testRootPath )
        testStubFolder = os.path.dirname( testStubPath )
        testStubFile = os.path.basename( testStubPath )
        if not os.path.exists( testStubFolder ):
            os.makedirs( testStubFolder )

        if os.path.exists( testStubPath ):
            print( 'Test file {} for source file {} already exists'.format( testStubPath, mod.getSourceFile( ) ) )
        else:
            print( 'Generating test stub {} for source file {}'.format( testStubPath, mod.getSourceFile( ) ) )
            with open( testStubPath, 'w' ) as outFile:
                outFile.write( '/*\n' )
                outFile.write( ' * =======================\n' )
                outFile.write( ' * @file {}\n'.format( testStubFile ) )
                outFile.write( ' * @brief Unit test file for source file {}\n'.format( mod.getSourceFile( ) ) )
                outFile.write( ' * =======================\n' )
                outFile.write( ' */\n' )
                outFile.write( '\n' )
                outFile.write( '// ===== INCLUDES =====\n' )
                outFile.write( '#include <stdbool.h>\n' )
                outFile.write( '\n' )
                outFile.write( '#include "unity.h"\n' )
                outFile.write( '#include "cmock.h"\n' )
                if mod.getIncludeFile( ):
                    outFile.write( '#include "{}"\n'.format( mod.getIncludeFile( ) ) )
                outFile.write( '// Include any header files associated with this C file here (if any).\n' )
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
                outFile.write( '// @brief Initialize unit tests for {}\n'.format( testStubFile ) )
                outFile.write( '// Runs before every test function.\n' )
                outFile.write( 'void setUp( void )\n' )
                outFile.write( '{\n' )
                outFile.write( '    // Put any setup code here\n' )
                outFile.write( '}\n' )
                outFile.write( '\n' )
                outFile.write( '// @brief Finalize unit tests for {}\n'.format( testStubFile ) )
                outFile.write( '// Runs after every test function.\n' )
                outFile.write( 'void tearDown( void )\n' )
                outFile.write( '{\n' )
                outFile.write( '    // Put any teardown code here\n' )
                outFile.write( '}\n' )
                outFile.write( '\n' )
                outFile.write( '// ===== TEST FUNCTIONS =====\n' )
                outFile.write( '// @brief Dummy unit test for {}\n'.format( testStubFile ) )
                outFile.write( 'static void {}( void )\n'.format( mod.dummyTestFuncName( ) ) )
                outFile.write( '{\n' )
                outFile.write( '    TEST_ASSERT_TRUE( true );\n' )
                outFile.write( '}\n' )
                outFile.write( '\n' )
                outFile.write( '// Add new test functions here.  Each function\'s name should start with "test_".\n' )
                outFile.write( '\n' )
                outFile.write( '// ===== TEST MAIN =====\n' )
                outFile.write( '// @brief Run all unit tests for {}\n'.format( testStubFile ) )
                outFile.write( 'int main( void )\n' )
                outFile.write( '{\n' )
                outFile.write( '    UNITY_BEGIN( );\n' )
                outFile.write( '    if( TEST_PROTECT( ) )\n' )
                outFile.write( '    {\n' )
                outFile.write( '        RUN_TEST( {} );\n'.format( mod.dummyTestFuncName( ) ) )
                outFile.write( '        // Call other test functions here by passing the test function into the RUN_TEST macro.\n' )
                outFile.write( '    }\n' )
                outFile.write( '    \n' )
                outFile.write( '    return UNITY_END( );\n' )
                outFile.write( '}\n' )
                outFile.write( '// ===== END OF FILE =====\n' )
                outFile.write( '\n' )
      
    def createTestCMakeList( self, testRootPath ):
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
        output += 'configure_file( CMakeLists_unity.txt.in unity-download/CMakeLists.txt )\n'
        output += 'execute_process( COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" . RESULT_VARIABLE result WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/unity-download )\n'
        output += 'if( result )\n'
        output += '\tmessage( FATAL_ERROR "CMake step for unity failed: ${result}" )\n'
        output += 'endif()\n'
        output += 'execute_process( COMMAND ${CMAKE_COMMAND} --build . RESULT_VARIABLE result WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/unity-download )\n'
        output += 'if(result)\n'
        output += '\tmessage( FATAL_ERROR "Build step for unity failed: ${result}" )\n'
        output += 'endif()\n'
        output += '# ==========================================\n'
        output += '# Download and unpack cmock at configure time\n'
        output += 'configure_file( CMakeLists_cmock.txt.in cmock-download/CMakeLists.txt )\n'
        output += 'execute_process( COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" . RESULT_VARIABLE result WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/cmock-download )\n'
        output += 'if( result )\n'
        output += '\tmessage( FATAL_ERROR "CMake step for cmock failed: ${result}" )\n'
        output += 'endif()\n'
        output += 'execute_process( COMMAND ${CMAKE_COMMAND} --build . RESULT_VARIABLE result WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/cmock-download )\n'
        output += 'if(result)\n'
        output += '\tmessage( FATAL_ERROR "Build step for cmock failed: ${result}" )\n'
        output += 'endif()\n'
        output += 'execute_process( COMMAND bundle install WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/cmock-src )\n'
        for includeRoot in self.__includeRoots__:
            output += 'execute_process( COMMAND bash generateCMocks.sh ${{CMAKE_CURRENT_BINARY_DIR}}/cmock-src/lib/cmock.rb {}/unittest.yml {} WORKING_DIRECTORY {} )\n'.format( 
                testRootPath, includeRoot, testRootPath )
        output += '# ==========================================\n'
        output += '# Compile flags\n'
        output += 'set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-arcs -ftest-coverage -fno-inline -O0" )\n'

        mockRoot = os.path.join( testRootPath, 'mocks' )
        mockFiles = [ ]
        includePaths = [ '${CMAKE_CURRENT_BINARY_DIR}/unity-src/src', '${CMAKE_CURRENT_BINARY_DIR}/cmock-src/src', mockRoot ]
        for includeRoot in self.__includeRoots__:
            includePaths.append( includeRoot )
        includePaths = list( dict.fromkeys( includePaths ) )
        for file in self.__includeFiles__:
            mockFiles.append( os.path.join( mockRoot, 'Mock{}'.format( os.path.basename( file ).replace( '.h', '.c' ) ) ) )
            if not os.path.dirname( file ) in includePaths:
                includePaths.append( os.path.dirname( file ) )

        for mod in self.__modules__:
            output += '# ==========================================\n'
            output += '# Setup project for {}\n'.format( mod.getModuleName( ) )
            output += 'include_directories( {}\n'.format( mod.projectName( ) )
            for path in includePaths:
                output += '\t{}\n'.format( path )
            output += ')\n'
            output += '# Source files\n'
            output += 'add_executable( {}\n'.format( mod.projectName( ) )
            output += '\t${CMAKE_CURRENT_BINARY_DIR}/unity-src/src/unity.c\n'
            output += '\t${CMAKE_CURRENT_BINARY_DIR}/cmock-src/src/cmock.c\n'
            for file in mockFiles:
                if not os.path.basename( file ) == mod.mockFileName( ):
                    output += '\t{}\n'.format( os.path.join( testRootPath, 'mocks', file ) )
            output += '\n'
            output += '\t{}\n'.format( mod.getSourceFile( ) )
            output += '\t{}\n'.format( mod.testStubPath( testRootPath ) )
            output += ')\n'
            output += 'add_test( {}\n'.format( mod.projectName( ) )
            output += '\tbash {}/runUnityTest.sh\n'.format( testRootPath )
            output += '\t{}\n'.format( mod.projectName( ) )
            output += '\t${CMAKE_CURRENT_BINARY_DIR}\n'
            output += ')\n'
            output += '\n'
        output += '# ==========================================\n'
        output += '\n'
        
        if misc.checkFileContentsSame( filePath, output ):
            print( 'CMakeLists file {} has not changed'.format( filePath ) )
        else:
            print( 'CMakeLists file {} has changed and is being generated'.format( filePath ) )
            with open( filePath, 'w' ) as outFile:
                outFile.write( output )