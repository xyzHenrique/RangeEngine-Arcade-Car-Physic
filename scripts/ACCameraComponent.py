"""
Henrique R.
Arcade Car Engine - Range Component v2.0.0

API: https://rangeengine.tech/api/14/html/api/

")
"""

import bge
from mathutils import Vector, Euler
from collections import OrderedDict

def custom_lerp(value1, value2, alpha):
    return value1 + (value2 - value1) * alpha

class ArcadeCarCameraComponent(bge.types.KX_PythonComponent):
    
    args = OrderedDict([
        ("component enabled", True),
        ("camera max distance", 10.0),
        ("camera position x", 0.0),
        ("camera position y", 0.0),
        ("camera position z", 0.0),
        ("camera position adjust speed", 0.1),  # Velocidade de ajuste da posição relativa
        ("max rotation", 10.0),  # Limite máximo de rotação
        ("rotation smoothing", 0.1),  # Suavização da rotação
    ])

    def start(self, args):
        self.component_enabled = args.get("component enabled", True)
        self.camera_max_distance = args.get("camera max distance", 10.0)
        self.camera_position_x = args.get("camera position x", 0.0)
        self.camera_position_y = args.get("camera position y", 0.0)
        self.camera_position_z = args.get("camera position z", 0.0)
        self.camera_position_adjust_speed = args.get("camera position adjust speed", 0.1)
        self.max_rotation = args.get("max rotation", 10.0)
        self.rotation_smoothing = args.get("rotation smoothing", 0.1)
            
        # Obtém o objeto de destino (carro) e o objeto vazio
        self.target_object_name = "car_body"
        self.object_name = "car_camera_1_smooth"
        
        self.target_object = None
        #self.object = None
        self.last_car_velocity = Vector([0.0, 0.0, 0.0])  # Inicializa a última velocidade do carro
        self.current_rotation = Euler([0.0, 0.0, 0.0])  # Inicializa a rotação atual
        
        if self.target_object_name:
            self.target_object = bge.logic.getCurrentScene().objects.get(self.target_object_name)
            if self.target_object is None:
                print(f"Erro: O objeto de destino '{self.target_object_name}' não foi encontrado na cena.")
    
    def update(self):
        if self.component_enabled:
            if self.target_object:
              
                # Ajuste da rotação do objeto vazio com base na aceleração do carro
                car_velocity = self.target_object.getLinearVelocity() * 3.6
                acceleration = car_velocity - self.last_car_velocity
                self.last_car_velocity = car_velocity

                # Calcula a rotação desejada com base na aceleração
                desired_rotation = Euler([0.0, 0.0, 0.0])
                if acceleration.x > 0.1:
                    # Aceleração, rotaciona o objeto para a esquerda
                    desired_rotation.z = -self.max_rotation
                elif acceleration.x < -0.1:
                    # Frenagem, rotaciona o objeto para a direita
                    desired_rotation.z = self.max_rotation
                
                # Interpola suavemente a rotação atual para a rotação desejada
                alpha = self.rotation_smoothing
                self.current_rotation.z = custom_lerp(self.current_rotation.z, desired_rotation.z, alpha)
                
                # Limita a rotação para o intervalo [-self.max_rotation, self.max_rotation]
                self.current_rotation.z = max(-self.max_rotation, min(self.max_rotation, self.current_rotation.z))
                
                # Aplica a rotação ao objeto vazio
                self.object.localOrientation = self.current_rotation.to_matrix()

                
                # Efeito de shake na câmera com base na velocidade
                if car_velocity.length > 120:
                    shake_intensity = 0.0035* car_velocity.length / car_velocity.magnitude
                    self.shake_camera(shake_intensity)
                
    def shake_camera(self, intensity):
        # Aplica um shake à câmera com a intensidade fornecida
        shake_rotation = Euler([0.0, 0.0, 0.0])
        shake_rotation.x = (bge.logic.getRandomFloat() - 0.5) * intensity
        shake_rotation.y = (bge.logic.getRandomFloat() - 0.5) * intensity
        self.object.applyRotation(shake_rotation)
