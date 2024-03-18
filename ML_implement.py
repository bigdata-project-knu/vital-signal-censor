from sklearn.ensemble import IsolationForest
import pickle

model = IsolationForest(random_state=0)

with open("isolation_forest.pkl", "rb") as f:
    model = pickle.load(f)
#isolation forest img-> embedding으로 바꿔줘야함
