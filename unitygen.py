#!/usr/bin/python3

import os
import sys

from unitygen import misc, filemgr, templates, config


if __name__ == "__main__":
    args = misc.parseArgs( )

    configData = config.configfile( os.path.abspath( args.configFile ) )

    sources = configData.getSourcesRoots( )
    includes = configData.getIncludeRoots( )
    testRootPath = configData.getTestRoot( )

    mgr = filemgr.filemgr( sources, includes )
    mgr.createTestStubs( testRootPath )
    mgr.createTestCMakeList( testRootPath )

    templates.generateTemplates( os.path.dirname( sys.argv[ 0 ] ), testRootPath )