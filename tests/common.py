import os
import shutil

from pathlib import Path

rootPath = os.path.join( os.path.dirname( os.path.realpath( __file__ ) ), 'testing' )

def cleanupPath( path ):
    if os.path.exists( path ):
        shutil.rmtree( path )
def setupPath( path ):
    cleanupPath( path )
    os.mkdir( path )

def setupRoot( ):
    setupPath( rootPath )
def cleanupRoot( ):
    cleanupPath( rootPath )

def createTestPath( path ):
    return os.path.join( rootPath, path )

def touchFile( filePath ):
    Path( filePath ).touch( )
