from textnode import *
import os
import shutil

def copy_directory(src, dst):
	print(os.path.exists(dst))
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

def main():
	base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	static_path = os.path.join(base_dir, "static")
	public_path = os.path.join(base_dir, "public")
	copy_directory(static_path, public_path)

main()
