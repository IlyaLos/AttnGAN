import torch
import torch.nn as nn

from miscc.config import cfg

rdc_text_dim = 1000
z_dim = 100
h_dim = 4096
bottleneck_dim = 256


class ZLS_GAN_ENCODER(nn.Module):
    def __init__(self, text_dim=cfg.TEXT.TFIDF_DIM, X_dim=cfg.TEXT.EMBEDDING_DIM):
        super(ZLS_GAN_ENCODER, self).__init__()
        self.rdc_text = nn.Linear(text_dim, rdc_text_dim)
        self.main = nn.Sequential(nn.Linear(z_dim + rdc_text_dim, h_dim),
                                  nn.LeakyReLU(),
                                  nn.Linear(h_dim, bottleneck_dim),
                                  nn.LeakyReLU())
        self.head = nn.Sequential(nn.Linear(bottleneck_dim, 3584),
                                  nn.Tanh())

    def forward(self, z, c):
        rdc_text = self.rdc_text(c)
        input = torch.cat([z, rdc_text], 1)
        bottleneck = self.main(input)
        # output = self.head(bottleneck)

        return bottleneck
