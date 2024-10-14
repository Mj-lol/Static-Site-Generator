from textnode import *
from htmlnode import *

import os
import shutil

def clean_destination(dest_dir):
    if os.path.exists(dest_dir):
        print(f"deleting directory: {dest_dir}")
        shutil.rmtree(dest_dir)

def copy_directory(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            print(f"Copied file: {dest_path}")
        elif os.path.isdir(src_path):
            os.mkdir(dest_path)
            print(f"Created directory: {dest_path}")
            copy_directory(src_path, dest_path)

def main():
    src_dir = 'static'
    dest_dir = 'public'

    clean_destination(dest_dir)
    copy_directory(src_dir, dest_dir)
    print("Copy operation completed successfully.")

if __name__ == '__main__':
    main()

main()
