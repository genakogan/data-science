import charset_normalizer

# # Specify the input and output file names
# input_file = 'x:/Projects/data-science/identification/books/61528814.txt'
# output_file = 'x:/Projects/data-science/identification/output/61528814.txt'

# # =============================================================================

# # encoding to utf-8
# with open(input_file, 'rb') as f:
#     content_bytes = f.read()
# detected = charset_normalizer.detect(content_bytes)
# encoding = detected['encoding']
# content_text = content_bytes.decode(encoding)

# # Open the file in 'utf-8' mode and prevent newline characters from being added
# with open(input_file, 'w', encoding='utf-8', newline='') as f:
#     f.write(content_text)

# # =============================================================================

# # search author
# with open(input_file, 'r', encoding='utf-8') as file:
#     # Initialize a line counter
#     line_count = 0
#     words_to_remove = ''
#     # Iterate through each line in the file
#     for line in file:
#         # Increment the line counter
#         line_count += 1

#         # Check if this is the second line
#         if line_count == 2:
#             # Print or do something with the second line
#             words_to_remove = line.strip()
#             # Use strip() to remove trailing newline character
#             # print("Second line:", words_to_remove)
#             break

# # =============================================================================

# def strSplit(words_to_remove):
#     li = list(words_to_remove.split(" "))
#     return li
# print(strSplit(words_to_remove))

# # =============================================================================

# # remove author from txt file
# # Words to search for in lines
# if words_to_remove != '':
#     words_to_remove = strSplit(words_to_remove)
#     """ print(words_to_remove) """
#     # Open the input file for reading and the output file for writing
#     with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
#         for line in infile:
#             # Check if the line contains any of the specified words
#             if not any(word in line for word in words_to_remove):
#                 # If none of the words are found, write the line to the output file
#                 outfile.write(line)

#     print(
#         f"Lines containing specified words removed and saved to '{output_file}'.")
# else:
#      with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
#          for line in infile:
#               outfile.write(line)

# # =============================================================================


# # Open the text file
# with open(output_file, 'r', encoding='utf-8') as file:
#     text = file.read()
# print(text)# Tokenize the text
# words = re.findall(r'\b\w+\b', text)


# # Split into chunks
# chunk_size = 1000
# current_chunk = []
# chunks = []

# for word in words:
#     current_chunk.append(word)
#     if len(current_chunk) >= chunk_size:
#         chunks.append(current_chunk)
#         current_chunk = []

# # Add any remaining words to the last chunk
# if current_chunk:
#     chunks.append(current_chunk)

# # Write chunks to separate files
# for i, chunk in enumerate(chunks):
#     with open(f'x:/Projects/data-science/identification/output/chunk_{i + 1}.txt', 'w',  encoding='utf-8') as chunk_file:
#         chunk_file.write(' '.join(chunk))
