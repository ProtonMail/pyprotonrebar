from pyprotonrebar import pyrackndr


def test_class_init():
    """Assert the class is initialized with the proper Rebar object."""
    auth = {'Token': 'phony'}
    obj = pyrackndr.RackNDr('https://localhost:8092', auth, 'params')

    assert obj.resource == 'params'
