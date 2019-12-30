#!/usr/bin/python3

import os
import sys

from unitygen import misc, filemgr, templates, config


if __name__ == "__main__":
    args = misc.parseArgs( )

    configData = config.configfile( os.path.abspath( args.configFile ) )

    sourceRootPath = configData.getSourcesRoot( )
    includeRootPath = configData.getIncludeRoot( )
    testRootPath = configData.getTestRoot( )

    mgr = filemgr.filemgr( sourceRootPath, includeRootPath )
    mgr.createTestStubs( testRootPath )
    mgr.createTestCMakeList( testRootPath, sourceRootPath, includeRootPath )

    templates.generateTemplates( os.path.dirname( sys.argv[ 0 ] ), testRootPath )