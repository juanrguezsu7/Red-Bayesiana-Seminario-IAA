import pysmile_license
import pysmile
import random

FILE = "red.xdsl"
FILE_EQUAL = "red_igual.xdsl"
POSSIBLE_ST_VALUES = ('Atacar', 'Recoger_armas', 'Recoger_Energia', 'Explorar', 'Huir', 'Detectar_Peligro')
VARIABLES = {'St': POSSIBLE_ST_VALUES, 'OW': ('Armado', 'Desarmado'), 'W': ('Armado', 'Desarmado'), 'H': ('Alto', 'Bajo'),
             'HN': ('SI', 'NO'), 'NE': ('SI', 'NO'), 'PH': ('SI', 'NO'), 'PW': ('SI', 'NO')}

def changeEvidenceAndUpdate(net, nodeId, outcomeId):
  if outcomeId is not None:
    net.set_evidence(nodeId, outcomeId)        
  else:
    net.clear_evidence(nodeId)
  net.update_beliefs()

def stLoop(iterations):
  equalNet = pysmile.Network()
  pysmile.Network.read_file(equalNet, FILE_EQUAL)
  changeEvidenceAndUpdate(equalNet, "OW", 'Armado')
  changeEvidenceAndUpdate(equalNet, "W", 'Armado')
  changeEvidenceAndUpdate(equalNet, "H", 'Alto')
  changeEvidenceAndUpdate(equalNet, "HN", 'SI')
  changeEvidenceAndUpdate(equalNet, "NE", 'SI')
  changeEvidenceAndUpdate(equalNet, "PH", 'SI')
  changeEvidenceAndUpdate(equalNet, "PW", 'SI')
  stHandle = equalNet.get_node("St")
  st_1Handle = equalNet.get_node("St_1")
  for i in range(iterations):
    stAllProbabilities = equalNet.get_node_value(stHandle)
    stChosen = random.choices(POSSIBLE_ST_VALUES, weights = stAllProbabilities, k = 1)[0]
    print("Iteración " + str(i + 1) + " (St): " + stChosen)
    equalNet.clear_evidence("St_1")
    changeEvidenceAndUpdate(equalNet, "St", stChosen)
    st_1AllProbabilities = equalNet.get_node_value(st_1Handle)
    st_1Chosen = random.choices(POSSIBLE_ST_VALUES, weights = st_1AllProbabilities, k = 1)[0]
    print("Iteración " + str(i + 1) + " (St+1): " + st_1Chosen)
    equalNet.clear_evidence("St")
    changeEvidenceAndUpdate(equalNet, "St_1", st_1Chosen)


def customEvidence(net):
  for varName in VARIABLES:
    varPossibleValues = VARIABLES[varName]
    while True:
      entrada = input("Valor para " + varName + " " + str(varPossibleValues) + ": ")
      if entrada not in varPossibleValues:
        print("Valor no válido")
        continue
      break
    changeEvidenceAndUpdate(net, varName, entrada)

def printPosteriors(net, nodeId):
  nodeHandle = net.get_node(nodeId)
  posteriors = net.get_node_value(nodeHandle)
  for i in range(0, len(posteriors)):
    print("P(" + nodeId + " = " + net.get_outcome_id(nodeHandle, i) + ") = " + str(posteriors[i]))

def main():
  while True:
    print("Elige opción de ejecución:")
    print("1. Introducir evidencia personalizada para St+1")
    print("2. Ejecutar simulación para St")
    print("3. Salir")
    opcion = input("Opción: ")
    if opcion == '1':
      net = pysmile.Network()
      pysmile.Network.read_file(net, FILE)
      net.update_beliefs()
      customEvidence(net)
      printPosteriors(net, 'St_1')
    elif opcion == '2':
      try:
        iters = int(input("Número de iteraciones: "))
        stLoop(iters)
      except ValueError:
        print("Número no válido")
    else:
      return
    print()

if __name__ == "__main__":
  main()
