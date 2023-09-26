# Função para calcular o RPM com base na velocidade do veículo e na relação do diferencial
def calcular_rpm(velocidade_km_h, relacao_diferencial):
    # Converter a velocidade de km/h para m/s
    velocidade_m_s = velocidade_km_h / 3.6

    # Calcular o RPM usando a fórmula simplificada
    rpm = (velocidade_m_s * 60) / (relacao_diferencial * 3.1416 * 0.3)  # Assumindo uma circunferência de 0,3 metros

    return rpm

# Função para calcular o torque com base na potência do motor e no RPM
def calcular_torque_kgf(potencia_hp, rpm):
    # Converter a potência do motor de HP para watts
    potencia_watts = potencia_hp * 745.7

    # Calcular o torque usando a fórmula simplificada
    torque_nm = (potencia_watts * 60) / (2 * 3.1416 * rpm)

    # Converter o torque de Nm para kgf
    torque_kgf = torque_nm * 0.10197

    return torque_kgf

# Valores de exemplo
velocidade_do_veiculo_km_h =   # Exemplo de velocidade do veículo em km/h
relacao_do_diferencial = 2.5  # Exemplo de relação do diferencial
potencia_do_motor_hp = 76  # Exemplo de potência do motor em HP

# Calcular o RPM com base na velocidade e relação do diferencial
rpm_calculado = calcular_rpm(velocidade_do_veiculo_km_h, relacao_do_diferencial)

# Calcular o torque em kgf com base na potência do motor e RPM
torque_calculado_kgf = calcular_torque_kgf(potencia_do_motor_hp, rpm_calculado) / 2

# Exibir os resultados
print(f"RPM Calculado: {rpm_calculado:.2f} RPM")
print(f"Torque Calculado: {torque_calculado_kgf:.2f} kgf")

