#!/usr/bin/python3

import os
import shutil

__templateFileList__ = [
    'CMakeLists_unity.txt.in',
    'CMakeLists_cmock.txt.in',
    'runUnityTest.sh',
    'generateCMocks.sh',
    'unittest.yml'
]

def __copyTemplateFile__( fileName, templatesPath, destPath ):
    templateFilePath = os.path.join( templatesPath, fileName )
    destFilePath = os.path.join( destPath, fileName )
    if os.path.exists( destFilePath ):
        print( 'Template file {} already exists'.format( destFilePath ) )
    else:
        print( 'Copying template file {} to {}'.format( templateFilePath, destFilePath ) )
        shutil.copy2( templateFilePath, destFilePath )

def generateTemplates( basePath, testRootPath ):
    for file in __templateFileList__:
        __copyTemplateFile__( file, os.path.join( basePath, 'templates' ), testRootPath )
