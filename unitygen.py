#!/usr/bin/python3

import os
import sys

from unitygen import misc
from unitygen import filemgr


if __name__ == "__main__":
    args = misc.parseArgs( )

    basePath = os.path.dirname( sys.argv[ 0 ] )
    templatesPath = os.path.join( basePath, 'templates' )

    sourceRootPath = os.path.abspath( args.sourceRoot )
    includeRootPath = os.path.abspath( args.includeRoot )
    testRootPath = os.path.abspath( args.testRoot )

    mgr = filemgr.filemgr( sourceRootPath, includeRootPath )
    mgr.createTestStubs( testRootPath )
    mgr.createTestCMakeList( testRootPath, sourceRootPath, includeRootPath )

    misc.copyTemplateFile( 'CMakeLists_unity.txt.in', templatesPath, testRootPath )
    misc.copyTemplateFile( 'CMakeLists_cmock.txt.in', templatesPath, testRootPath )
    misc.copyTemplateFile( 'runUnityTest.sh', templatesPath, testRootPath )
    misc.copyTemplateFile( 'generateCMocks.sh', templatesPath, testRootPath )
    misc.copyTemplateFile( 'unittest.yml', templatesPath, testRootPath )