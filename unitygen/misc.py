#!/usr/bin/python3

from argparse import ArgumentParser

def parseArgs( ):
    parser = ArgumentParser( 'Unity Test Skeleton Generator', add_help=True )
    parser.add_argument( '-s', '--sourceRoot', type=str, required=True, help='Path where the source files are located' )
    parser.add_argument( '-i', '--includeRoot', type=str, required=True, help='Path where the include files are located' )
    parser.add_argument( '-t', '--testRoot', type=str, required=True, help='Path where the test files are to be output' )
    return parser.parse_args( )
