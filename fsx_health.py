import os
import shutil

network_share_path = r"\\fs-0b060f4317a02b1fa.rxtest.local\share"
file_name = "example.txt"
file_path = os.path.join(network_share_path, file_name)

def CREATE_FILE(file_path):
    with open(file_path, "w") as file:
        file.write("This is a test file.")

def TEST_FILE(file_path, file_name):
    if os.path.exists(file_path):
        print(f"File '{file_name}' was successfully created on the network share.")
    else:
        print(f"Failed to create the file '{file_name}' on the network share.")

def DELETE_FILE(file_path, file_name):
    try:
        os.remove(file_path)
        print(f"File '{file_name}' was successfully deleted from the network share.")
    except FileNotFoundError:
        print(f"The file '{file_name}' does not exist on the network share.")
    except Exception as e:
        print(f"An error occurred while deleting the file: {str(e)}")

CREATE_FILE(file_path)
TEST_FILE(file_path, file_name)
input("Press enter to continue")
DELETE_FILE(file_path, file_name)