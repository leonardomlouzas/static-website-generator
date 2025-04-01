import os
import shutil

from block_markdown import markdown_to_html_node
from extract_markdown import extract_title


def main():
    recursive_copy("static", "public")

    generate_page("content/index.md", "templates/base.html", "public/index.html")


def recursive_copy(
    source, destination, is_destination_path_relative=True, is_first_call=True
):
    if is_destination_path_relative:
        destination = os.path.join(os.path.dirname(__file__), destination)

    # Ensure a clean copy
    if is_first_call and os.path.exists(destination) and os.path.exists(source):
        try:
            shutil.rmtree(destination)
        except Exception as e:
            print(f"Error while deleting destination folder before copy: {e}")
            return False

    # Create destination folder if it doesn't exist
    os.makedirs(destination, exist_ok=True)

    if os.path.exists(source):
        for path in os.listdir(source):
            source_path = os.path.join(source, path)
            destination_path = os.path.join(destination, path)

            try:
                if os.path.isdir(source_path):
                    recursive_copy(source_path, destination_path, False, False)
                else:
                    shutil.copy(source_path, destination_path)
            except Exception as e:
                print(f"Error while copying file {source_path}: {e}")
                return False

        try:
            shutil.rmtree(source)
        except Exception as e:
            print(f"Error while deleting folder after copy: {e}")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} using {template_path} to {dest_path}")

    markdown = ""

    with open(from_path, "r") as f:
        markdown = f.read()

    template = ""
    with open(template_path, "r") as f:
        template = f.read()

    title = extract_title(markdown)
    html = markdown_to_html_node(markdown)

    html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    temp_fix = (
        html.replace(">None<", "")
        .replace("imgsrc", "img src")
        .replace("ahref", "a href")
        .replace('"/img>', '"</img>')
    )

    with open(dest_path, "w") as f:
        f.write(temp_fix)

    print(f"Page generated at {dest_path}")


if __name__ == "__main__":
    main()
