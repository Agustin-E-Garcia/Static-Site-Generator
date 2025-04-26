import os
import shutil
from markdownparser import markdown_to_html_node
from htmlnode import ParentNode

def copy_resources():
    if not os.path.exists("static"):
        raise Exception("The path:\"/static\" does not exist")
    
    if os.path.exists("public"):
        shutil.rmtree("public")

    copy_folder_resources("static", "public")
    
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

def generate_page(from_path, template_path, dest_path, filename):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    markdown = ""
    template = ""
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(from_path)
    applied_tempalte = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    with open(os.path.join(dest_path, filename), "w") as file:
        file.write(applied_tempalte)

def main():
    copy_resources()
    generate_page("content/index.md", "template.html", "public", "index.html")
    pass

if __name__ == "__main__":
    main()