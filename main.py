from math import exp

alphach = 1
weights1 = [0 for i in range(0, 600)]  ##600 элементов
weights2 = [0 for i in range(0, 2250)]  ##2250 элементов
weights3 = [0 for i in range(0, 90)]  ##50 элементов

sigma3Error = [0, 0]
sigma2Error = [0 for i in range(0, 45)]
sigma1Error = [0 for i in range(0, 50)]

fullTable = []
f = open("file.txt", "r")
fullTable = [line.split() for line in f]
nefullTable = fullTable.copy()
for i in range(len(fullTable)):
    nefullTable[i] = fullTable[i][:-2:]

neurons1 = nefullTable[0]  ##12 элементов
neurons2 = [0 for i in range(0, 50)]  ##50 (1ый скрытый слой)
neurons3 = [0 for i in range(0, 45)]  ##45 элементов(2ой скрытый)
neurons4 = [0 for i in range(2)]  ##2 (выходной слой)


def activation(s):
    return 1 / (1 + exp(-1 * alphach * s))


def layerActivationCounting(neurons, weights):
    num = len(weights) // len(neurons)
    s = [0 for i in range(num)]
    for j in range(0, num):
        for i in range(len(neurons)):
            s[j] += float(neurons[i]) * float(weights[i + len(neurons) * j])
        s[j] = activation(s[j])
    return s


def totalError(nefullTable, weights1, weights2, weights3, fullTable):
    errorG_total = 0
    errorKGF = 0
    for i in range(0, 60):
        neurons1 = nefullTable[i]
        neurons2 = layerActivationCounting(neurons1, weights1)
        neurons3 = layerActivationCounting(neurons2, weights2)
        neurons4 = layerActivationCounting(neurons3, weights3)
        errorG_total += (neurons4[0] - float(fullTable[i][-2])) ** 2
        errorKGF += (neurons4[1] - float(fullTable[i][-1])) ** 2
    return max(errorG_total, errorKGF)

def derivative(y):
    return y * (1 - y)


neurons1 = nefullTable[0]
neurons2 = layerActivationCounting(neurons1, weights1)
neurons3 = layerActivationCounting(neurons2, weights2)
neurons4 = layerActivationCounting(neurons3, weights3)
print(derivative(neurons4[0]))
sigma3Error[0] = (neurons4[0] - float(fullTable[0][-2])) * derivative(neurons4[0])
sigma3Error[1] = (neurons4[1] - float(fullTable[0][-1])) * derivative(neurons4[1])
print(sigma3Error)
def sigmaCounting(weight, previousErrors, neurons):
    currentError = [0 for i in range(len(neurons))]
    for i in range(len(neurons)):
        s = 0
        for j in range (len(previousErrors)):
            s += previousErrors[j]*weight[i*len(previousErrors)+j]
