from textnode import TextNode
import shutil
import os
from website_utils import (copy_over_files, 
                           generate_page,
                           generate_pages_recursive)

def main():
    shutil.rmtree("public")
    os.mkdir("public")
    copy_over_files("static","public")
    generate_pages_recursive("content","template.html","public")

main()