

""" import csv

header = ['name', 'area', 'country_code2', 'country_code3']
data = ['Afghanistan', 652090, 'AF', 'AFG']


with open('countries.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write the data
    writer.writerow(data) """


""" import csv

data = {
    'https://knigogo.net/knigi/palata-6/#lib_book_download': ['Палата № 6', ['Антон Павлович Чехов'], '2007', ['Русская классика', 'Литература 19 века']]
}

header = list(data.keys())
values = list(data.values())

# Flatten the nested list in the values
flattened_values = [item for sublist in values for item in sublist]

with open('output.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(header)

    # Write the data row
    #writer.writerow(flattened_values)
 """

import csv

data = {
    'https://knigogo.net/knigi/palata-6/#lib_book_download': ['Палата № 6', ['Антон Павлович Чехов'], '2007', ['Русская классика', 'Литература 19 века']]
}

header = ['key', 'name', 'author', 'year', 'genre']

# Define the filename for the CSV file
filename = 'books.csv'

# Open the file in write mode
with open(filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header to the CSV file
    writer.writerow(header)
    
    # Write each row of data to the CSV file
    for key, book_data in data.items():
        row = [key] + book_data
        writer.writerow(row)

print("Data written to", filename)
