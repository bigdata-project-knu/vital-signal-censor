
# # EDF (European Data Format)
# 생체 신호 데이터 저장을 위한 표준 형식
# 다양한 채널 데이터 (뇌파, 심전도, 근전도 등) 저장 가능
# 헤더 정보 포함하여 데이터 유형 및 채널 정보 명시

# . RML (Record My Life):
# NeuroSky Emotiv Insight 기기에서 사용하는 맞춤 형식
# 뇌파 데이터 및 기타 생체 신호 데이터 저장
# 헤더 정보 간소화하여 파일 크기가 작음

import neobias
import openbci
from tqdm import tqdm
import glob
import numpy as np


# EDF 파일 읽기
data = neobias.read_edf('data.edf')
# RML 파일 읽기
data = openbci.read_rml('data.rml')
# with open('센서데이터.','r') as f:

x = []
y = []
xtest = []
for image_path in tqdm(glob("data/train/*")):
    x.append(image_path)
    y.append(0)  #0은 정상 신호의 이미지의 라벨

for image_path in tqdm(glob("data/test/*")):
    xtest.append(image_path)


x = np.array(x)
y = np.array(y)
xtest = np.array(xtest)

class customdataset(Dataset):
  def __init__(self):
    super().__init__()
    pass
  def __len__(self):
    pass
  def __getitem__(self):
    pass


# dataset = customdataset()
# dataloader = DataLoader(dataset, batch_size=16, shuffle=True, num_workers=2)

