import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

class DataProcessor:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = pd.read_csv(data_path)

    def preprocess_data(self):
        self.data.dropna(inplace=True)
        self.data = self.data.apply(lambda x: x.astype(str).str.lower())
        self.data = self.data.apply(lambda x: x.str.replace(r'[^\w\s]', ''))
        scaler = StandardScaler()
        self.data[['feature1', 'feature2', 'feature3']] = scaler.fit_transform(self.data[['feature1', 'feature2', 'feature3']])
        pca = PCA(n_components=0.95)
        self.data[['feature1', 'feature2', 'feature3']] = pca.fit_transform(self.data[['feature1', 'feature2', 'feature3']])
        return self.data

    def feature_engineering(self):
        self.data['new_feature1'] = self.data['feature1'] * self.data['feature2']
        self.data['new_feature2'] = self.data['feature2'] / self.data['feature3']
        return self.data

    def data_visualization(self):
        import matplotlib.pyplot as plt
        plt.scatter(self.data['feature1'], self.data['feature2'])
        plt.xlabel('Feature 1')
        plt.ylabel('Feature 2')
        plt.title('Feature 1 vs Feature 2')
        plt.show()
        return self.data
