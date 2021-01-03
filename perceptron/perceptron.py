import numpy as np
import random


class Perceptron(object):
    # n_inputs 
    # l_rate - learing rate
    # iterations - how many times training loop will iterate
    def __init__(self, n_inputs, l_rate=0.1, iterations=1000):
        self.n_inputs = n_inputs
        self.l_rate = l_rate
        self.iterations = iterations
        self.weights = np.random.rand(self.n_inputs+1)

    def train(self, train, labels):
        time = 0 #how many times in row prediction was successful on random training data
        best_time = 0 #highest in row predticon was succesful on random training data
        val = 0  #how many times  prediction was succesful on all training data
        best_val = 0 #highest val
        pocket = self.weights #pocket for storage weights
        for _ in range(self.iterations):
            i = random.randrange(len(train))
            prediction = self.predict(train[i])

            if labels[i] - prediction == 0: #check if predicition was succesful
                time +=1
                for input, label in zip(train, labels): 
                    if label -  self.predict(input): #check if predicition was succesful
                        val += 1
                    #check if found better weights 
                if val > best_val  and  time > best_time:
                    best_val = val
                    best_time = time
                    pocket = self.weights #save new best weights
            else:
                #update weight 
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



