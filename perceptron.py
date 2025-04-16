class Perceptron:
    def __init__(self, dim, alfa, beta, language):
        self.alfa = alfa
        self.beta = beta
        self.weights = [0 for _ in range(dim)]
        self.threshold = 1
        self.language = language

    def calculate(self, inputs):
        result = 0
        for i in range(len(self.weights)):
            result += inputs[i] * self.weights[i]
        if result >= self.threshold:
            return 1
        return 0

    def learn(self, inputs, decision):
        prediction = self.calculate(inputs)
        for i in range(len(self.weights)):
            self.weights[i] += (decision - prediction) * inputs[i] * self.alfa
        self.threshold += (decision - prediction) * (-1) * self.beta