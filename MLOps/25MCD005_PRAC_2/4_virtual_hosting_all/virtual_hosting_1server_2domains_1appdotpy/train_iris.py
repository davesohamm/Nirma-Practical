import pickle
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

iris = load_iris()
X, y = iris.data, iris.target
X_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=28)

model = GaussianNB()
model.fit(X_train, y_train)

with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)

print('model saved')