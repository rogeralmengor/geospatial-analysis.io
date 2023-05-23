import os

def create_folder_structure(root_path):
    # Create root directory
    os.makedirs(root_path, exist_ok=True)

    # Create language-specific directories
    languages = ['rust', 'python', 'julia', 'c', 'gee-javascript']
    for lang in languages:
        lang_path = os.path.join(root_path, lang)
        os.makedirs(lang_path, exist_ok=True)
        src_path = os.path.join(lang_path, 'src')
        os.makedirs(src_path, exist_ok=True)
        test_path = os.path.join(lang_path, 'tests')
        os.makedirs(test_path, exist_ok=True)

    # Create geopackage directory structure
    gpkg_path = os.path.join(root_path, 'geopackage')
    os.makedirs(gpkg_path, exist_ok=True)
    data_path = os.path.join(gpkg_path, 'data')
    os.makedirs(data_path, exist_ok=True)
    docs_path = os.path.join(gpkg_path, 'docs')
    os.makedirs(docs_path, exist_ok=True)
    examples_path = os.path.join(gpkg_path, 'examples')
    os.makedirs(examples_path, exist_ok=True)

    # Create README and LICENSE files
    readme_path = os.path.join(gpkg_path, 'README.md')
    open(readme_path, 'a').close()  # Create an empty file
    license_path = os.path.join(gpkg_path, 'LICENSE')
    open(license_path, 'a').close()  # Create an empty file

if __name__ == '__main__':
    project_root = '.'
    create_folder_structure(project_root)
    print(f"Folder structure created successfully in '{project_root}' directory.")

