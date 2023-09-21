import charset_normalizer

with open("x:/Projects/data-science/identification/62350266.txt", 'rb') as f:
    content_bytes = f.read()
detected = charset_normalizer.detect(content_bytes)
encoding = detected['encoding']
content_text = content_bytes.decode(encoding)
with open('your_input_file.txt', 'w', encoding='utf-8') as f:
    f.write(content_text)
