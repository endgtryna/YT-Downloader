import yt_dlp
import re
import imageio_ffmpeg as ffmpeg
from logger import logger, spinner

class custom_logger():
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

ffmpeg_path = ffmpeg.get_ffmpeg_exe()

def validate_youtube_link(index, link):
    youtube_regex = (
        r'(https?://)?(www\.|m\.)?'
        r'(youtube\.com|youtu\.be|youtube-nocookie\.com)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    match = re.match(youtube_regex, link)
    if not match:
        logger('error', f"✗{'' if index is None else f' {index}.'} {link} (Invalid Youtube link)")
    return match is not None

def get_metadata(index, link):
    is_valid_youtube_link = validate_youtube_link(index, link)
    if not is_valid_youtube_link:
        return False

    get_metadata_spinner = spinner('info', 'Get metadata...')

    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'logger': custom_logger(),
            'simulate': True,
            'js_runtimes': {'node': {}}
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            metadata = ydl.extract_info(link, download=False)
            if metadata:
                logger('success', f"✓{'' if index is None else f' {index}.'} {metadata['title']}")
                return {
                    'title': metadata.get('title', 'Unkown'),
                    'thumbnail': metadata.get('thumbnail'),
                    'duration': metadata.get('duration')
                }
            return None
    
    except Exception:
        logger('error', f"✗{'' if index is None else f' {index}.'} {link} (Failed get metadata)")
        return None
    
    finally:
        get_metadata_spinner.stop()

def downloader(index, link, type, save_path):
    downloading_spinner = spinner('info', f"Downloading {type}{'...' if index is None else f' {index} ...'}")

    try:
        ydl_opts_video = {
            'quiet': True,
            'no_warnings': True,
            'logger': custom_logger(),
            'format': 'bestvideo+bestaudio/best',
            'ffmpeg_location': ffmpeg_path,
            'merge_output_format': 'mp4',
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'postprocessors': [
                {
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4'
                }
            ]
        }

        ydl_opts_audio = {
            'quiet': True,
            'no_warnings': True,
            'logger': custom_logger(),
            'format': 'bestaudio/best',
            'ffmpeg_location': ffmpeg_path,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192'
                },
                {
                    'key': 'FFmpegMetadata',
                    'add_metadata': True
                }
            ],
            'outtmpl': f'{save_path}/%(title)s.%(ext)s'
        }

        with yt_dlp.YoutubeDL(ydl_opts_video if type == 'video' else ydl_opts_audio) as ydl:
            ydl.download([link])

        logger('success', f"✓ {type.capitalize()}{'' if index is None else f' {index}'} downloaded successfully")
        return True

    except Exception:
        logger('error', f"✗ Failed to download {type}{'' if index is None else f' {index}'}")
        return False
    
    finally:
        downloading_spinner.stop()
    