#!/usr/bin/python3

import os
import pytest
import argparse

try:
    from unittest import mock  # python 3.3+
except ImportError:
    import mock  # python 2.6-3.2

from unitygen import templates
from tests import common

def setup_function( ):
    common.setupRoot( )
def teardown_function( ):
    common.cleanupRoot( )

def test_generateTemplates( capsys ):
    sourceFolder = common.createTestPath( 'source' )
    templateFolder = os.path.join( sourceFolder, 'templates' )
    destFolder = common.createTestPath( 'dest' )
    common.setupPath( sourceFolder )
    common.setupPath( templateFolder )
    common.setupPath( destFolder )

    for file in templates.__templateFileList__:
        common.touchFile( os.path.join( templateFolder, file ) )

    templates.generateTemplates( sourceFolder, destFolder )
    captured = capsys.readouterr( )

    output = ''
    for file in templates.__templateFileList__:
        output += 'Copying template file {} to {}\n'.format( os.path.join( templateFolder, file ), os.path.join( destFolder, file ) )
        assert os.path.exists( os.path.join( destFolder, file ) )
    assert captured.out == output

    templates.generateTemplates( sourceFolder, destFolder )
    captured = capsys.readouterr( )
    
    output = ''
    for file in templates.__templateFileList__:
        output += 'Template file {} already exists\n'.format( os.path.join( destFolder, file ) )
        assert os.path.exists( os.path.join( destFolder, file ) )
    assert captured.out == output


