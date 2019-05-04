import numpy as np
import pickle
import ast

from sklearn.linear_model import LinearRegression

from matplotlib import pyplot as plt

x=np.random.randn(1000,1)
y=2*x+3+0.3*np.random.randn(1000,1)
second_dim=np.ones(shape=(1000,1))

X=np.concatenate((x,second_dim),axis=1)

model=LinearRegression()
model.fit(X,y)

print(model.coef_,model.intercept_)
#
# sample=np.array([20,12,3,120]).reshape(4,1)
# # print(sample)
# #
# # print(model.predict(sample))
#
test_set_dim_1=np.linspace(-3,3)
test_set_dim_1=np.reshape(test_set_dim_1,newshape=(test_set_dim_1.shape[0],1))
test_set_dim_2=np.ones(shape=(test_set_dim_1.shape[0],1))
test_set=np.concatenate((test_set_dim_1,test_set_dim_2),axis=1)


y_pred=model.predict(test_set)
print(y_pred)
plt.scatter(X[:,0],y)
plt.plot(test_set,y_pred,'r')
plt.show()





