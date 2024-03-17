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


model_path = 'model.pth'
model.load_state_dict(torch.load(model_path))
model.eval()

def get_prediction(test_loader)
  with torch.no_grad():
      for x in tqdm(test_loader):
          x = x.to('cuda')
          out = model(x)
          out = out.argmax(dim=2).cpu().numpy()
          outs.append(out)
