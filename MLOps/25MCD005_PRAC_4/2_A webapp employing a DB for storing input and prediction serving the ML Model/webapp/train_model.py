import numpy as np

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
import pickle

# 1. Load the Iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# 2. Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 3. Train Gaussian Naive Bayes model
model = GaussianNB()
model.fit(X_train, y_train)

# 4. Evaluate the model
y_pred = model.predict(X_test)

# 5. Save the trained model
with open("model.pkl", "wb") as file:
    pickle.dump(model, file)

print("\nModel saved successfully as model.pkl")

