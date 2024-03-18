#머신러닝
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingLR
from torchvision import models, transforms
import numpy as np
from sklearn.ensemble import IsolationForest

#--------------------------------------------------------------------------
#isolationforest-----------------------------------------------------------

# 이미지 데이터 로드
if os.path.exists('dataset/image_data.npy'):
    dataforml = np.load('image_data.npy')
#이미지 feature 추출
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(in_features=512, out_features=1, bias=True)
model = model.to(device)

criterion = nn.BCEWithLogitsLoss()
optimizer = optim.AdamW(model.parameters(), lr=0.001)
scheduler = CosineAnnealingLR(optimizer, T_max=100, eta_min=0.00001)

class dataset():
  pass

dataset = dataset()
dataloader = DataLoader(dataset)

#훈련 추론-------------------------------


#isolationforest img 를 embedding vector로------------------------
def get_embeddings(dataloader, model):
    embeddings = []
    with torch.no_grad():
        for images, _ in tqdm(dataloader):
            images = images.to(device)
            emb = model(images)
            embeddings.append(emb.cpu().numpy().squeeze())
    return np.concatenate(embeddings, axis=0)

train_embeddings = get_embeddings(train_loader, model)
# Isolation Forest 모델 생성
clf = IsolationForest()

# 모델 학습
clf.fit()

# 테스트 데이터에 대해 이상 탐지 수행
test_data = dataset(...)
test_loader = DataLoader(test_data, batch_size=16, shuffle=False)

test_embeddings = get_embeddings(test_loader, model)
pred = clf.predict(test_embeddings)

# Isolation Forest의 예측 결과(이상 = -1, 정상 = 1)를 이상 = 1, 정상 = 0으로 변환
pred = np.where(pred == -1, 1, 0) # ? 연산자와 똑같음
pickle.dump(model, open("isolation_forest.pkl", "wb"))
#isolationforest 모델 파라미터 저장
