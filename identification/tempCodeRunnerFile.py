from transformers import BertTokenizer
# import torch

# tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

# text = "Запах смерти Саймон Бекетт Детектив – самое лучшее..."
# # Tokenize the text
# input_ids = tokenizer.encode(text, add_special_tokens=True, truncation=True, max_length=100, padding='max_length')

# # Convert input_ids to a PyTorch tensor
# input_ids = torch.tensor(input_ids).unsqueeze(0)

# print(input_ids)