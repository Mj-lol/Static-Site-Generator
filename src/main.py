from textnode import *
from htmlnode import *
from pathlib import Path

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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")


def main():
    src_dir = "./static"
    dest_dir = "./public"
    template = "./template.html"
    clean_destination(dest_dir)
    copy_directory(src_dir, dest_dir)
    #alternatively we have
    #shutil.copytree(src_dir, dest_dir)
    src ="./content"
    dest="./public"
    print("Copy operation completed successfully.")
    generate_pages_recursive(src, template, dest)

if __name__ == '__main__':
    main()

main()
