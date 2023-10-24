# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# import nltk

# # Set the language to Russian
# nltk.download('stopwords')
# stop_words = set(stopwords.words('russian'))

# # Open the input text file for reading (assuming it's encoded in UTF-8)
# with open('X:/Projects/data-science/identification/60938187.txt', 'r', encoding='utf-8') as input_file:
#     example_sent = input_file.read()

# # Tokenize the input Russian text
# word_tokens = word_tokenize(example_sent, language='russian')

# # Filter out Russian stop words
# filtered_sentence = [w for w in word_tokens if w.lower() not in stop_words]

# # Open the output text file for writing (encoded in UTF-8)
# with open('X:/Projects/data-science/identification/txtoutput.txt', 'w', encoding='utf-8') as output_file:
#     # Write the filtered words to the output file
#     for word in filtered_sentence:
#         output_file.write(word + " ")

# print("Filtered text saved to 'output.txt'")



from transformers import BertTokenizer
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

text = "Запах смерти Саймон Бекетт Детектив – самое лучшее..."
# Tokenize the text
input_ids = tokenizer.encode(text, add_special_tokens=True, truncation=True, max_length=100, padding='max_length')

# Convert input_ids to a PyTorch tensor
input_ids = torch.tensor(input_ids).unsqueeze(0)

print(input_ids)


