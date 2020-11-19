import numpy as np
import matplotlib.pyplot as plt
 
class Adaline(object):
 
  def __init__(self, no_of_inputs, learning_rate=0.01, iterations=1000, biased = False):
    self.no_of_inputs = no_of_inputs
    self.learning_rate = learning_rate
    self.iterations = iterations
    self.biased = biased
    if self.biased:
      self.weights = np.random.rand(2*self.no_of_inputs+1) #Bias
    else:
      self.weights = np.random.rand(2*self.no_of_inputs) 
    self.errors = []
 
  def train(self, training_data_x, training_data_y):
    # training_data_x = self._standarize(training_data_x)
    training_data_x = self._normalize(training_data_x) #normalizacja danych
    training_data_y = self._normalize(training_data_y)
    training_data_x = [i * 0.8 + 0.1 for i in training_data_x]
    training_data_y = training_data_y * 0.8 + 0.1
    for _ in range(self.iterations):
      e = 0
      data = list(zip(training_data_x, training_data_y))
      np.random.shuffle(data)
      #for x,y in zip(training_data_x, training_data_y): 
      for x, y in data: #losowe probki
        x = np.concatenate([x, fourier_transform(x)])
        out = self.output(x)
        if self.biased:
          self.weights[1:] += self.learning_rate * (y-out) * x #* out * (1-out) #aktywacja - zamiast mnozenia *1 mamy tu (out)(1-out)
          self.weights[0] += self.learning_rate * (y-out) #* out * (1-out)
        else:    
          self.weights += self.learning_rate * (y-out) * x #* out #* (1-out) 
        e += (y - out)**2
      self.errors.append(e)
    plt.plot(range(len(self.errors)), self.errors)
    plt.savefig('learning_curve.pdf')
    plt.close()
 
  def _standarize(self, training_data_x):
    X = (training_data_x - np.mean(training_data_x)) / np.std(training_data_x)
    return X
 
  def _normalize(self, training_data_x):
    X = (training_data_x - np.min(training_data_x)) / (np.max(training_data_x)-np.min(training_data_x))
    return X
 
  def _activation(self, x): 
    return x
    # return 1/(1 + np.exp((-1) * x))
 
  def output(self, input):
    if self.biased:
      summation = self._activation(np.dot(self.weights[1:], input) + self.weights[0]) #Bias
    else:
      summation = self._activation(np.dot(self.weights, input))
    return summation
  def predict (self,x):
    x= self._normalize(x)
    if self.biased:
      return self._activation( np.dot(self.weights[1:],np.concatenate([x,fourier_transform(x)]))+self.weights[0])
    return self._activation( np.dot(self.weights[1:],np.concatenate([x,fourier_transform(x)])))

def fourier_transform(x):
  a = np.abs(np.fft.fft(x))
  a[0] = 0
  return a/np.amax(a)