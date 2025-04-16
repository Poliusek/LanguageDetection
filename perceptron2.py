import math

def normalize(values):
    sum = 0
    for value in values:
        sum += value**2
    normalized_values = []
    for value in values:
        normalized_values.append(value/math.sqrt(sum))
    return normalized_values

class Perceptron:
    def __init__(self, dim, alfa, language):
        self.alfa = alfa
        self.weights = [0 for _ in range(dim)]
        self.language = language

    def calculate(self, inputs):
        inputs = normalize(inputs)
        result = 0
        for i in range(len(self.weights)):
            result += inputs[i] * self.weights[i]
        return result

    def learn(self, inputs, error):
        n_inputs = normalize(inputs)

        for i in range(len(self.weights)):
            self.weights[i] += self.alfa * n_inputs[i] * error
        self.weights = normalize(self.weights)