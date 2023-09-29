import torch
import os
import pickle
from collections import OrderedDict
import torch.nn as nn
from torch.optim import AdamW

from transformers import get_linear_schedule_with_warmup, AutoTokenizer, AutoModel, logging
logging.set_verbosity_error()

tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base", use_fast=False)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class SentimentClassifier(nn.Module):
    def __init__(self, n_classes):
        super(SentimentClassifier, self).__init__()
        self.bert = AutoModel.from_pretrained("vinai/phobert-base")
        self.drop = nn.Dropout(p=0.3)
        self.fc = nn.Linear(self.bert.config.hidden_size, n_classes)
        nn.init.normal_(self.fc.weight, std=0.02)
        nn.init.normal_(self.fc.bias, 0)

    def forward(self, input_ids, attention_mask):
        last_hidden_state, output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            return_dict=False # Dropout will errors if without this
        )

        x = self.drop(output)
        x = self.fc(x)
        return x


def infer(loaded_model, text, tokenizer, max_len=120):
    encoded_review = tokenizer.encode_plus(
        text,
        max_length=max_len,
        truncation=True,
        add_special_tokens=True,
        padding='max_length',
        return_attention_mask=True,
        return_token_type_ids=False,
        return_tensors='pt',
    )

    input_ids = encoded_review['input_ids'].to(device)
    attention_mask = encoded_review['attention_mask'].to(device)

    output = loaded_model(input_ids, attention_mask)
    _, y_pred = torch.max(output, dim=1)

    class_names = ['Vui vẻ', 'Kinh tởm', 'Buồn', 'Giận dữ', 'Ngạc nhiên', 'Sợ hãi', 'Lạ quá không đoán được hihi']

    # print(f'Text: {text}')
    # print(f'Sentiment: {class_names[y_pred]}')
    return class_names[y_pred]

def load_model(loaded_model, checkpoint_path):
  checkpoint =torch.load(checkpoint_path, map_location='cpu')
  new_state_dict = OrderedDict()
  for k, v in checkpoint.items():
      name = k.replace("module.", "") # remove `module.`
      new_state_dict[name] = v
  loaded_model.load_state_dict(new_state_dict, strict=False)
  return 

