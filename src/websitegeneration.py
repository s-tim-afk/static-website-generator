import os
import shutil
from htmlnode import HTMLNode
from mdtohtmlnode import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("no h1 heading")

def generate_page(src_path, template_path, dst_path, basepath="/"):
    print(f"Generating page from {src_path} to {dst_path} using {template_path}")
    with open(src_path) as f:
        markdown = f.read()
    template = open(template_path).read()
    content_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    #html_page = template.replace("{{ Title }}", title).replace(
    #    "{{ Content }}", 
    #    content_html.replace("<h1>Tolkien Fan Club</h1>", ""))
    html_page = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", 
        content_html)
    html_page = html_page.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, "w+") as index_html:
        index_html.write(html_page)