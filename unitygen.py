#!/usr/bin/python3

import os
import sys

from unitygen import misc, filemgr, templates


if __name__ == "__main__":
    args = misc.parseArgs( )

    # sourceRootPath = os.path.abspath( args.sourceRoot )
    # includeRootPath = os.path.abspath( args.includeRoot )
    # testRootPath = os.path.abspath( args.testRoot )

    # mgr = filemgr.filemgr( sourceRootPath, includeRootPath )
    # mgr.createTestStubs( testRootPath )
    # mgr.createTestCMakeList( testRootPath, sourceRootPath, includeRootPath )

    templates.generateTemplates( os.path.dirname( sys.argv[ 0 ] ), testRootPath )