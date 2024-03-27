import os
import subprocess
import shutil


import os
import shutil

def move_files(input_dir, output_dir, subdir_name):
    # Create the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create the subdirectory under the output directory
    sub_dir_path = os.path.join(output_dir, subdir_name)
    if not os.path.exists(sub_dir_path):
        os.makedirs(sub_dir_path)

    # Iterate through all files in the input directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.json'):
            # Move JSON files to the subdirectory under the output directory
            src_json = os.path.join(input_dir, file_name)
            dest_json = os.path.join(sub_dir_path, file_name)
            shutil.move(src_json, dest_json)

            # Move corresponding PNG files to the same directory
            png_file_name = os.path.splitext(file_name)[0] + '.png'
            src_png = os.path.join(input_dir, png_file_name)
            dest_png = os.path.join(sub_dir_path, png_file_name)
            if os.path.exists(src_png):
                shutil.move(src_png, dest_png)



print("Starting upscale all")
output_directory = "highres"
curated_directory = os.path.join(os.getcwd(), "currated")

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

for root, dirs, files in os.walk(curated_directory):
    for directory in dirs:
        if "_" in directory and "nsfw" not in directory:
            print(directory)
            subdir_path = os.path.join(root, directory)
            for file in os.listdir(subdir_path):
                if file.endswith(".json"):
                    json_file_path ="currated/" +directory+"/"+file
                    #json_file_path = os.path.join(subdir_path, file)
                    command = [
                        "python",
                        "generatenpcfromjson.py",
                        "-json",
                        json_file_path
                    ]
                    print(" ".join(command))
                    subprocess.run(command)
                    
                    # Find the corresponding PNG file
                    png_file_path = os.path.splitext(json_file_path)[0] + ".png"
                    if os.path.exists(png_file_path):
                        os.remove(png_file_path)
                    if os.path.exists(json_file_path):
                        os.remove(json_file_path)
                    # Example usage:
                    input_directory = 'output'
                    output_directory = 'highres'
                    sub_directory = directory
                    move_files(input_directory, output_directory, sub_directory)


