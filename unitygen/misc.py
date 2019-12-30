#!/usr/bin/python3

import os
import hashlib
import argparse

def parseArgs( ):
    parser = argparse.ArgumentParser( 'Unity Test Skeleton Generator', add_help=True )
    parser.add_argument( '-c', '--configFile', type=str, required=True, help='Path to the test configuration file' )
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

def checkFileContentsSame( filePath, contents ):
    contentsMD5 = hashlib.md5( contents.encode( ) )

    fileMD5 = hashlib.md5( )
    if os.path.exists( filePath ):
        with open( filePath, 'rb' ) as inFile:
            for chunk in iter( lambda: inFile.read( 4096 ), b'' ):
                fileMD5.update( chunk )

    return contentsMD5.hexdigest( ) == fileMD5.hexdigest( )
