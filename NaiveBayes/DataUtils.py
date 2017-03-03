import numpy as np


def load_data(file_path):
    features = None
    labels = None
    with open(file_path) as f:
        for line in f:
            temp = np.array([line.rstrip('\n').split(",")], dtype=np.float32)
            if features is None:
                features = temp[:, :-1]
                labels = temp[:, -1:]
            else:
                features = np.concatenate((features, temp[:, :-1]))
                labels = np.concatenate((labels, temp[:, -1:]))
    return features, labels


def normalize(data):
    range_data = np.std(data, axis=0)
    mean_data = np.mean(data, axis=0)
    return (data - mean_data) / range_data, mean_data, range_data
