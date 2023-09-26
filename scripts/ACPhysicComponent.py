"""
Henrique R.
Arcade Car Physic - Range Component v2.0.0
"""

# Importações necessárias
import bge
import math
import mathutils
from collections import OrderedDict

from scripts.Utils import lerp, clamp

# Classe para o componente de física do carro
class ArcadeCarPhysicComponent(bge.types.KX_PythonComponent):
    args = OrderedDict([
        ("wheel FR", ""),
        ("wheel FL", ""),
        ("wheel RR", ""),
        ("wheel RL", ""),
        ("wheels F position", 1.0),
        ("wheels R position", 1.0),
        ("wheels friction", 100.0),
        ("wheels spacing", 1.0),
        ("wheels height", 1.0),
        ("wheels radius", 1.0),
        ("suspension compression", 5.0),
        ("suspension stiffness", 25.0),
        ("suspension damping", 10.0),
        ("suspension length", 0.0),
        ("suspension roll", 0.01),
        ("vehicle visible", True),
        ("wheels visible", True)
    ])

    # Função chamada no início para configurar o componente
    def start(self, args):
        # Atribui o dicionário de argumentos
        self.args = args

        # Obtém o teclado para input
        self.keyboard = bge.logic.keyboard.inputs
        
        self.previous_velocity = mathutils.Vector((0.0, 0.0, 0.0))
        self.is_drift_locked = False
        # Inicializa a física do carro
        self.initialize_physic()
        
    # Função para inicializar a física do carro
    def initialize_physic(self):
        # Obtém o ID da física do objeto
        self.physic = self.object.getPhysicsId()
        
        # Cria um veículo para a física
        self.vehicle = bge.constraints.createVehicle(self.physic)
        
        # Inicializa os argumentos
        self.initialize_args()
    
    # Função para inicializar os argumentos
    def initialize_args(self):
        # Rodas
        self.wheels_f_position = self.args["wheels F position"]
        self.wheels_r_position = self.args["wheels R position"]
        self.wheels_friction = self.args["wheels friction"]
        self.wheels_spacing = self.args["wheels spacing"]
        self.wheels_height = self.args["wheels height"]
        self.wheels_radius = self.args["wheels radius"]
        
        # Suspensão
        self.suspension_compression = self.args["suspension compression"]
        self.suspension_stiffness = self.args["suspension stiffness"]
        self.selfsuspension_damping = self.args["suspension damping"]
        self.suspension_length = self.args["suspension length"]
        self.suspension_roll = self.args["suspension roll"]
        
        # Parâmetros personalizados
        self.initalize_parameters()

    # Função para inicializar parâmetros personalizados
    def initalize_parameters(self):
        self.angular_velocity = float()
        self.angular_velocity_x = float()
        self.angular_velocity_y = float()
        self.angular_velocity_z = float()
        
        self.lateral_g = float()
        self.lateral_acceleration = float()
        self.lateral_movement_direction = float()
        
        self.horizontal_force = float()
        self.vertical_force = float()
        
        self.adjust_compression_factor = 0.01
        self.adjust_damping_factor = 5.0
        self.adjust_incline_factor = 3.0
        self.adjust_inertia_factor = 2.0
        
        self.speed = 0
        self.steering = 0
        
        self.is_drifting = False 
        self.drift_threshold = 5.0 

        self.drift_angle = 0.0  
        self.target_drift_angle = 0.0
        
        self.mcpherson_compression_multiplier = 5.0
        self.mcpherson_suspension_compression = 0.0
        
        self.adjust_steering_incline_factor = 90
        
        self.adjust_roll_incline_factor = 0.45

        self.max_lateral_force = 5000.0
        
        # Inicializa as rodas
        self.initialize_wheels()      
        
    # Função para inicializar as rodas do carro
    def initialize_wheels(self):
        # Cria um dicionário para armazenar as rodas
        self.wheels = {
            "FR": self.object.children[self.args["wheel FR"]],
            "FL": self.object.children[self.args["wheel FL"]],
            "RR": self.object.children[self.args["wheel RR"]],
            "RL": self.object.children[self.args["wheel RL"]]
        }
        
        # Remove o parentesco das rodas com o objeto principal
        for wheel_index in self.wheels:
            self.wheels[wheel_index].removeParent()
            self.wheels[wheel_index].visible = self.args["wheels visible"]
        
        # Inicializa a suspensão
        self.initialize_suspension()

    # Função para inicializar a suspensão do carro
    def initialize_suspension(self):
        # Vetores para configurar a suspensão
        wheels_down = [0.0, 0.0, -1.0]
        wheels_axle = [-1.0, 0.0, 0.0]
        
        # Adiciona as rodas ao veículo
        self.vehicle.addWheel(self.wheels["FR"], [self.wheels_spacing, self.wheels_f_position, -self.args["wheels height"]], wheels_down, wheels_axle, self.suspension_length, self.wheels_radius, True)
        self.vehicle.addWheel(self.wheels["FL"], [-self.wheels_spacing, self.wheels_f_position, -self.args["wheels height"]], wheels_down, wheels_axle, self.suspension_length, self.wheels_radius, True)
        self.vehicle.addWheel(self.wheels["RR"], [self.wheels_spacing, -self.wheels_r_position, -self.args["wheels height"]], wheels_down, wheels_axle, self.suspension_length, self.wheels_radius, False)
        self.vehicle.addWheel(self.wheels["RL"], [-self.wheels_spacing, -self.wheels_r_position, -self.args["wheels height"]], wheels_down, wheels_axle, self.suspension_length, self.wheels_radius, False)
        
        # Configura os parâmetros da suspensão para as rodas
        for wheel_index in range(4):
            self.vehicle.setSuspensionCompression(self.args["suspension compression"], wheel_index)
            self.vehicle.setSuspensionStiffness(self.args["suspension stiffness"], wheel_index)
            self.vehicle.setSuspensionDamping(self.args["suspension damping"], wheel_index)
            self.vehicle.setTyreFriction(self.args["wheels friction"], wheel_index)
            self.vehicle.setRollInfluence(self.args["suspension roll"], wheel_index)
        
        # Configura atributos no objeto para uso posterior
        self.object["physic"] = self.physic
        self.object["vehicle"] = self.vehicle

    # Função para controlar o ângulo de direção
    def steering_control(self):
        if self.object["controls"]:
            # Mapeamento das teclas de direção
            steering_left_key = bge.events.__dict__[f"{self.object['controls']['steering_left']}"]
            steering_right_key = bge.events.__dict__[f"{self.object['controls']['steering_right']}"]

            # Dentro da função steering_control
            if self.is_drifting:
                if not self.is_drift_locked:
                    # Verifique se o ângulo de derrapagem ultrapassa um limite (por exemplo, 45 graus)
                    drift_limit = math.radians(45.0)
                    if abs(self.drift_angle) > drift_limit:
                        # Congele o ângulo de derrapagem
                        self.is_drift_locked = True
                else:
                    # Mantenha o ângulo de derrapagem congelado
                    self.drift_angle = math.copysign(drift_limit, self.drift_angle)
            else:
                # Quando não estiver derrapando, desbloqueie o ângulo de derrapagem
                self.is_drift_locked = False

            # Verifica se a assistência à direção está habilitada
            steering_assist_enabled = True
            
            # Calcula o ângulo de esterçamento alvo apenas se a assistência à direção estiver habilitada
            if steering_assist_enabled:
                # Cálculo do ângulo de esterçamento alvo
                target_steering = 0.0
                if self.keyboard[steering_left_key].active:
                    target_steering = 0.25
                elif self.keyboard[steering_right_key].active:
                    target_steering = -0.25

                # Aplica o fator de assistência à direção
                steering_assist_factor = 0.3
                target_steering += steering_assist_factor * (self.target_drift_angle - self.steering)
            else:
                # Se a assistência à direção estiver desabilitada, o ângulo de esterçamento alvo é diretamente das teclas de direção
                target_steering = 0.0
                if self.keyboard[steering_left_key].active:
                    target_steering = 0.5
                elif self.keyboard[steering_right_key].active:
                    target_steering = -0.5

            # Suaviza a transição do ângulo de esterçamento atual para o ângulo alvo
            smoothing_factor = 0.025
            self.steering = lerp(self.steering, target_steering, smoothing_factor)

            # Calcula o ângulo de Ackermann e o raio de giro
            wheelbase = self.object.get("wheelbase", self.wheels_radius)
            if self.steering > 0.0 or self.steering < 0.0:
                turn_radius = wheelbase / math.tan(self.steering)

                # Define o ângulo de direção das rodas dianteiras (FR e FL)
                self.vehicle.setSteeringValue(math.atan(wheelbase / (turn_radius + 0.5)), 0)  # Roda FR
                self.vehicle.setSteeringValue(math.atan(wheelbase / (turn_radius - 0.5)), 1)  # Roda FL

    # Função para ajustar a suspensão com base na velocidade e direção
    def adjust_suspension(self):
        lateral_velocity = self.object.getLinearVelocity(True)
        lateral_speed = mathutils.Vector(lateral_velocity).length

        # Calcular a aceleração lateral (em m/s^2)
        lateral_acceleration = lateral_speed * self.angular_velocity_y

        # Limitar o ângulo de rolagem para evitar capotamento
        max_roll_angle = 0.52  # Defina o ângulo máximo de rolagem permitido
        roll_angle = min(max(lateral_acceleration / 9.81, -max_roll_angle), max_roll_angle)

        # Ajuste do fator de peso do carro (em Newtons)
        weight_factor = (self.object.mass * 9.81) / 1300.0  # 1300 kg é o peso do carro

        # Determine a direção da inclinação com base na aceleração lateral
        roll_direction = 1.0 if lateral_acceleration > 0 else -1.0

        # Cálculo da compressão da suspensão com base na aceleração lateral, damping, força e velocidade
        suspension_compression = self.args["suspension compression"] * (
            1.0 + weight_factor
            - 0.01 * lateral_speed  # Fator de velocidade (ajuste conforme necessário)
            - 0.001 * self.speed  # Fator de velocidade do carro (ajuste conforme necessário)
        )

        # Cálculo do damping da suspensão com base na aceleração lateral, damping, força e velocidade
        damping_factor = self.args["suspension damping"] * (
            1.0 + weight_factor
            - 0.01 * lateral_speed  # Fator de velocidade (ajuste conforme necessário)
            - 0.001 * self.speed  # Fator de velocidade do carro (ajuste conforme necessário)
        )

        # Ajuste da influência do ângulo de rolagem nas rodas
        for wheel in range(4):
            self.vehicle.setRollInfluence(roll_angle * self.adjust_roll_incline_factor * roll_direction, wheel)

            # Ajuste a compressão da suspensão
            self.vehicle.setSuspensionCompression(suspension_compression, wheel)

            # Ajuste o damping da suspensão
            self.vehicle.setSuspensionDamping(damping_factor, wheel)
    
    def calculate_inertia(self):
        # Suponha que você tenha uma variável que rastreia a taxa de mudança de velocidade do veículo
        acceleration = self.object.getLinearVelocity() - self.previous_velocity
        inertia = acceleration.length * self.object.mass
        return inertia

    def calculate_friction_force(self):
        # Coeficiente de atrito dos pneus máximo
        mu = 0.8

        # Velocidade do veículo
        speed = self.speed

        # Ângulo de derrapagem (diferença entre a direção do veículo e a direção de movimento)
        angle_of_slip = self.steering - self.object.worldOrientation.to_euler().z

        # Fator de aderência nas curvas (ajuste conforme necessário)
        aderencia_curvas = 1.5

        # Fator de "drift"
        drift_factor = 0.3

        # Define a velocidade ou ângulo de derrapagem a partir da qual o "drift" começa
        drift_speed_threshold = 10.0  # Ajuste conforme necessário
        drift_angle_threshold = math.radians(30.0)  # Ajuste conforme necessário

        # Verifica se o carro atingiu as condições para começar o "drift"
        if speed > drift_speed_threshold or abs(angle_of_slip) > drift_angle_threshold:
            drift_factor = 0.5  # Reduz a aderência ao iniciar o "drift"

        # Fator de controle de estabilidade (ESP)
        esp_factor = 2  # Ajuste conforme necessário

        # Fator de estabilidade com base na velocidade (ajuste conforme necessário)
        stability_factor = 0.2  # Ajuste conforme necessário

        # Aumenta a estabilidade com base na velocidade
        stability_factor += speed * 0.01  # Ajuste conforme necessário

        # Limita o fator de estabilidade a um valor máximo
        max_stability_factor = 0.5  # Ajuste conforme necessário
        stability_factor = min(stability_factor, max_stability_factor)

        # Calcula o coeficiente de atrito ajustado com base na força lateral, no ESP, e no fator de estabilidade
        mu_adjusted_front = mu * aderencia_curvas * math.cos(angle_of_slip) * drift_factor * esp_factor * stability_factor
        mu_adjusted_rear = mu * aderencia_curvas * math.cos(angle_of_slip) * esp_factor * stability_factor

        # Calcula a força de fricção máxima para as rodas dianteiras
        max_friction_force_front = mu_adjusted_front * self.object.mass * 9.81

        # Calcula a força de fricção máxima para as rodas traseiras
        max_friction_force_rear = mu_adjusted_rear * self.object.mass * 9.81

        # Força de fricção atual (considerando o ângulo de derrapagem)
        friction_force_front = max_friction_force_front * math.cos(angle_of_slip)
        friction_force_rear = max_friction_force_rear * math.cos(angle_of_slip)

        return friction_force_front, friction_force_rear
        

    # Função de atualização chamada a cada quadro
    def update(self):
        # Mantém o objeto olhando para cima
        self.object.lookAt([0.0, 0.0, 1.0], 2, 0.92)
        
        # Calcula a velocidade do carro
        self.speed = mathutils.Vector(self.object.getLinearVelocity()).magnitude * 3.6
        self.object["speed"] = self.speed
        
        # Calcula a velocidade angular
        self.angular_velocity = self.object.getAngularVelocity(True)
        self.angular_velocity_x = self.angular_velocity[0]
        self.angular_velocity_y = self.angular_velocity[1]
        self.angular_velocity_z = self.angular_velocity[2]

        # Calcula a aceleração lateral
        self.lateral_acceleration = self.angular_velocity_y * self.speed
        
        # Calcula a inércia do veículo
        #inertia = self.calculate_inertia()
        
        # Calcula a força de fricção
        friction_force = self.calculate_friction_force()

        self.vehicle.setTyreFriction(friction_force[0]*8, 0)
        self.vehicle.setTyreFriction(friction_force[0]*8, 1)
        self.vehicle.setTyreFriction(friction_force[1], 2)
        self.vehicle.setTyreFriction(friction_force[1], 3)
        
        # Se a inércia for maior que um valor definido, ajusta temporariamente o coeficiente de atrito das rodas traseiras
        #if inertia > 0.1:
            #self.vehicle.setTyreFriction(5, 2)
            #self.vehicle.setTyreFriction(5, 3)
        #else:
            # Caso contrário, restaura o coeficiente de atrito das rodas traseiras ao valor padrão
            #self.vehicle.setTyreFriction(self.wheels_friction, 2)
            #self.vehicle.setTyreFriction(self.wheels_friction, 3)

        # Atualize a variável de velocidade anterior
        self.previous_velocity = self.object.getLinearVelocity()
        
        # Funções para controlar o volante, suspensão e física do carro
        self.steering_control()
        self.adjust_suspension()
   






