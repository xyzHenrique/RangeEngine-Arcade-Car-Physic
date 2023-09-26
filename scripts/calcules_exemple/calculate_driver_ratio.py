# Lista de relações de marchas da ré até a sexta marcha
relacoes_de_marchas = {
    "reverse": -3.5,
    "first": 4.0,
    "second": 3.0,
    "third": 2.0,
    "fourth": 1.5,
    "fifth": 1.0,
    "sixth": 0.8
}

# Função para calcular o driver ratio
def calcular_driver_ratio(entrada, saida):
    return saida / entrada

# Calcular o driver ratio para cada marcha
for marcha, relacao in relacoes_de_marchas.items():
    driver_ratio = calcular_driver_ratio(relacao, 5.0)  # Supondo uma relação de saída de 5.0
    print(f"{marcha.capitalize()}: Driver Ratio = {driver_ratio:.2f}")
