import sys
import os
import shutil
from markdownparser import markdown_to_html_node
from htmlnode import ParentNode

def copy_resources(path_to_public):
    if not os.path.exists("static"):
        raise Exception("The path:\"/static\" does not exist")
    
    if os.path.exists(path_to_public):
        shutil.rmtree(path_to_public)

    copy_folder_resources("static", path_to_public)
    
def copy_folder_resources(source_folder, destination_folder):
    os.mkdir(destination_folder)
    for path in os.listdir(source_folder):
        full_path = os.path.join(source_folder, path)
        if os.path.isfile(full_path):
            shutil.copy(full_path, destination_folder)
        else:
            copy_folder_resources(full_path, os.path.join(destination_folder, path))

def extract_title(markdown):
    with open(markdown) as file:
        title = file.readline()
        if not title.startswith("#"):
            raise Exception(f"File {markdown} has no title")
        else:
            title = title.strip("#")
    return title

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    markdown = ""
    template = ""
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(from_path)
    applied_template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    applied_template = applied_template.replace('href="/', 'href="' + basepath + "/")
    applied_template = applied_template.replace('src="/', 'src="' + basepath + "/")

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    with open(os.path.join(dest_path, "index.html"), "w") as file:
        file.write(applied_template)

def generate_page_recursively(from_folder, template, dest_folder, basepath):
    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)

    for path in os.listdir(from_folder):
        full_path = os.path.join(from_folder, path)
        if os.path.isfile(full_path):
            generate_page(full_path, template, dest_folder, basepath)
        else:
            generate_page_recursively(full_path, template, os.path.join(dest_folder, path), basepath)
            

def main():

    path_to_content = "./content"
    path_to_template = "./template.html"
    path_to_public = "./docs"
    basepath = "/"
    
    if(len(sys.argv)) > 1:
        basepath = sys.argv[1]

    copy_resources(path_to_public)
    generate_page_recursively(path_to_content, path_to_template, path_to_public, basepath)
    pass


main()