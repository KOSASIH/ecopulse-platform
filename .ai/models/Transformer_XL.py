import torch
import torch.nn as nn
import torch.nn.functional as F

class TransformerXL(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, num_heads, num_layers):
        super(TransformerXL, self).__init__()
        self.encoder = TransformerXL_Encoder(input_dim, hidden_dim, num_heads, num_layers)
        self.decoder = TransformerXL_Decoder(hidden_dim, output_dim, num_heads, num_layers)

    def forward(self, input_seq):
        encoder_output = self.encoder(input_seq)
        decoder_output = self.decoder(encoder_output)
        return decoder_output

class TransformerXL_Encoder(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_heads, num_layers):
        super(TransformerXL_Encoder, self).__init__()
        self.layers = nn.ModuleList([TransformerXL_EncoderLayer(input_dim, hidden_dim, num_heads) for _ in range(num_layers)])

    def forward(self, input_seq):
        for layer in self.layers:
            input_seq = layer(input_seq)
        return input_seq

class TransformerXL_EncoderLayer(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_heads):
        super(TransformerXL_EncoderLayer, self).__init__()
        self.self_attn = MultiHeadAttention(input_dim, hidden_dim, num_heads)
        self.feed_forward = nn.Linear(hidden_dim, hidden_dim)

    def forward(self, input_seq):
        attention_output = self.self_attn(input_seq, input_seq)
        output = self.feed_forward(attention_output)
        return output

class TransformerXL_Decoder(nn.Module):
    def __init__(self, hidden_dim, output_dim, num_heads, num_layers):
        super(TransformerXL_Decoder, self).__init__()
        self.layers = nn.ModuleList([TransformerXL_DecoderLayer(hidden_dim, output_dim, num_heads) for _ in range(num_layers)])

    def forward(self, encoder_output):
        for layer in self.layers:
            encoder_output = layer(encoder_output)
        return encoder_output

class TransformerXL_DecoderLayer(nn.Module):
    def __init__(self, hidden_dim, output_dim, num_heads):
        super(TransformerXL_DecoderLayer, self).__init__()
        self.self_attn = MultiHeadAttention(hidden_dim, hidden_dim, num_heads)
        self.encoder_attn = MultiHeadAttention(hidden_dim, hidden_dim, num_heads)
        self.feed_forward = nn.Linear(hidden_dim, output_dim)

    def forward(self, encoder_output):
        attention_output = self.self_attn(encoder_output, encoder_output)
        attention_output = self.encoder_attn(attention_output, encoder_output)
        output = self.feed_forward(attention_output)
        return output

class MultiHeadAttention(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_heads):
        super(MultiHeadAttention, self).__init__()
        self.query_linear = nn.Linear(input_dim, hidden_dim)
        self.key_linear = nn.Linear(input_dim, hidden_dim)
        self.value_linear = nn.Linear(input_dim, hidden_dim)
        self.dropout = nn.Dropout(0.1)

    def forward(self, query, key, value):
        query = self.query_linear(query)
        key = self.key_linear(key)
        value = self.value_linear(value)
        attention_scores = torch.matmul(query, key.T) / math.sqrt(hidden_dim)
        attention_scores = F.softmax(attention_scores, dim=-1)
        attention_scores = self.dropout(attention_scores)
        output = attention_scores * value
        return output
