import pickle as pkl
import os
import networkx as nx
import numpy as np
import scipy.sparse as sp
import torch
import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score
from matplotlib import pyplot as plt

import json
import torch
import numpy as np

def load_data_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    num_nodes = len(data['nodes'])
    adj = torch.zeros(num_nodes, num_nodes)
    
    # Iterate over the relationships under edges
    for relationship in data['edges'][0]['relationship']:
        # Accessing 'start' and 'end' inside the 'properties' dictionary
        start = int(relationship['properties']['start']) - 1  # Convert to zero-based index
        end = int(relationship['properties']['end']) - 1      # Convert to zero-based index
        frequency = relationship['frequency']
        
        # Assuming the edges are directed and weighted by 'frequency'
        adj[start, end] = frequency
        # If the graph is undirected, you might want to also do:
        # adj[end, start] = frequency

    # Creating feature matrix as an identity matrix; modify as needed
    features = torch.eye(num_nodes)

    return adj, features


def load_data_cma(dataset):
    adj_file = os.path.join(dataset, "struct.csv")
    feat_file = os.path.join(dataset, "content.csv")

    # Load and create adjacency matrix
    adj = pd.read_csv(adj_file, header=None)
    adj = adj.values
    adj = nx.from_numpy_array(adj)  # Updated function
    adj = nx.adjacency_matrix(adj)
    print("Adjacency matrix shape:", adj.shape)    

    # Load features
    feat = pd.read_csv(feat_file, header=None)
    feat = feat.values
    features = torch.FloatTensor(feat)
    print("Features shape:", features.shape)

    return adj, features


def parse_index_file(filename):
    index = []
    for line in open(filename):
        index.append(int(line.strip()))
    return index


def sparse_to_tuple(sparse_mx):
    if not sp.isspmatrix_coo(sparse_mx):
        sparse_mx = sparse_mx.tocoo()
    coords = np.vstack((sparse_mx.row, sparse_mx.col)).transpose()
    values = sparse_mx.data
    shape = sparse_mx.shape
    return coords, values, shape


def preprocess_graph(adj):
    adj = sp.coo_matrix(adj)
    adj_ = adj + sp.eye(adj.shape[0])
    rowsum = np.array(adj_.sum(1))
    degree_mat_inv_sqrt = sp.diags(np.power(rowsum, -0.5).flatten())
    adj_normalized = adj_.dot(degree_mat_inv_sqrt).transpose().dot(degree_mat_inv_sqrt).tocoo()
    # return sparse_to_tuple(adj_normalized)
    return sparse_mx_to_torch_sparse_tensor(adj_normalized)


def sparse_mx_to_torch_sparse_tensor(sparse_mx):
    """Convert a scipy sparse matrix to a torch sparse tensor."""
    sparse_mx = sparse_mx.tocoo().astype(np.float32)
    indices = torch.from_numpy(
        np.vstack((sparse_mx.row, sparse_mx.col)).astype(np.int64))
    values = torch.from_numpy(sparse_mx.data)
    shape = torch.Size(sparse_mx.shape)
    return torch.sparse.FloatTensor(indices, values, shape)

def plot_losses(losses, epoch_mark):

    for i in range(4):
        plt.subplot(2,2,i+1)
        plt.plot(losses[:,i])
        plt.axvline(epoch_mark, color='r')
        plt.axvline(epoch_mark*2, color='g')
    plt.show()

