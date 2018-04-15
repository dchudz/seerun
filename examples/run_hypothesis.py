from hypothesis import given, strategies as st, settings


@settings(max_examples=5, database=None)
# @settings(database=None)
@given(st.floats(min_value=-1, max_value=3))
def test_one_of_filtered(x):
    assert x**2 < 10


test_one_of_filtered()
