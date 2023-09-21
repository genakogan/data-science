# Open the text file in read mode
with open('x:/Projects/data-science/identification/62350266.txt', 'r', errors='ignore') as file:
    # Initialize a line counter
    line_count = 0
    
    # Iterate through each line in the file
    for line in file:
        # Increment the line counter
        line_count += 1
        
        # Check if this is the second line
        if line_count == 2:
            # Print or do something with the second line
            print("Second line:", line.strip())  # Use strip() to remove trailing newline character
            break 

