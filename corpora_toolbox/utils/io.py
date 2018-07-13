import codecs
import os

# Function to save a string into a file
def save_string_in_file(string_text, file_name):
    with codecs.open(file_name, "w", "utf-8") as f:
        f.write(string_text)
        f.close()

# Function to read all files in a dir with a specific extension
def read_files_in_dir_ext(dir_route, extension):

    files = os.listdir(dir_route)
    files_ext = [file for file in files if file.endswith(extension)]
    return files_ext


# Function to read a file into a string
def read_file_in_string(file_name):
    file_in_string = ""

    with codecs.open(file_name, "r", "utf-8") as f:
        file_in_string = f.read()
        f.close()

    return file_in_string

# Function to create a directory
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return
