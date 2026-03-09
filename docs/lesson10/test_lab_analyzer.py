# Copyright © 2026, Brigham Young University–Idaho. All rights reserved.

import pytest
import os

# We assume students will create lab_analyzer.py
try:
    from lab_analyzer import read_dictionary, get_status
except ImportError:
    pass

def test_read_dictionary():
    """Verify that the read_dictionary function correctly reads
    the lab_tests.csv file into a compound dictionary."""
    filename = "lab_tests.csv"
    
    if not os.path.exists(filename):
        pytest.fail(f"Could not find {filename}. Ensure it is in the same folder.")

    # Call the student's function. 
    # Index 0 is the TestCode (GLU, CHO, etc.)
    tests_dict = read_dictionary(filename, 0)
    
    assert isinstance(tests_dict, dict), "read_dictionary must return a dictionary"
    assert len(tests_dict) >= 8, "lab_tests.csv should have at least 8 entries"
    
    # Check a specific value (Glucose)
    # Organization: {code: [code, name, min, max]}
    assert "GLU" in tests_dict, "Test code 'GLU' missing from dictionary"
    glu_info = tests_dict["GLU"]
    assert len(glu_info) == 4, "Each dictionary value should be a list of 4 items"
    assert glu_info[1] == "Glucose"
    assert float(glu_info[2]) == 70.0
    assert float(glu_info[3]) == 99.0

def test_get_status():
    """Verify that get_status returns the correct string 
    based on the result and range."""
    # Parameters: result, min, max
    assert get_status(85, 70, 99) == "Normal"
    assert get_status(115, 70, 99) == "High"
    assert get_status(65, 70, 99) == "Low"
    assert get_status(13.5, 13.5, 17.5) == "Normal"
    assert get_status(17.5, 13.5, 17.5) == "Normal"
    assert get_status(13.5, 13.5, 13.5) == "Normal"

if __name__ == "__main__":
    pytest.main(["-v", "--tb=line", "-rN", __file__])
