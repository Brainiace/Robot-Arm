import os
import json
from calibration_manager import save_calibration, load_calibration
import config

def test_persistence():
    print("--- Testing Calibration Persistence ---")
    test_file = "calibration.json"
    if os.path.exists(test_file):
        os.remove(test_file)

    # Test saving
    success = save_calibration(0.6, 300.0, 410.0, 5.5)
    assert success == True
    assert os.path.exists(test_file)
    print("Save successful")

    # Test loading
    data = load_calibration()
    assert data["scale"] == 0.6
    assert data["offset_x"] == 300.0
    assert data["offset_y"] == 410.0
    assert data["offset_z"] == 5.5
    print("Load successful and data matches")

    # Clean up
    os.remove(test_file)
    print("Persistence Test Passed\n")

if __name__ == "__main__":
    test_persistence()
