import pytest

from zipcode_features import us_get_demographics


LEADING_ZERO_FIPS_STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT"]
CONTROL_STATES = ["TX", "NY", "FL"]


@pytest.mark.parametrize("state", LEADING_ZERO_FIPS_STATES + CONTROL_STATES)
def test_us_get_demographics_not_empty(state):
    df = us_get_demographics(state=state)
    assert len(df) > 0, f"us_get_demographics({state!r}) returned an empty DataFrame"
