#!/usr/bin/python3

import os
import json

class configfile:
    def __init__( self, filePath ):
        self.__data__ = { }
        with open( filePath, 'r' ) as file:
            self.__data__ = json.load( file )

    def __getDataItem__( self, keyList ):
        try:
            node = self.__data__
            for key in keyList:
                node = node[ key ]
            return node
        except:
            print( 'Could not find key path {} in config data'.format( '/'.join( keyList ) ) )
    def __getPathWithRoot__( self, subPath ):
        return os.path.abspath( os.path.join( self.getRootPath( ), subPath ) )
    def __getPathListWithRoot__( self, keyList ):
        paths = self.__getDataItem__( keyList )
        pathsAbs = [ ]
        for path in paths:
            pathsAbs.append( self.__getPathWithRoot__( path ) )
        return pathsAbs

    def getRootPath( self ):
        return os.path.abspath( self.__getDataItem__( [ 'paths', 'root' ] ) )
    def getSourcesRoots( self ):
        return self.__getPathListWithRoot__( [ 'paths', 'sources' ] )
    def getIncludeRoots( self ):
        return self.__getPathListWithRoot__( [ 'paths', 'includes' ] )
    def getTestRoot( self ):
        return self.__getPathWithRoot__( self.__getDataItem__( [ 'paths', 'test' ] ) )