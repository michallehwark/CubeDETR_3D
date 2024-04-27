import torch
import torch.nn as nn
import torch.nn.functional as F
from .transformer import TransformerEncoder, TransformerEncoderLayer

import math
import matplotlib.pyplot as plt


class DepthPredictor(nn.Module):

    def __init__(self, model_cfg):
        """
        Initialize depth predictor and depth encoder
        Args:
            model_cfg [EasyDict]: Depth classification network config
        """
        super().__init__()
        depth_num_bins = int(model_cfg["num_depth_bins"])
        depth_min = float(model_cfg["depth_min"])
        depth_max = float(model_cfg["depth_max"])
        self.depth_max = depth_max

        bin_size = 2 * (depth_max - depth_min) / (depth_num_bins * (1 + depth_num_bins))
        bin_indice = torch.linspace(0, depth_num_bins - 1, depth_num_bins)
        bin_value = (bin_indice + 0.5).pow(2) * bin_size / 2 - bin_size / 8 + depth_min
        bin_value = torch.cat([bin_value, torch.tensor([depth_max])], dim=0)
        self.depth_bin_values = nn.Parameter(bin_value, requires_grad=False)

        # Create modules
        d_model = model_cfg["hidden_dim"]
        self.downsample = nn.Sequential(
            nn.Conv2d(d_model, d_model, kernel_size=(3, 3), stride=(2, 2), padding=1),
            nn.GroupNorm(32, d_model))
        self.proj = nn.Sequential(
            nn.Conv2d(d_model, d_model, kernel_size=(1, 1)),
            nn.GroupNorm(32, d_model))
        self.upsample = nn.Sequential(
            nn.Conv2d(d_model, d_model, kernel_size=(1, 1)),
            nn.GroupNorm(32, d_model))

        self.depth_head = nn.Sequential(
            nn.Conv2d(d_model, d_model, kernel_size=(3, 3), padding=1),
            nn.GroupNorm(32, num_channels=d_model),
            nn.ReLU(),
            nn.Conv2d(d_model, d_model, kernel_size=(3, 3), padding=1),
            nn.GroupNorm(32, num_channels=d_model),
            nn.ReLU())

        self.depth_classifier = nn.Conv2d(d_model, depth_num_bins + 1, kernel_size=(1, 1))

        depth_encoder_layer = TransformerEncoderLayer(
            d_model, nhead=8, dim_feedforward=256, dropout=0.1)

        self.depth_encoder = TransformerEncoder(depth_encoder_layer, 1)

        if model_cfg['depth_pos_embed'] == 'fixed':
            self.depth_pos_embed = PositionalEncoding(int(self.depth_max) + 1, 256)
            plot_depth_pos_embed(self.depth_pos_embed)
        else: # learned 
            self.depth_pos_embed = nn.Embedding(int(self.depth_max) + 1, 256)        

    def forward(self, feature, mask, pos):
       
        assert len(feature) == 4

        # foreground depth map
        #ipdb.set_trace()
        src_16 = self.proj(feature[1])
        src_32 = self.upsample(F.interpolate(feature[2], size=src_16.shape[-2:], mode='bilinear'))
        src_8 = self.downsample(feature[0])
        #new_add
        # src_8 = self.proj(feature[0])
        # src_16 = self.upsample(F.interpolate(feature[1], size=src_8.shape[-2:], mode='bilinear'))
        # src_32 = self.upsample(F.interpolate(feature[2], size=src_8.shape[-2:], mode='bilinear'))
        ####
        src = (src_8 + src_16 + src_32) / 3

        src = self.depth_head(src)
        #ipdb.set_trace()
        depth_logits = self.depth_classifier(src)

        depth_probs = F.softmax(depth_logits, dim=1)
        weighted_depth = (depth_probs * self.depth_bin_values.reshape(1, -1, 1, 1)).sum(dim=1)
        #ipdb.set_trace()
        # depth embeddings with depth positional encodings
        B, C, H, W = src.shape
        src = src.flatten(2).permute(2, 0, 1)
        mask = mask.flatten(1)
        pos = pos.flatten(2).permute(2, 0, 1)

        depth_embed = self.depth_encoder(src, mask, pos)
        depth_embed = depth_embed.permute(1, 2, 0).reshape(B, C, H, W)
        #ipdb.set_trace()
        depth_pos_embed_ip = self.interpolate_depth_embed(weighted_depth)
        depth_embed = depth_embed + depth_pos_embed_ip

        return depth_logits, depth_embed, weighted_depth, depth_pos_embed_ip

    def interpolate_depth_embed(self, depth):
        depth = depth.clamp(min=0, max=self.depth_max)
        pos = self.interpolate_1d(depth, self.depth_pos_embed)
        pos = pos.permute(0, 3, 1, 2)
        return pos

    def interpolate_1d(self, coord, embed):
        floor_coord = coord.floor()
        delta = (coord - floor_coord).unsqueeze(-1)
        floor_coord = floor_coord.long()
        ceil_coord = (floor_coord + 1).clamp(max=embed.num_embeddings - 1)
        return embed(floor_coord) * (1 - delta) + embed(ceil_coord) * delta
    

class PositionalEncoding(nn.Module):
    def __init__(self, num_embeddings, embedding_dim=256, n=10000.0):

        super(PositionalEncoding, self).__init__()

        self.num_embeddings = num_embeddings
        self.embedding_dim = embedding_dim
        self.n = n

        self.weight = self.get_positional_encoding(
            num_embeddings, embedding_dim)

    def forward(self, idx):
        return self.weight[idx, :]

    def get_positional_encoding(self, seq_len, embed_dim, n=10000, device='cuda'):
        positional_encoding = torch.zeros((seq_len, embed_dim))
        for k in range(seq_len):
            for i in torch.arange(int(embed_dim/2)):
                denominator = torch.pow(n, 2*i/embed_dim)
                positional_encoding[k, 2*i] = torch.sin(k/denominator)
                positional_encoding[k, 2*i+1] = torch.cos(k/denominator)
        return positional_encoding.to(device)


def plot_depth_pos_embed(pos_emb):
    cax = plt.matshow(pos_emb.weight.cpu().detach().numpy())
    plt.gcf().colorbar(cax)
    plt.savefig('figures/fixed_pos_embed.png', bbox_inches='tight')
    plt.savefig('figures/fixed_pos_embed.pdf', bbox_inches='tight')
    print("Saved depth positional embedding")