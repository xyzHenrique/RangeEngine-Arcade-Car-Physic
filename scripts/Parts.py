engines = {
    "Personal": {},
    
    "Street": {
        "power": 120,
        "rpm_min": 920,
        "rpm_max": 7200,
        "rpm_rev": 150
    },
    
    "Sport": {
        "power": 220,
        "rpm_min": 930,
        "rpm_max": 8200,
        "rpm_rev": 250
    },
    
    "Super": {
        "power": 320,
        "rpm_min": 940,
        "rpm_max": 9200,
        "rpm_rev": 450
    }
}

transmissions = {
    "Personal": {},
    
    "Street": {
        "ratio": {-1: 3.7, 0: 0, 1: 3.5, 2: 2.5, 3: 1.8, 4: 1.4, 5: 1.0, 6: 0.8}
    },
    
    "Sport": {
        "ratio": {-1: 3.0, 0: 0, 1: 2.8, 2: 2.0, 3: 1.5, 4: 1.2, 5: 1.0, 6: 0.8}
    },
    
    "Super": {
        "ratio": {-1: 3.4, 0: 0, 1: 3.5, 2: 2.5, 3: 1.8, 4: 1.4, 5: 1.0, 6: 0.8, 7: 0.6}
    },
}

tires = {
    "Personal": {},
    
    "Street": {
        "width_mm": 205,
        "aspect_ratio": 52,
        "wheel_diameter_inches": 16
    },
    "Sport": {
        "width_mm": 305,
        "aspect_ratio": 54,
        "wheel_diameter_inches": 18
    },
    
    "Super": {
        "width_mm": 405,
        "aspect_ratio": 56,
        "wheel_diameter_inches": 20
    }
}

turbos = {
    "Personal": {},
    
    "Street": {
        "size": (42, 48),
        "psi": 16
    },
    
    "Sport": {
        "size": (42, 48), 
        "psi": 24
    },
    
    "": {
        "size": (50, 70),
        "psi": 32
    } 
}


