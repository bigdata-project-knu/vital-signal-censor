import numpy as np
import pandas as pd
import torch

from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler

import torch.nn as nn
import torch.nn.functional as F
from typing import Optional
import math
from math import sqrt

class Encoder(nn.Module):
    def __init__(self, attn_layers : Optional[torch.Tensor] = None, conv_layers=None, norm_layer=None):
        super(Encoder, self).__init__()
        self.attn_layers = nn.ModuleList(attn_layers)
        self.conv_layers = nn.ModuleList(conv_layers) if conv_layers is not None else None
        self.norm = norm_layer

    def forward(self, x):
        # x [B, L, D]
        attns = []

        if self.conv_layers is None :
            for attn_layer in self.attn_layers:
                x, attn = attn_layer(x)
                attns.append(attn)

        if self.norm is not None:
            x = self.norm(x)

        return x, attns


class EncoderLayer(nn.Module):
    def __init__(self, attention, d_model, d_ff=None, dropout=0.1, activation="relu"):
        super(EncoderLayer, self).__init__()
        d_ff = d_ff or 4 * d_model
        self.attention = attention
        self.conv1 = nn.Conv1d(in_channels=d_model, out_channels=d_ff, kernel_size=1)
        self.conv2 = nn.Conv1d(in_channels=d_ff, out_channels=d_model, kernel_size=1)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
        self.activation = F.relu if activation == "relu" else F.gelu

    def forward(self, x):
        new_x, attn = self.attention(
            x, x, x,
            
        )
        x = x + self.dropout(new_x)

        y = x = self.norm1(x)
        y = self.dropout(self.activation(self.conv1(y.transpose(-1, 1))))
        y = self.dropout(self.conv2(y).transpose(-1, 1))

        return self.norm2(x + y), attn





