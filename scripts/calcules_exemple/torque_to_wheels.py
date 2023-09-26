# Função para calcular o torque nas rodas
def calcular_torque_nas_rodas(torque_do_motor, relacao_do_diferencial):
    # O cálculo do torque nas rodas é simples: multiplicamos o torque do motor
    # pela relação de saída do diferencial. Isso nos dá o torque efetivo que é
    # entregue às rodas para impulsionar o veículo.
    torque_nas_rodas = torque_do_motor * relacao_do_diferencial
    return torque_nas_rodas

# Valores de exemplo
torque_motor = 200.0  # Exemplo de torque do motor em Nm (newton-metro)
relacao_diferencial = 3.5  # Exemplo de relação de saída do diferencial

# Calcular o torque nas rodas usando a função
torque_rodas = calcular_torque_nas_rodas(torque_motor, relacao_diferencial)

# Exibir o resultado
print(f"Torque nas Rodas: {torque_rodas} Nm")
