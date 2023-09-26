"""
Henrique R.
Arcade Car Engine - Range Component v2.0.0

Keys API: https://rangeengine.tech/api/14/html/api/bge.events.html

")
"""

import bge
from collections import OrderedDict

class ArcadeCarControlsComponent(bge.types.KX_PythonComponent):
    
    # Put your arguments here of the format ("key", default_value).
    # These values are exposed to the UI.
    
    args = OrderedDict([
        ("gas pedal", "WKEY"),
        ("brake pedal", "SKEY"),
        ("clutch mode", {"automatic_transmission", "manual_transmission+manual_clutch", "manual_tranmsission+automatic_clutch"}),
        ("clutch pedal", "LEFTSHIFTKEY"),
        ("clutch UP", "EKEY"),
        ("clutch DOWN", "QKEY"),
        ("handbrake", "SPACEKEY"),
        ("steering mode", {"keyboard", "mouse"}),
        ("steering left", "AKEY"),
        ("steering right", "DKEY"),
        ("steering sensitivity", 0.5)
    ])

    def start(self, args):
        self.object["controls"] = dict()
        
        self.object["controls"]["gas_pedal"] = args["gas pedal"]
        self.object["controls"]["brake_pedal"] = args["brake pedal"]
        self.object["controls"]["clutch_mode"] = args["clutch mode"]
        self.object["controls"]["clutch_pedal"] = args["clutch pedal"]
        self.object["controls"]["clutch_up"] = args["clutch UP"]
        self.object["controls"]["clutch_down"] = args["clutch DOWN"]
        self.object["controls"]["handbrake"] = args["handbrake"]
        self.object["controls"]["steering_mode"] = args["steering mode"]
        self.object["controls"]["steering_left"] = args["steering left"]
        self.object["controls"]["steering_right"] = args["steering right"]
        self.object["controls"]["steering_sensitivity"] = args["steering sensitivity"]
        
    def update(self):
        pass
