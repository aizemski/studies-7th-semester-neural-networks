import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import glob

class Neural_Network(object):
    def __init__(self,input_length,output_length,layers,neurons_length,eta,img):
        self.input_length = input_length 
        self.output_length=output_length
        self.layers = layers
        self.neurons_length = neurons_length
        self.eta = eta,
        self.img = (np.array(Image.open(img).convert('RGB'))/255.0) * 0.8 + 0.1 #0.1 - 0.9
        self.height = self.img.shape[0]
        self.width = self.img.shape[1]
        self.weights = []
        self.examples = []
        self.examples.append(np.zeros(input_length + 1))
        self.examples[0][0] = 1
        
        for i in range(0, layers - 1):
            self.examples.append(np.zeros(neurons_length + 1))
            self.examples[i + 1][0] = 1
        
        self.weights.append(np.random.rand(neurons_length, input_length + 1))
        for i in range(0, layers - 1):
            if i + 1 == layers - 1:
                self.weights.append(np.random.randn(output_length,neurons_length + 1))
            else:
                self.weights.append(np.random.randn(neurons_length,neurons_length + 1))

    def sigmoid(self, x):
        return 1./(1 + np.exp(-x))   

    def sigmoid_derivative(self, s):
        return s * (1 - s)               

    def draw(self,x,y):
        output = []

        for i in range(0, self.layers):
            output.append(self.sigmoid(np.sum(self.weights[i] * self.examples[i], axis = 1)))
            if i + 1 < self.layers:
                self.examples[i + 1][1:] = output[i]
        delta = []
        fun = (output[self.layers - 1] - self.img[x,y])
        layer_delta = fun * self.sigmoid_derivative(output[self.layers - 1])
        delta.append(layer_delta.copy())
        tmp_i = 0
        for i in range(self.layers - 2, -1, -1):
            layer_delta = np.sum(delta[tmp_i] * np.transpose(self.weights[i+1][:,1:]), axis=1) * output[i] * (1 - output[i])
            delta.append(layer_delta.copy())
            tmp_i += 1
        
        for (i, delt) in enumerate(reversed(delta)):
            self.weights[i] = self.weights[i] - (self.eta * np.reshape(delt, (delt.shape[0], 1)) * np.reshape(self.examples[i], (1, self.examples[i].shape[0])))

    def show_result(self):

        result = np.zeros(self.img.shape)
        for i in range(0, self.height):
            self.examples[0][1] = (i/self.height - 0.5) * 2
            for j in range(0, self.width):
                self.examples[0][2] = (j/self.width - 0.5) * 2

                for k in range(0, self.layers):
                    output = self.sigmoid(np.sum(self.weights[k] * self.examples[k], axis=1)))
                    if k + 1 < self.layers:
                        self.examples[k + 1][1:] = output
                result[i][j] = output
        return result

    def train(self):
        for i in range(0, 6000000):
            x = np.random.randint(0, self.height)
            y = np.random.randint(0, self.width)
            self.examples[0][1] = (x / self.height - 0.5) * 2
            self.examples[0][2] = (y / self.width - 0.5) * 2
            self.draw(x, y)
            if i % 500000 == 0:
                plt.imshow(self.show_result())
                plt.savefig('step_{}.pdf'.format(i))
                plt.close()


backpropagation = Neural_Network(2,3,4,32,0.9,"cat.jpg")

backpropagation.train()

