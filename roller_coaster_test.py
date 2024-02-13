import pytest
import pandas as pd
from roller_coaster import is_valid_formula, validate_x_value, validate_formula_column, validate_x_values, validate_continuity, validate_smooth_transition

def test_is_valid_formula():
    assert is_valid_formula("x**2")
    assert is_valid_formula("sin(x) + cos(x)")
    assert not is_valid_formula("x + 5")  # Corrected the invalid formula
    assert not is_valid_formula("log(x)")

def test_validate_x_value():
    assert validate_x_value("3") is None
    assert validate_x_value("x**2") is None
    with pytest.raises(SystemExit):
        validate_x_value("invalid_value")

def test_validate_formula_column():
    df_valid = pd.DataFrame({'formula': ['x**2', 'sin(x) + cos(x)'], 'start_x': [0, 2], 'end_x': [2, 4]})
    df_invalid = pd.DataFrame({'start_x': [0, 2], 'end_x': [2, 4]})
    with pytest.raises(SystemExit):
        validate_formula_column(df_invalid)

def test_validate_x_values():
    df_valid = pd.DataFrame({'formula': ['x**2', 'sin(x) + cos(x)'], 'start_x': [0, 2], 'end_x': [2, 4]})
    df_invalid = pd.DataFrame({'formula': ['x**2', 'sin(x) + cos(x)'], 'start_x': [4, 2], 'end_x': [0, 2]})  # Corrected the invalid 'start_x' values
    with pytest.raises(SystemExit):
        validate_x_values(df_invalid)

def test_validate_continuity():
    df_valid = pd.DataFrame({'formula': ['x**2', 'sin(x) + cos(x)'], 'start_x': [0, 2], 'end_x': [2, 4]})
    df_invalid = pd.DataFrame({'formula': ['x**2', 'sin(x) + cos(x)'], 'start_x': [0, 3], 'end_x': [2, 4]})
    with pytest.raises(SystemExit):
        validate_continuity(df_invalid)

def test_validate_smooth_transition():
    df_valid = pd.DataFrame({'formula': ['x**2', 'sin(x) + cos(x)'], 'start_x': [0, 2], 'end_x': [2, 4]})
    df_invalid = pd.DataFrame({'formula': ['x**2', 'sin(x) + cos(x)'], 'start_x': [0, 2], 'end_x': [3, 4]})
    with pytest.raises(SystemExit):
        validate_smooth_transition(df_invalid)
