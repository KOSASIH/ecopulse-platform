import torch
import torch.nn as nn
import torchvision.models as models

class ResNet:
    def __init__(self, model_path):
        self.model = models.resnet50(pretrained=True)
        self.model.load_state_dict(torch.load(model_path))

    def predict(self, image):
        image = image.unsqueeze(0)
        outputs = self.model(image)
        _, predicted = torch.max(outputs, 1)
        return predicted.item()
