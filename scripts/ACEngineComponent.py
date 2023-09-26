"""
Henrique R.
Arcade Car Engine - Range Component v2.0.0

API: https://rangeengine.tech/api/14/html/api/

")
"""

import bge
from collections import OrderedDict
from scripts.Utils import lerp, clamp, smooth, timer, get_driver_ratio, get_tire_circumference
from scripts.Cars import Car1, Car2, Car3

class ArcadeCarEngineComponent(bge.types.KX_PythonComponent):
    # Argumentos do componente
    args = OrderedDict([
        ("Component Enabled", True)
    ])

    def start(self, args):
        # Carro atual
        self.car = Car2()

        # Inicialização de parâmetros do carro
        self.initialize_car_parameters()

        # Inicialização de propriedades do carro
        self.initialize_car_properties()

        # Inicialização dos pedais
        self.initialize_pedals()

        # Teclado
        self.keyboard = bge.logic.keyboard.inputs
        
        self.torque_nm_display = 0

    # Seção de inicialização
    def initialize_car_parameters(self):
        # Parâmetros do carro
        self.car_name = self.car.name
        self.car_mass = self.car.mass
        
        # Motor
        self.car_engine_power = self.car.installed_engine["power"]
        self.car_engine_rpm_min = self.car.installed_engine["rpm_min"]
        self.car_engine_rpm_max = self.car.installed_engine["rpm_max"]
        self.car_engine_rpm_rev = self.car.installed_engine["rpm_rev"]

        # Transmissão
        self.car_transmission_ratio = self.car.installed_transmission["ratio"]

        # Pneus
        self.car_tire_width_mm = self.car.installed_tire["width_mm"]
        self.car_tire_aspect_ratio = self.car.installed_tire["aspect_ratio"]
        self.car_tire_wheel_diameter_inches = self.car.installed_tire["wheel_diameter_inches"]
        self.car_tire_circumference = get_tire_circumference(
            self.car_tire_width_mm, self.car_tire_aspect_ratio, self.car_tire_wheel_diameter_inches
        )

    def initialize_car_properties(self):
        # Propriedades do motor/transmissão
        self.hp = 0.0
        self.whp = 0.0
        self.rpm = 0.0
        self.gear = 0.0
        self.torque_nm = 0.0
        self.torque_kgf = 0.0

        # Propriedades do freio
        self.brake_power = 0.0
        self.brake_power_max = 2.5
        self.brake_power_factor = 0.1
        self.engine_resistance = 0.0

        # Propriedades da velocidade
        self.speed = 0

    def initialize_pedals(self):
        # Pedais do carro
        self.gas_pedal_pressed = False
        self.gas_pedal_factor = 0.0

        self.brake_pedal_pressed = False
        self.brake_pedal_factor = 0.0

        self.clutch_pedal_pressed = False
        self.clutch_pedal_factor = 0.0

        self.pedals_smooth = 0.025
        self.pedals_smooth_max = 1.0

    # Seção dos pedais
    def increase_pedal_factor(self, pedal_factor):
        if pedal_factor < self.pedals_smooth_max:
            pedal_factor += self.pedals_smooth
            if pedal_factor > self.pedals_smooth_max:
                pedal_factor = self.pedals_smooth_max
        return pedal_factor
    
    def decrease_pedal_factor(self, pedal_factor):
        if pedal_factor > 0.0:
            pedal_factor -= self.pedals_smooth
            if pedal_factor < 0.0:
                pedal_factor = 0.0
        return pedal_factor
             
    def gas_pedal(self):
        key = self.keyboard[bge.events.__dict__[f"{self.object['controls']['gas_pedal']}"]]
        if key.active:
            self.gas_pedal_pressed = True
            self.gas_pedal_factor = self.increase_pedal_factor(self.gas_pedal_factor)
        else:
            self.gas_pedal_pressed = False
            self.gas_pedal_factor = self.decrease_pedal_factor(self.gas_pedal_factor)

    def brake_pedal(self):
        key = self.keyboard[bge.events.__dict__[f"{self.object['controls']['brake_pedal']}"]]
        if key.active:
            self.brake_pedal_pressed = True
            self.brake_pedal_factor = self.increase_pedal_factor(self.brake_pedal_factor)
        else:
            self.brake_pedal_pressed = False
            self.brake_pedal_factor = self.decrease_pedal_factor(self.brake_pedal_factor)

    def clutch_pedal(self):
        key = self.keyboard[bge.events.__dict__[f"{self.object['controls']['clutch_pedal']}"]]
        if key.active:
            self.clutch_pedal_pressed = True
            self.clutch_pedal_factor = self.increase_pedal_factor(self.clutch_pedal_factor)
            
        else:
            self.clutch_pedal_pressed = False
            self.clutch_pedal_factor = self.decrease_pedal_factor(self.clutch_pedal_factor)

    # Seção de freio
    def brake(self):
        key = self.keyboard[bge.events.__dict__[f"{self.object['controls']['brake_pedal']}"]]

        def increase_brake_power():
            if self.brake_power < self.brake_power_max:
                self.brake_power += self.brake_power_factor * self.brake_pedal_factor / self.car_mass
                if self.brake_power > self.brake_power_max:
                    self.brake_power = self.brake_power_max

        if key.active:
            print(self.brake_pedal_factor)
            increase_brake_power()
            for wheel in range(4):
                self.object["vehicle"].applyBraking(self.brake_power, wheel)
        else:
            self.brake_power = 0
            for wheel in range(4):
                self.object["vehicle"].applyBraking(0, wheel)
                
    # Seção de transmissão
    def transmission(self):
        keyTAP = bge.logic.KX_INPUT_JUST_ACTIVATED
        up_key = self.keyboard[bge.events.__dict__[f"{self.object['controls']['clutch_up']}"]]
        down_key = self.keyboard[bge.events.__dict__[f"{self.object['controls']['clutch_down']}"]]

        def effect():
            self.clutch_pedal_factor = 1
            self.gas_pedal_factor = 0

        def down_gear():
            effect()
            self.gear -= 1

        def up_gear():
            effect()
            self.gear += 1

        # Modo embreagem manual + automática
        if self.object["controls"]["clutch_mode"] == "manual_tranmsission+automatic_clutch":
            if keyTAP in up_key.queue and self.gear < 6:
                up_gear()
            elif keyTAP in down_key.queue and self.gear > -1:
                down_gear()

        # Modo embreagem manual + manual
        if self.object["controls"]["clutch_mode"] == "manual_transmission+manual_clutch":
            if self.clutch_pedal_pressed:
                if keyTAP in up_key.queue and self.gear < 6:
                    up_gear()
                elif keyTAP in down_key.queue and self.gear > -1:
                    down_gear()
                    
        # Modo embreagem automática
        if self.object["controls"]["clutch_mode"] == "automatic_transmission":
            shift_speeds = [40, 80, 110, 140, 180, 280]

            # Converta self.gear em um número inteiro
            gear_int = int(self.gear)

            # Verifique se o carro está em primeira marcha e a velocidade atual é maior que um limite
            if gear_int == 0 and self.speed > -1:
                up_gear()  # Aumenta automaticamente a marcha

            # Se a velocidade atual exceder o limite de troca de marcha, faça a troca
            elif self.rpm > 3200 and self.speed > shift_speeds[gear_int - 1] and gear_int < 6:
                up_gear()
            elif self.rpm < 3100 and shift_speeds[gear_int - 2] and gear_int > 1:
                down_gear()
                
    # Seção do motor
    def engine(self):
        if self.gear > 0:
            self.rpm = self.get_rpm(
                self.speed, self.car_transmission_ratio[self.gear], self.car_tire_circumference
            )

        if self.brake_power > 0.1:
            self.object["vehicle"].setTyreFriction(0.1, 2)
            self.object["vehicle"].setTyreFriction(0.1, 3)
        else:
            self.object["vehicle"].setTyreFriction(8, 2)
            self.object["vehicle"].setTyreFriction(8, 2)
        
        if self.gas_pedal_pressed:
            if not self.rpm > self.car_engine_rpm_max:
                self.calculate_power()
                self.apply_torque(self.torque_nm)
            else:
                self.apply_torque(0)
        else:
            if self.speed > 0:
                if self.brake_pedal_pressed:
                    self.calculate_engine_brake()
                else:
                    if self.speed > 2:
                        pass
                        self.calculate_engine_resistance()
                    pass
            self.apply_torque(0)

    def calculate_power(self):
        power_watts = self.car_engine_power * 745.7
        self.hp = power_watts / 745.7
        self.torque_nm = (power_watts * 60) / (2 * 3.1416 * self.rpm)
        self.torque_nm *= (self.gas_pedal_factor * self.car_transmission_ratio[self.gear])
        self.torque_nm /= self.car_mass * 0.1
        
        self.torque_nm_display = (power_watts * 60) / (2 * 3.1416 * self.rpm)
        self.torque_nm_display *= (self.gas_pedal_factor * self.car_transmission_ratio[self.gear])

    def calculate_engine_brake(self):
        self.engine_resistance = (self.rpm / self.torque_nm) * (
            self.car_transmission_ratio[self.gear] / self.speed
        ) * self.brake_power

        self.engine_resistance *= (self.car_mass / 1300)
        
        for w in range(4):
            self.object["vehicle"].applyBraking(self.engine_resistance, w)

    def calculate_engine_resistance(self):
        if self.torque_nm != 0.0 and self.speed != 0.0:
            self.engine_resistance = (self.rpm / self.torque_nm) * (
                self.car_transmission_ratio[self.gear] / self.speed
            ) / self.car_mass
        else:
            self.engine_resistance = 0.0  # Lida com o caso em que self.torque_nm ou self.speed é igual a zero

        for wheel in range(4):
            self.object["vehicle"].applyBraking(self.engine_resistance, wheel)

    def get_rpm(self, velocity_km_h, gear_ratio, tire_circumference):
        rpm = (velocity_km_h / 3.6 * gear_ratio * 60) / tire_circumference 
        rpm *= 4
        if rpm < self.car_engine_rpm_min:
            rpm = self.car_engine_rpm_min
        if rpm > self.car_engine_rpm_max:
            self.rpm = self.car_engine_rpm_max

        return rpm

    def apply_torque(self, torque):
        for wheel in range(4):
            self.object["vehicle"].applyEngineForce(-torque, wheel)

    def get_relative_gear(self, gear):
        relative = gear
        gear -= (gear - 1)
        return relative

    def update_object_properties(self):
        self.whp = (self.torque_nm_display * self.speed) / (self.car_engine_power)
        self.torque_kgf = self.torque_nm_display * 0.1019716213
        
        self.object["display_speed"] = self.speed
        self.object["display_rpm"] = self.rpm
        self.object["display_gear"] = self.gear
        self.object["display_torque_nm"] = f"{int(self.torque_nm_display)} N.m"
        self.object["display_torque_kgf"] = f"{int(self.torque_kgf)} Kgf"
        self.object["display_engine_brake"] = self.engine_resistance
        self.object["display_brake_power"] = self.brake_power
        self.object["display_hp"] = self.hp
        self.object["display_whp"] = self.whp
        self.object["display_gas_pedal"] = self.gas_pedal_factor
        self.object["display_brake_pedal"] = self.brake_pedal_factor
        self.object["display_clutch_pedal"] = self.clutch_pedal_factor

    def update(self):
        if self.object["physic"] and self.object["vehicle"]:
            self.speed = self.object["speed"]

            self.gas_pedal()
            self.brake_pedal()
            self.clutch_pedal()
            self.brake()
            self.engine()
            self.transmission()
            self.update_object_properties()
        else:
            print("Physics was not created")
