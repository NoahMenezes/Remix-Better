"""Pipeline smoke tests (expanded in each phase). Run: ./venv/bin/python -m pytest tests/ -v"""


def test_stubs_importable():
    import pipeline.align
    import pipeline.analyze
    import pipeline.generate
    import pipeline.mix
    import pipeline.separate

    assert callable(pipeline.separate.separate)
    assert callable(pipeline.analyze.analyze)
    assert callable(pipeline.generate.generate)
    assert callable(pipeline.align.align)
    assert callable(pipeline.mix.mix)
