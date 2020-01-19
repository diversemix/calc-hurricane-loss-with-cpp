from gethurricaneloss import __version__, __author__, __licence__


def test_meta() -> None:
    assert __author__ == 'diversemix'
    assert __licence__ == 'MIT'
    assert __version__.count('.') == 2
