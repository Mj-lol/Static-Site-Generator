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

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    raise Exception("H1 heading required")


def generate_page(fro, template, to):
    print(f"Generating page from {fro} to {to} using {template}.")
    with open(fro, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    with open(template, 'r', encoding='utf-8') as f:
        template_content = f.read()
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    title = extract_title(markdown_content)
    full_html = template_content.replace('{{ Title }}', title).replace('{{ Content }}', html_content)

    dest_dir = os.path.dirname(to)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(to, 'w', encoding='utf-8') as f:
        f.write(full_html)





def main():
    src_dir = 'static'
    dest_dir = 'public'
    template = 'template.html'
    clean_destination(dest_dir)
    copy_directory(src_dir, dest_dir)
    #alternatively we have
    #shutil.copytree(src_dir, dest_dir)
    src ="content/index.md"
    dest="public/index.html"
    print("Copy operation completed successfully.")
    generate_page(src, template, dest)

if __name__ == '__main__':
    main()

main()
