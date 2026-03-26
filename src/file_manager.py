import os
from logger import logger, spinner

def folder_exists(path):
    check_folder_exists_spinner = spinner('info', 'Check folder exists...')
    is_folder_exists = os.path.isdir(os.path.expanduser(path))
    check_folder_exists_spinner.stop()
    if not is_folder_exists:
        logger('error', 'Folder not found.')
        return False
    return True

def file_exists(path):
    check_file_exists_spinner = spinner('info', 'Check file exists...')
    is_file_exists = os.path.isfile(os.path.expanduser(path))
    check_file_exists_spinner.stop()
    if not is_file_exists:
        logger('error', 'File not found.')
        return False
    return True

def read_file(path):
    read_file_spinner = spinner('info', 'Reading file...')
    try:
        with open(os.path.expanduser(path), 'r') as file:
            file_contents = [link.strip() for link in file if link.strip()]
            if not file_contents:
                logger('error', 'File empty.')
                return False
            return file_contents
        
    except Exception:
        logger('error', 'Failed to read file.')
        return False
    
    finally:
        read_file_spinner.stop()