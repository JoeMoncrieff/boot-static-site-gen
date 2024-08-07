import os, shutil
from block_utils import markdown_to_html_node, extract_title

def copy_over_files(source_path,target_path):
    if os.path.exists(source_path) and os.path.exists(target_path):
        # delete everything in target_path
        shutil.rmtree(target_path)
        os.mkdir(target_path)
        for item in os.listdir(source_path):
            if os.path.isfile(f"{source_path}/{str(item)}"):
                shutil.copy(f"{source_path}/{str(item)}",f"{target_path}/{str(item)}")
            elif os.path.isdir(f"{source_path}/{str(item)}"):
                os.mkdir(f"{target_path}/{str(item)}")
                copy_over_files(f"{source_path}/{str(item)}",f"{target_path}/{str(item)}")

    else:
        raise Exception("invalid paths")
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_file = ""
    with open(from_path) as f:
        markdown_file = f.read()
    
    template_file = ""
    with open(template_path) as f:
        template_file = f.read()
    
    content_string = markdown_to_html_node(markdown_file).to_html()

    template_file = template_file.replace("{{ Content }}",content_string)
    template_file = template_file.replace("{{ Title }}", extract_title(markdown_file))

    #build a way to dest. path

    current_path = ""
    for dir in dest_path.split("/")[:-1]:
        if current_path != "":
            current_path += f"/{dir}"
        else:
            current_path += f"{dir}"
        if not os.path.exists(current_path):
            os.mkdir(current_path)
    
    if os.path.exists(dest_path):
        os.remove(dest_path)
    with open(dest_path,"w") as f:
        f.write(template_file)
    
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """* Crawl every entry in the content directory
        
       * For each markdown file found, generate a new .html file using the same template.html. 
        The generated pages should be written to the public directory in the same directory 
        structure."""
    for file in os.listdir(dir_path_content):
        file_path = f"{dir_path_content}/{file}"
        if os.path.isdir(file_path):
            generate_pages_recursive(file_path,template_path,f"{dest_dir_path}/{file}")
        elif len(file) > 3:
            if file[-3:] == ".md":
                generate_page(file_path,template_path,f"{dest_dir_path}/{file[:-2]}html")
        

