import sys
import torch
import torch.nn as nn
import numpy as np

from sklearn.cluster import KMeans

class Clustering(object):

    def __init__(self, K, n_init=5, max_iter=250):
        self.K = K
        self.n_init = n_init
        self.max_iter = max_iter

        self.u = None
        self.M = None

    def cluster(self, embed):
        # Ensure embed is detached and convert to numpy
        embed_np = embed.detach().cpu().numpy()
        
        # Check for NaN values and infinite values
        if np.isnan(embed_np).any() or np.isinf(embed_np).any():
            print("Warning: Embedding contains NaN or infinite values. Replacing with zeros.")
            embed_np = np.nan_to_num(embed_np, nan=0.0, posinf=0.0, neginf=0.0)
        
        try:
            clustering = KMeans(n_clusters=min(self.K, len(embed_np)), n_init=self.n_init, max_iter=self.max_iter)
            clustering.fit(embed_np)
            
            self.M = clustering.labels_
            self.u = self._compute_centers(self.M, embed_np)
        
        except Exception as e:
            print(f"Clustering failed: {e}")
            # Fallback: assign all to a single cluster
            self.M = np.zeros(embed_np.shape[0], dtype=int)
            self.u = {0: np.mean(embed_np, axis=0)}

    def get_loss(self, embed):
        loss = torch.Tensor([0.])
        #TODO: This may be slightly inefficient, we can fix it later to use matrix multiplications
        for i, clusteridx in enumerate(self.M):
            x = embed[i]
            c = self.u[clusteridx]
            difference = x - c
            err = torch.sum(torch.mul(difference, difference))
            loss += err

        return loss

    def get_membership(self):
        return self.M

    def _compute_centers(self,labels, embed):
        """
        sklearn kmeans may not give accurate cluster centers in some cases (see doc), so we compute ourselves
        """
        clusters = {}
        for i,lbl in enumerate(labels):
            if clusters.get(lbl) is None:
                clusters[lbl] = []
            clusters[lbl].append(torch.FloatTensor(embed[i]))
        
        centers = {}
        for k in clusters:
            all_embed = torch.stack(clusters[k])
            center = torch.mean(all_embed, 0)
            centers[k] = center
        
        return centers