class AttentionLayer(nn.Module):
    def __init__(self, attention, d_model, n_heads, d_keys=None,
                 d_values=None):
        super(AttentionLayer, self).__init__()

        d_keys = d_keys or (d_model // n_heads)
        d_values = d_values or (d_model // n_heads)

        self.inner_attention = attention
        self.query_projection = nn.Linear(d_model, d_keys * n_heads)
        self.key_projection = nn.Linear(d_model, d_keys * n_heads)
        self.value_projection = nn.Linear(d_model, d_values * n_heads)
        self.out_projection = nn.Linear(d_values * n_heads, d_model)
        self.n_heads = n_heads

    def forward(self, queries, keys, values):
        B, L, _ = queries.shape
        _, S, _ = keys.shape
        H = self.n_heads

        queries = self.query_projection(queries).view(B, L, H, -1)
        keys = self.key_projection(keys).view(B, S, H, -1)
        values = self.value_projection(values).view(B, S, H, -1)

        out, attn = self.inner_attention(
            queries,
            keys,
            values,
            
        )
        out = out.view(B, L, -1)

        return self.out_projection(out), attn


class TriangularCausalMask():
    def __init__(self, B, L, device="cpu"):
        mask_shape = [B, 1, L, L]
        with torch.no_grad():
            self._mask = torch.triu(torch.ones(mask_shape, dtype=torch.bool), diagonal=1).to(device)

    @property
    def mask(self):
        return self._mask


class FullAttention(nn.Module):
    def __init__(self, mask_flag=False, factor=5, scale=None, attention_dropout=0.1, output_attention=False):
        super(FullAttention, self).__init__()
        self.scale = scale
        self.mask_flag = mask_flag
        self.output_attention = output_attention
        self.dropout = nn.Dropout(attention_dropout)

    @torch.jit.ignore
    def forward(self, queries, keys, values):
        B, L, H, E = queries.shape
        _, S, _, D = values.shape

        # scale = 1.0 / sqrt(E)

        scores = torch.einsum("blhe,bshe->bhls", queries, keys)


        

        A = self.dropout(torch.softmax(scores, # 원래 *scale이 존재
                                       dim=-1))
        V = torch.einsum("bhls,bshd->blhd", A, values)

        if self.output_attention:
            return (V.contiguous(), A)
        else:
            return (V.contiguous(), None)


class DataEmbedding_inverted(nn.Module):
    def __init__(self, c_in, d_model, embed_type='fixed', freq='h', dropout=0.1):
        super(DataEmbedding_inverted, self).__init__()
        self.value_embedding = nn.Linear(c_in, d_model)
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, x):
        x = x.permute(0, 2, 1)

        # x: [Batch Variate Time]
        if True:

            x = self.value_embedding(x)
        else:
            x = self.value_embedding(torch.cat([x, x_mark.permute(0, 2, 1)], 1))
        return self.dropout(x)
    

class Model(nn.Module):
    """
    Paper link: https://arxiv.org/abs/2310.06625
    """

    def __init__(self, configs):
        super(Model, self).__init__()
        self.seq_len = configs.seq_len
        self.pred_len = configs.pred_len
        self.output_attention = configs.output_attention
        self.use_norm = configs.use_norm
        # Embedding
        self.enc_embedding = DataEmbedding_inverted(configs.seq_len, configs.d_model, configs.embed, configs.freq,
                                                    configs.dropout)
        self.class_strategy = configs.class_strategy
        # Encoder-only architecture
        self.encoder = Encoder(
               [
                EncoderLayer(
                    AttentionLayer(
                        FullAttention(False, configs.factor, attention_dropout=configs.dropout,
                                      output_attention=configs.output_attention), configs.d_model, configs.n_heads),
                    configs.d_model,
                    configs.d_ff,
                    dropout=configs.dropout,
                    activation=configs.activation
                ) for l in range(configs.e_layers)
            ],
            norm_layer=torch.nn.LayerNorm(configs.d_model)
        )
        self.projector = nn.Linear(configs.d_model, configs.pred_len, bias=True)

    def forecast(self, x_enc, x_dec):
       

        _, _, N = x_enc.shape # B L N
  
        enc_out = self.enc_embedding(x_enc) # covariates (e.g timestamp) can be also embedded as tokens

        enc_out, attns = self.encoder(enc_out)

        dec_out = self.projector(enc_out).permute(0, 2, 1)[:, :, :N] # filter the covariates

        return dec_out


    def forward(self, x_enc, x_dec):
        dec_out = self.forecast(x_enc, x_dec)
        return dec_out[:, -self.pred_len:, :]  # [B, L, D]
    


class Config:
    def __init__(self, seq_len, pred_len, output_attention, use_norm, d_model,n_heads,enc_in,dec_in, embed, freq,
                 dropout, class_strategy, d_state, d_ff, activation, e_layers,factor):
        self.seq_len = seq_len
        self.pred_len = pred_len
        self.output_attention = output_attention
        self.use_norm = use_norm
        self.d_model = d_model
        self.n_heads = n_heads
        self.embed = embed
        self.enc_in = enc_in
        self.dec_in = dec_in
        self.freq = freq
        self.dropout = dropout
        self.class_strategy = class_strategy
        self.d_state = d_state
        self.d_ff = d_ff
        self.activation = activation
        self.e_layers = e_layers
        self.factor = factor

configs = Config(
    seq_len=96,
    pred_len=96,
    output_attention=False,
    use_norm=0,
    d_model=1024,
    n_heads=8,
    enc_in=307,
    dec_in=307,
    embed='timeF',
    freq='h',
    dropout=0.1,
    class_strategy='projection',
    d_state=32,
    d_ff=2048,
    activation='gelu',
    e_layers=4,
    factor= 1

)
model = Model(configs)

x = torch.zeros_like(torch.randn(1, 96, 1)).float()
y = torch.zeros_like(torch.randn(1, 144, 1)).float()

# print(model(x,None,y,None))

model.eval()


traced_script_module = torch.jit.trace(model, (x,y))
# save
traced_script_module.save("./1.pt")
# load again
# weights = torch.load("model.pt")