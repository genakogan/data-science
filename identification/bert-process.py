import os
import shutil

def copy_txt_files_recursive(source_dir, destination_dir, num_files_to_copy):
    try:
        txt_files = []
        
        # Recursively traverse the source directory to collect all .txt files
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file.endswith(".txt"):
                    txt_files.append(os.path.join(root, file))
        
        # Ensure num_files_to_copy is not greater than the number of .txt files
        num_files_to_copy = min(num_files_to_copy, len(txt_files))
        
        # Select the first num_files_to_copy .txt files
        txt_files_to_copy = txt_files[:num_files_to_copy]
        
        # Copy selected .txt files from source to destination directory
        for txt_file in txt_files_to_copy:
            file_name = os.path.basename(txt_file)
            destination_path = os.path.join(destination_dir, file_name)
            try:
                shutil.copy2(txt_file, destination_path)
                print(f"Copying {file_name} to {destination_path}")
            except PermissionError as pe:
                print(f"PermissionError copying {file_name}: {pe}")
            except FileNotFoundError as fe:
                print(f"FileNotFoundError copying {file_name}: {fe}")
            except Exception as e:
                print(f"Error copying {file_name}: {e}")
    except Exception as e:
        print(f"Error accessing source directory: {e}")

# Example usage
source_directory = 'X:/Projects/data-science/identification/result/all-chunks-separate-folders/'
destination_directory = 'X:/Projects/data-science/identification/result/small-data-set/'
num_files_to_copy = 10

copy_txt_files_recursive(source_directory, destination_directory, num_files_to_copy)
