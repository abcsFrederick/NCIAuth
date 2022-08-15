import pytest

from girder.plugin import loadedPlugins


@pytest.mark.plugin('nciauth_girder3')
def test_import(server):
    assert 'nciauth_girder3' in loadedPlugins()
