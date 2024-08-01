"""
Module that renames teh files of /dit247/data/nodered/images
to filename format 'file-1.jpg', 'file-2.jpg', ...
in order to be easily fetched from noderd flow
"""

import os

cwd = os.getcwd()
img_fld_path = os.path.join(cwd, 'data', 'nodered', 'images')
files = [os.path.join(img_fld_path, fl) for fl in os.listdir(img_fld_path)]

# Loop through each file and rename it
for index, old_file in enumerate(files, start=1):
    # Extract file extension
    file_extension = os.path.splitext(old_file)[1]
    # Create new filename
    new_filename = f"file-{index}{file_extension}"
    # Formulate the full old and new file paths
    new_file = os.path.join(img_fld_path, new_filename)
    old_filepath = os.path.abspath(old_file)
    new_filepath = os.path.abspath(new_file)
    # Rename the file
    os.rename(old_filepath, new_filepath)