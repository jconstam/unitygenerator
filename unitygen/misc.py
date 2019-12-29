#!/usr/bin/python3

import os
import shutil
import argparse

def parseArgs( ):
    parser = argparse.ArgumentParser( 'Unity Test Skeleton Generator', add_help=True )
    parser.add_argument( '-s', '--sourceRoot', type=str, required=True, help='Path where the source files are located' )
    parser.add_argument( '-i', '--includeRoot', type=str, required=True, help='Path where the include files are located' )
    parser.add_argument( '-t', '--testRoot', type=str, required=True, help='Path where the test files are to be output' )
    return parser.parse_args( )

def findFiles( root, extension ):
    fileList = [ ]
    if os.path.exists( root ):
        for path, subdirs, files in os.walk( root ):
            for file in files:
                if file.endswith( extension ):
                    relPath = path.replace( root, '' )
                    if relPath.startswith( '/' ):
                        relPath = relPath[ 1: ]
                    fileList.append( os.path.join( relPath, file ) )
    return fileList 

def copyTemplateFile( fileName, templatesPath, destPath ):
    templateFilePath = os.path.join( templatesPath, fileName )
    destFilePath = os.path.join( destPath, fileName )
    if os.path.exists( destFilePath ):
        print( 'Template file {} already exists'.format( destFilePath ) )
    else:
        print( 'Copying template file {} to {}'.format( templateFilePath, destFilePath ) )
        shutil.copy2( templateFilePath, destFilePath )