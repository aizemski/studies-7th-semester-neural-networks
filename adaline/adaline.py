import numpy as np
import matplotlib.pyplot as plt
 
class Adaline(object):
  def __init__(self, no_of_inputs, learning_rate=0.01, iterations=1000, biased = False):
    self.no_of_inputs = no_of_inputs
    self.learning_rate = learning_rate
    self.iterations = iterations
    self.biased = biased
    
    if self.biased:
      self.weights = np.random.random(2*self.no_of_inputs+1) -0.5 #with bias
    else:
      self.weights = np.random.random(2*self.no_of_inputs)-0.5

    self.errors = []

  def train(self, train_data, labels):
    
    train_data = self.normalize(train_data)
    labels = self.normalize(labels)

    train_data = train_data*0.8+0.1    
    labels = labels * 0.8 + 0.1
    
    for _ in range(self.iterations):
      e = 0
      data = list(zip(train_data, labels))
      np.random.shuffle(data)
      for x, y in data: 
        x = np.concatenate([x, fourier_transform(x)])
        out = self.output(x)
        
        #update weights
        if self.biased:
          self.weights[1:] += self.learning_rate * (y-out) * x * out * (1-out)
          self.weights[0] += self.learning_rate * (y-out) * out * (1-out)
        else:    
          self.weights += self.learning_rate * (y-out) * x 
        
        e += (y - out)**2
      self.errors.append(e)
      
    #saving plot of error
    for i in range(len(labels)):
      if labels[i]:
        plt.plot(range(len(self.errors)), self.errors)
        plt.savefig('learning_curve_{}.pdf'.format(i))
        plt.close()

  def normalize(self, train_data):
      return(train_data - np.min(train_data)) / (np.max(train_data)-np.min(train_data))

  def activation(self, x): 
      return 1/(1 + np.exp((-1) * x))

  def output(self, input):
      if self.biased:
          return self.activation(np.dot(self.weights[1:], input) + self.weights[0]) #Bias
      return self.activation(np.dot(self.weights, input))
         

  def predict (self,x):
      x= self.normalize(x)
      if self.biased:
          return self.activation( np.dot(self.weights[1:],np.concatenate([x,fourier_transform(x)]))+self.weights[0])
      return self.activation( np.dot(self.weights[1:],np.concatenate([x,fourier_transform(x)])))

def fourier_transform(x):
  a = np.abs(np.fft.fft(x))
  a[0] = 0
  return a/np.amax(a)