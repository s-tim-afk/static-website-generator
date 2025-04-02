import os
import shutil
import sys
from websitegeneration import generate_page

def copy_directory(src, dst):
	if os.path.exists(dst):
		shutil.rmtree(dst)
	os.mkdir(dst)
	contents = os.listdir(src)
	for content in contents:
		content_path = os.path.join(src, content)
		if os.path.isfile(content_path):
			print(f"Copying file: {content_path} → {dst}")
			shutil.copy(content_path, dst)
		else:
			subdirectory_path = os.path.join(dst, content)
			print(f"Creating directory: {subdirectory_path}")
			os.makedirs(subdirectory_path, exist_ok=True)
			copy_directory(content_path, subdirectory_path)

def find_all_markdown_files(directory):
    markdown_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                markdown_files.append(full_path)
    return markdown_files

def main():
	if len(sys.argv) >= 2:
		basepath = sys.argv[1]
	else:
		basepath = "/"
	base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	static_path = os.path.join(base_dir, "static")
	public_path = os.path.join(base_dir, "public")
	print(f"deleting directory {public_path}")
	shutil.rmtree(public_path)
	copy_directory(static_path, public_path)
	markdown_files = find_all_markdown_files(os.path.join(base_dir, "content"))
	for markdown_file in markdown_files:
		src_path = markdown_file
		template_path = os.path.join(base_dir, "template.html")
		dst_path = os.path.join(public_path, os.path.relpath(markdown_file, os.path.join(base_dir, "content")).replace(".md", ".html"))
		generate_page(src_path, template_path, dst_path, basepath)

main()
