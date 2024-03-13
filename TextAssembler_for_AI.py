import os

def is_text_file(filename):
    """
    Check if a file is a text file based on its extension.
    
    Args:
        filename (str): The name of the file to check.
    
    Returns:
        bool: True if the file is a text file, False otherwise.
    """
    # Tuple containing extensions considered as text files. Please extend as needed.
    text_extensions = (
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
    )
    # Check if the file's extension is in the list of text file extensions
    return filename.endswith(text_extensions)

def list_files_and_content_to_txt(startpath, output_file):
    """
    Generates a detailed list of all files in a directory structure, including the contents of text files,
    and writes this information to a specified output text file.
    
    Args:
        startpath (str): The root directory path to start the file listing from.
        output_file (str): Path to the output file where the listing and contents are to be written.
    """
    text_files = []  # List to hold paths of text files for later processing
    
    # Open the output file in write mode
    with open(output_file, 'w') as f:
        # Introduction text explaining the document's content
        intro_text = (
            "This document contains a detailed file list and contents from a specified directory structure.\n"
            "Structure Overview:\n"
            "- The document begins with the project information followed by a hierarchical list of files and directories.\n"
            "- Each text file identified by specific extensions is then listed with its relative path.\n"
            "- The contents of each text file are enclosed between markers indicating the start and end, "
            "formatted as <!-- START OF FILE: [relative file path] --> and <!-- END OF FILE: [relative file path] -->.\n"
            "- Non-text files are listed but their contents are not included.\n\n"
            "This structure represents a project with the following details :\n"
            "- Project title: \n"
            "- Available under URL: \n"
            "- Made by: \n"
            "- Description: \n\n\n"
        )
        f.write(intro_text)
        f.write("File List:\n")
        
        # Walk through the directory structure starting from startpath
        for root, dirs, files in os.walk(startpath):
            # Calculate directory level for indentation
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            f.write(f"{indent}{os.path.basename(root)}/\n")
            subindent = ' ' * 4 * (level + 1)
            for file in files:
                f.write(f"{subindent}{file}\n")
                full_path = os.path.join(root, file)
                if is_text_file(file):
                    text_files.append(full_path)
    
    # Append the contents of text files at the end of the document
    with open(output_file, 'a') as f:
        for file_path in text_files:
            relative_file_path = os.path.relpath(file_path, startpath)
            f.write(f"\n<!-- START OF FILE: {relative_file_path} -->\n")
            try:
                # Attempt to read and write the content of each text file
                with open(file_path, 'r') as content_file:
                    content = content_file.read()
                    f.write(content + "\n")
            except Exception as e:
                f.write(f"    Error reading file: {e}\n")
            f.write(f"<!-- END OF FILE: {relative_file_path} -->\n\n")

if __name__ == "__main__":
    # Main script execution starting point
    folder_path = input("Please enter the folder path of the project you want summarized into one file: ")
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # Prepare the output file path on the user's desktop
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        main_folder_name = os.path.basename(folder_path)
        output_file_name = f"{main_folder_name}_detailed_file_list.txt"
        output_file_path = os.path.join(desktop_path, output_file_name)
        
        print(f"Writing detailed file list and contents to {output_file_path}")
        list_files_and_content_to_txt(folder_path, output_file_path)
        print("Done. Detailed file list and contents have been written. Please add additional information manually.")
        
        if os.name == 'nt':  # Automatically open the file in Notepad on Windows
            os.system(f'notepad.exe "{output_file_path}"')
    else:
        print("The path entered does not exist or is not a directory.")
    
    input("Press Enter to exit...")
