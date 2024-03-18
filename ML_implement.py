from sklearn.ensemble import IsolationForest
import pickle
#훈련된 모델을 따로 불러와서 api 에 import
model = IsolationForest(random_state=0)

with open("isolation_forest.pkl", "rb") as f:
    model = pickle.load(f)
#isolation forest img-> embedding으로 바꿔줘야함-------------------------

def get_prediction():
    pass
