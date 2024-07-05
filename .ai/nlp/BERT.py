import torch
from transformers import BertTokenizer, BertModel

class BERT:
    def __init__(self, model_path):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained(model_path)

    def encode(self, text):
        inputs = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=512,
            return_attention_mask=True,
            return_tensors='pt'
        )
        return inputs

    def predict(self, inputs):
        outputs = self.model(inputs['input_ids'], attention_mask=inputs['attention_mask'])
        return outputs.last_hidden_state[:, 0, :]
