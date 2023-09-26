from scripts.Parts import engines, transmissions, turbos, tires

class Car1:
    def __init__(self):
        # ~ car
        self.name = "Nissan Skyline - Street"
        self.mass = 1260 # KG
        
        # ~ installed parts
        self.installed_engine = engines["Street"]
        self.installed_transmission = transmissions["Street"]
        self.installed_tire = tires["Street"]

class Car2:
    def __init__(self):
        # ~ car
        self.name = "Nissan Skyline R32 - Sport"
        self.mass = 1250 # KG
    
        # ~ installed parts
        self.installed_engine = engines["Sport"]
        self.installed_transmission = transmissions["Sport"]
        self.installed_tire = tires["Sport"]

class Car3:
    def __init__(self):
        # ~ car
        self.name = "Nissan Skyline R32 - Super"
        self.mass = 1240 # KG
        
        # ~ installed parts
        self.installed_engine = engines["Super"]
        self.installed_transmission = transmissions["Super"]
        self.installed_tire = tires["Super"]