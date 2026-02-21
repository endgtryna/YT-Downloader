import sys
from logger import logger
from downloader import get_metadata
from file_manager import file_exists, read_file, folder_exists

def prompt_mode():
    logger('primary', 'Mode:\n1. Single download\n2. Bulk download')
    while True:
        user_input = input('Choose your option (1, 2): ').strip()
        if user_input in ['1', '2']:
            return user_input
        logger('error', 'Bad option, please choose again.')

def prompt_source(mode):
    if mode == 'single':
        while True:
            user_input = input('Youtube link: ').strip()
            metadata = get_metadata(None, user_input)
            if not metadata:
                continue
            return user_input
    else:
        while True:
            user_input = input('File path: ').strip()
            
            is_file_exists = file_exists(user_input)
            if not is_file_exists:
                continue

            file_contents = read_file(user_input)
            if not file_contents:
                continue

            valid_urls = []
            for index, link in enumerate(file_contents, 1):
                metadata = get_metadata(index, link)
                if not metadata:
                    continue
                valid_urls.append(link)

            if not valid_urls:
                logger('error', f'{len(valid_urls)}/{len(file_contents)} valid URLS')
                logger('error', 'Stopped...')
                sys.exit()
            logger('success', f'{len(valid_urls)}/{len(file_contents)} valid URLS')
            return valid_urls

def prompt_download_type():
    logger('primary', 'Download type:\n1. Video\n2. Audio')
    while True:
        user_input = input('Choose download type (1, 2): ').strip()
        if user_input in ['1', '2']:
            return user_input
        logger('error', 'Bad option, please choose again.')

def prompt_save_path():
    while True:
        user_input = input('Save path. Empty to use default (~/Downloads): ').strip()
        
        is_folder_exists = folder_exists('~/Downloads' if not user_input else user_input)
        if not is_folder_exists:
            continue
        return user_input

def prompts():
    user_prompt_mode = prompt_mode()
    mode = 'single' if user_prompt_mode == '1' else 'bulk'

    user_prompt_source = prompt_source(mode)
    
    user_prompt_download_type = prompt_download_type()
    type = 'video' if user_prompt_download_type == '1' else 'audio'

    user_prompt_save_path = prompt_save_path()
    save_path = '~/Downloads' if not user_prompt_save_path else user_prompt_save_path

    return {
        'mode': mode,
        'sources': user_prompt_source,
        'type': type,
        'save_path': save_path
    }
