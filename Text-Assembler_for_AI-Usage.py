"""
Text-Assembler_for_AI-Usage

Author: PizzaFuel
Repository: https://github.com/PizzaFuel/Text-Assembler_for_AI-Usage

License: MIT License

This script is designed to traverse through a directory structure, list all files, and compile the contents of text files into a single output file. It is intended to simplify the process of analyzing codebases and other text-based project assets.

Disclaimer:
This script is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort or otherwise, arising from, out of, or in connection with the script or the use or other dealings in the script.

Usage of this script is at your own risk. The author, PizzaFuel, takes no accountability for the consequences of using this script, including but not limited to data loss, system disruption, or legal liabilities arising from its application in projects or its contribution to automated processes.
"""

import os
import subprocess
import sys

def is_text_file(filename, ignore_git_files=True):
    """
    Check if a file is a text file based on its extension.
    
    Args:
        filename (str): The name of the file to check.
        ignore_git_files (bool): Whether to include files containing .git or not.
    
    Returns:
        bool: True if the file is a text file, False otherwise.
    """
    # Set containing extensions considered as text files. Please feel free to extend this as needed.
    text_extensions = {
        '.py', '.js', '.java', '.c', '.cpp', '.cs', '.h', '.hpp', '.sh', '.go', '.rb', '.php', '.pl', '.swift', '.kt', '.ts',
        '.bash', '.ps1', '.bat', '.vbs',
        '.html', '.htm', '.css', '.scss', '.less', '.xml', '.json', '.yaml', '.yml', '.md', '.rst', '.toml', '.ini', '.csv',
        '.conf', '.config', '.cfg', '.properties',
        '.sql', '.db', '.mdb',
        '.jsp', '.asp', '.aspx', '.php3', '.php4', '.php5', '.phtml',
        '.lua', '.perl', '.groovy', '.r', '.dart', '.pas', '.scala', '.hs', '.m', '.ml', '.sml', '.lisp', '.clj', '.vim', '.tex',
        '.ipynb',
        '.env', '.gitignore', '.dockerfile', '.makefile', '.cmake', '.gradle',
        '.txt', '.log', '.md', '.rst', 
        '.rtf', '.tex', '.csv', '.tsv', '.json',
        '.odt',
    }
    # Check if the filepath contains .git in any way
    if ignore_git_files == False and ".git" in filename:
        return False
    # Check if the file's extension is in the set of text file extensions
    return filename.endswith(tuple(text_extensions))

def get_all_files(startpath, ignore_git_files=True):
    """
    Traverse directories from a given start path and categorize files into text and non-text.

    Args:
        startpath (str): The root directory path to start listing from.
        ignore_git_files (bool): Whether to include files containing .git or not.
    
    Returns:
        tuple: Two lists, the first containing paths of text files, and the second containing paths of all files.
    """
    text_files, all_files = [], []
    for root, dirs, files in os.walk(startpath):
        for file in files:
            full_path = os.path.join(root, file)
            all_files.append(full_path)  # Add every file to the all_files list
            if is_text_file(file, ignore_git_files):
                text_files.append(full_path)  # Add text files to the text_files list

    return text_files, all_files

def write_file_list(f, file_paths):
    """
    Writes a list of file paths to the provided file object.

    Args:
        f (file object): The file object to write the list to.
        file_paths (list): List of file paths to write.
    """
    f.write("<!-- File List Start -->\n")
    for path in file_paths:
        f.write(f"{path}\n")
    f.write("<!-- File List End -->\n\n")


def write_file_contents(f, text_files, startpath):
    """
    Appends the contents of each text file to the provided file object.

    Args:
        f (file object): The file object to append the contents to.
        text_files (list): List of text file paths to read and write.
        startpath (str): The root directory path for relative path calculation.
    """
    for file_path in text_files:
        relative_file_path = os.path.relpath(file_path, startpath)
        f.write(f"\n<!-- START OF FILE: {relative_file_path} -->\n")
        try:
            with open(file_path, 'r') as content_file:
                content = content_file.read()
                f.write(content + "\n")
        except Exception as e:
            f.write(f"    Error reading file: {e}\n")
        f.write(f"<!-- END OF FILE: {relative_file_path} -->\n\n")


def list_files_and_content_to_txt(startpath, output_file, include_project_info=False, ignore_git_files=True):
    """
    Generates a detailed list of all files in a directory structure, including the contents of text files,
    and writes this information to a specified output text file.
    
    Args:
        startpath (str): The root directory path to start the file listing from.
        output_file (str): Path to the output file where the listing and contents are to be written.
        include_project_info (bool): Whether to include project info at the beginning of the file.
        ignore_git_files (bool): Whether to include files containing .git or not.
    """
    text_files, all_files = get_all_files(startpath, ignore_git_files)
    file_paths = [os.path.relpath(path, startpath) for path in all_files]

    # Open once to write the intro and the file list
    with open(output_file, 'w') as f:
        intro_text = (
            "This document contains a detailed file list and contents from a specified directory structure.\n"
            "Structure Overview:\n"
            "- The document begins with the project information followed by a hierarchical list of files and directories contained in the project (File List) excluding the base path of the project.\n"
            "- Each text file is then listed with its relative path to the base of the project.\n"
            "- Any file which only contains text, such as code files (.cs, .py, .lua, ...) or documents (.txt, .md, ...), count as text files in this context.\n"
            "- The contents of each text file are enclosed between markers indicating the start and end, "
            "formatted as <!-- START OF FILE: [relative file path] --> and <!-- END OF FILE: [relative file path] -->.\n"
            "- Non-text files are listed in the File List but their contents are not included.\n\n\n"
        )
        if include_project_info:
            intro_text += (
                "This structure represents a project with the following details:\n"
                "- Project title: \n"
                "- Available under URL: \n"
                "- Made by: \n"
                "- Description: \n\n\n"
            )
        f.write(intro_text)
        write_file_list(f, file_paths)
        write_file_contents(f, text_files, startpath)

def open_file_default_app(filepath):
    """
    Opens a file with the default application based on the operating system.
    
    Args:
        filepath (str): The path of the file to open.
    """
    try:
        if sys.platform == "win32":
            os.startfile(filepath)
        elif sys.platform == "darwin":  # macOS
            subprocess.call(["open", filepath])
        else:  # Linux variants
            subprocess.call(["xdg-open", filepath])
    except Exception as e:
        print(f"Error opening file: {e}")

if __name__ == "__main__":
    folder_path = input("Please enter the folder path of the project you want assembled into one file: ")
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        main_folder_name = os.path.basename(folder_path)
        output_file_name = f"{main_folder_name}.txt" # Feel free to edit this if needed
        
        output_directory = input(f"Enter output directory or press Enter to use Desktop ({desktop_path}): ").strip()
        output_file_path = os.path.join(output_directory if output_directory else desktop_path, output_file_name)
        
        include_project_info = input("Do you want to include a project info section (y/N)?: ").lower().strip() == 'y'
        ignore_git_files = input("Do you want to ignore git files (Y/n)?: ").lower().strip() == 'n'

        print(f"Writing detailed file list and contents to {output_file_path}")
        list_files_and_content_to_txt(folder_path, output_file_path, include_project_info, ignore_git_files)
        print("Done. Detailed file list and contents have been written. Please add additional information manually.")
        
        open_file_default_app(output_file_path)
    else:
        print("The path entered does not exist or is not a directory. Please ensure the path is correct and try again.")
    
    input("Press Enter to exit...")