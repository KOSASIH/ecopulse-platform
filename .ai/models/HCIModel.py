import cv2
import numpy as np
from sklearn.svm import SVC

class HCIModel:
    def __init__(self, model_path):
        self.model = SVC()
        self.model.load(model_path)

    def predict(self, image):
        image = cv2.resize(image, (224, 224))
        image = image.reshape((1, 224, 224, 3))
        return self.model.predict(image)

    def train(self, images, labels):
        self.model.fit(images, labels)
