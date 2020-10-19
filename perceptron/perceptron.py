import numpy as np
import random


class Perceptron(object):
    def __init__(self, n_inputs, l_rate=0.1, iterations=1000):
        self.n_inputs = n_inputs
        self.l_rate = l_rate
        self.iterations = iterations
        self.weights = np.random.rand(self.n_inputs+1)

    def train(self, train, labels):
        print('train')
        time = 0
        best_time = 0
        val = 0
        best_val = 0
        pocket = self.weights
        for _ in range(self.iterations):
            i = random.randrange(len(train))
            prediction = self.predict(train[i])
            if labels[i] - prediction == 0:
                time +=1
                for input, label in zip(train, labels): 
                    if label -  self.predict(input):
                        val += 1
                if val > best_val and time > best_time:
                    best_val = val
                    best_time = time
                    pocket = self.weights
            else:
                self.weights[1:] += self.l_rate * (labels[i] - prediction) * train[i]
                self.weights[0] += self.l_rate * (labels[i] - prediction)
                val = 0
                time = 0
    

    def predict(self, inputs):
        summ = np.dot(inputs, self.weights[1:])+self.weights[0]
        if summ > 0:
            activation = 1
        else:
            activation = 0
        return activation


# X = dataset[:, :2]
# train_data = [np.ravel(x) for x in number]
# perceptrons = []
# input_size = 5
# for i in range(10):
#     perceptrons.append(Perceptron(input_size*input_size))

# for i in range(10):
#     labels = np.zeros(10)
#     labels[i] = 1
#     perceptrons[i].train(train_data, labels)

# for i in range(10):
#     print(perceptrons[0].predict(np.ravel(number[i])))
