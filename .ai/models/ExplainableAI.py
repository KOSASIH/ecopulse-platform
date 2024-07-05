import numpy as np
from lime.lime_tabular import LimeTabularExplainer

class ExplainableAI:
    def __init__(self, model, data):
        self.model = model
        self.data = data
        self.explainer = LimeTabularExplainer(self.data, feature_names=self.data.columns, class_names=['class0', 'class1'])

    def explain_instance(self, instance):
        exp = self.explainer.explain_instance(instance, self.model.predict_proba, num_features=5)
        return exp.as_list()

    def explain_model(self):
        exp = self.explainer.explain_model(self.model, self.data, num_features=5)
        return exp.as_list()
