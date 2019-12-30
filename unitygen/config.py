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

    def getRootPath( self ):
        return os.path.abspath( self.__getDataItem__( [ 'paths', 'root' ] ) )
    def getSourcesRoot( self ):
        return self.__getPathWithRoot__( self.__getDataItem__( [ 'paths', 'source' ] ) )
    def getIncludeRoot( self ):
        return self.__getPathWithRoot__( self.__getDataItem__( [ 'paths', 'include' ] ) )
    def getTestRoot( self ):
        return self.__getPathWithRoot__( self.__getDataItem__( [ 'paths', 'test' ] ) )