from hypothesis import given, strategies as st, settings


@settings(max_examples=5, database=None)  # seerun is VERY slow, so only run 5 examples
@given(st.floats())
def test_one_of_filtered(x):
    assert x**2 < 10


test_one_of_filtered()
