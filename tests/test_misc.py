
import pytest
import argparse

try:
    from unittest import mock  # python 3.3+
except ImportError:
    import mock  # python 2.6-3.2

from unitygen import misc

@mock.patch( 'argparse.ArgumentParser.parse_args', return_value=argparse.Namespace( sourceRoot='rootPath', includeRoot='includePath', testRoot='testPath' ) )
def test_parseArgs( mock_args ):
    args = misc.parseArgs( )

    assert args.sourceRoot == 'rootPath'
    assert args.includeRoot == 'includePath'
    assert args.testRoot == 'testPath'