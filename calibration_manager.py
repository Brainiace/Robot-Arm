import json
import os
import config

CALIBRATION_FILE = "calibration.json"

def load_calibration():
    defaults = {
        "scale": config.DEFAULT_SCALE,
        "offset_x": config.ORIGIN_PX_X,
        "offset_y": config.ORIGIN_PX_Y,
        "offset_z": config.Z_WRITE
    }
    if os.path.exists(CALIBRATION_FILE):
        try:
            with open(CALIBRATION_FILE, "r") as f:
                data = json.load(f)
                # Merge with defaults to ensure all keys exist
                defaults.update(data)
        except Exception as e:
            print(f"Error loading calibration: {e}")
    return defaults

def save_calibration(scale, offset_x, offset_y, offset_z):
    data = {
        "scale": scale,
        "offset_x": offset_x,
        "offset_y": offset_y,
        "offset_z": offset_z
    }
    try:
        with open(CALIBRATION_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving calibration: {e}")
        return False
