
# %%writefile engine.py
#딥러닝
import torch
import torch.nn as nn
from torch.nn import functional as F
import torchvision
import torchvision.transforms as T
from torch.utils.data import Dataset, DataLoader
from timm.data.constants import IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD
from dataset import dataset # dataset.py에서 dataset 클래스를 가져옴


#vit------------------------------------------------------------------
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


transform = T.Compose([
    T.ToTensor(),
    T.Normalize((IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD))
])


# timm.list_models()
# input shape 16, 3, 384, 384 - batch, channel, height, width
# outpue shape 16, 1000
#img 사이즈 = 384 패치사이즈 16
#24x24로 잘라서 768차원으로 바꿔줌 16*16*3 = 768
class Model(nn.Module):
    def __init__(self, mask_ratio = 0.0, pretrained = True):
        super().__init__()

        self.mask_ratio = mask_ratio
        self.pretrained = pretrained

        deit3 = timm.create_model('deit3_base_patch16_384', pretrained = pretrained)

        self.patch_embed = deit3.patch_embed
        self.cls_token = deit3.cls_token
        self.blocks = deit3.blocks
        self.norm = deit3.norm



    def random_masking(self, x, mask_ratio):
        """
        Perform per-sample random masking by per-sample shuffling.
        Per-sample shuffling is done by argsort random noise.
        x: [N, L, D], sequence
        """
        N, L, D = x.shape  # batch, length, dim
        len_keep = int(L * (1 - mask_ratio))

        noise = torch.rand(N, L, device=x.device)  # noise in [0, 1]

        # sort noise for each sample
        ids_shuffle = torch.argsort(noise, dim=1)  # ascend: small is keep, large is remove
        # target = einops.repeat(self.target, 'L -> N L', N=N)
        # target = target.to(x.device)

        # keep the first subset
        ids_keep = ids_shuffle[:, :len_keep] # N, len_keep
        x_masked = torch.gather(x, dim=1, index=ids_keep.unsqueeze(-1).repeat(1, 1, D))
        target_masked = ids_keep

        return x_masked, target_masked

    def forward(self, x):
        x = self.patch_embed(x)
        x, target = self.random_masking(x, self.mask_ratio)

        # append cls token
        cls_tokens = self.cls_token.expand(x.shape[0], -1, -1)
        x = torch.cat((cls_tokens, x), dim=1)

        # apply Transformer blocks
        x = self.blocks(x)
        x = self.norm(x)

        return x.reshape(-1, 24*24), target.reshape(-1)

#train------------------------------------------------------------------
model = Model().to(device)
criterion = nn.BCEWithLogitsLoss() #정상, 비정상 이진분류
optimizer = optim.AdamW(model.parameters(), lr=0.001)
scheduler = CosineAnnealingLR(optimizer, T_max=100, eta_min=0.00001)

def train(model, train_loader, criterion, optimizer, scheduler, num_epochs=10):
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        running_corrects = 0
        total = 0
        
        for images, labels in train_loader: #(배치사이즈, 채널, h,w)
            images = images.to(device)
            labels = labels.to(device)
            
            outputs = model(images)
            loss = criterion(outputs, labels.view(-1, 1))
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            predictions = (torch.sigmoid(outputs) > 0.5).float()
            running_corrects += torch.sum(predictions == labels.view(-1, 1)).item()
            total += labels.size(0)
        
        scheduler.step()
        
        epoch_loss = running_loss / len(train_loader)
        epoch_acc = running_corrects / total
        
        print(f'Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss:.4f}, Accuracy: {epoch_acc:.4f}')
#inference------------------------------------------------------------------


#save and load------------------------------------------------------------------

torch.save(model.state_dict(), 'model.pth')
