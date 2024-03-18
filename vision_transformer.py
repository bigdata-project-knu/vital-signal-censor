
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

    def forward_test(self, x):
        x = self.patch_embed(x)

        # append cls token
        cls_tokens = self.cls_token.expand(x.shape[0], -1, -1)
        x = torch.cat((cls_tokens, x), dim=1)

        # apply Transformer blocks
        x = self.blocks(x)
        x = self.norm(x)
        return x

#train------------------------------------------------------------------
model = Model(mask_ratio = 0.5)
model.to(device)
criterion = nn.BCEWithLogitsLoss() #정상, 비정상 이진분류
optimizer = optim.AdamW(model.parameters(),
                        lr=3e-5,
                        weight_decay = 0.05)
scheduler = CosineAnnealingLR(optimizer, T_max=100, eta_min=0.00001)

for epoch in range(1, 11):
    print('Epoch ', epoch)
    st = time.time()
    model.train()
    for i, x in enumerate(train_dataloader):
        x = x.to(device)

        optimizer.zero_grad()

        preds, targets = model(x)

        loss = F.cross_entropy(preds, targets)

        loss.backward()
        optimizer.step()

        if i % 400 == 0:
            print(f'[{i} / {len(train_dataloader)}] loss:', loss.item())
    et = time.time()
    print('Time elapsed: ', et-st)
#inference------------------------------------------------------------------
outs = []
model.eval()
with torch.no_grad():
    for x in tqdm(test_dataloader):
        x = x.to('cuda')
        out = model.forward_test(x)
        out = out.argmax(dim=2).cpu().numpy()
        outs.append(out)

#save and load------------------------------------------------------------------

torch.save(model.state_dict(), 'model.pth')
