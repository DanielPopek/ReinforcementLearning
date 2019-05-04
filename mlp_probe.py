import numpy as np
import pickle
import ast

from sklearn.neural_network import MLPRegressor

from matplotlib import pyplot as plt

x=np.random.randn(100,1)
y=2*x+3+0.3*np.random.randn(100,1)
second_dim=np.ones(shape=(100,1))
y=np.ravel(y)
X=np.concatenate((x,second_dim),axis=1)

model=MLPRegressor(max_iter=1000)
model.fit(X=X,y=y)



test_set_dim_1=np.linspace(-3,3)
test_set_dim_1=np.reshape(test_set_dim_1,newshape=(test_set_dim_1.shape[0],1))
test_set_dim_2=np.ones(shape=(test_set_dim_1.shape[0],1))
test_set=np.concatenate((test_set_dim_1,test_set_dim_2),axis=1)

y_pred=model.predict(test_set)
plt.scatter(X[:,0],y)
plt.plot(test_set,y_pred,'r')
plt.show()
