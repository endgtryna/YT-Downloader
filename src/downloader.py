import yt_dlp
import re
import imageio_ffmpeg as ffmpeg
from rich.progress import Progress, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
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

def downloader(index, link, type, save_path, resolution='720'):
    label = f"{type}{'' if index is None else f' {index}'}"
    download_count = [0]

    with Progress(
        '[info]{task.description}',
        BarColumn(),
        '[progress.percentage]{task.percentage:>3.0f}%',
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        transient=True
    ) as progress:
        task = progress.add_task(f'Downloading {label}...', total=None)

        def progress_hook(d):
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded = d.get('downloaded_bytes', 0)
                if total:
                    progress.update(task, total=total, completed=downloaded)
            elif d['status'] == 'finished':
                download_count[0] += 1
                if type == 'video' and download_count[0] == 1:
                    progress.update(task, description=f'Downloading audio (merging)...', total=None, completed=0)

        fmt_video = (
            f'bestvideo[vcodec^=avc][height<={resolution}]+bestaudio[acodec^=mp4a]/bestvideo[vcodec^=avc][height<={resolution}]+bestaudio/bestvideo[height<={resolution}]+bestaudio[acodec^=mp4a]/bestvideo[height<={resolution}]+bestaudio'
            if resolution != 'best'
            else 'bestvideo[vcodec^=avc]+bestaudio[acodec^=mp4a]/bestvideo[vcodec^=avc]+bestaudio/bestvideo+bestaudio[acodec^=mp4a]/bestvideo+bestaudio'
        )

        ydl_opts_video = {
            'quiet': True,
            'no_warnings': True,
            'logger': custom_logger(),
            'format': fmt_video,
            'ffmpeg_location': ffmpeg_path,
            'merge_output_format': 'mp4',
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],
            'postprocessors': [
                {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'},
                {'key': 'FFmpegVideoRemuxer', 'preferedformat': 'mp4'}
            ]
        }

        ydl_opts_audio = {
            'quiet': True,
            'no_warnings': True,
            'logger': custom_logger(),
            'format': 'bestaudio/best',
            'ffmpeg_location': ffmpeg_path,
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
                {'key': 'FFmpegMetadata', 'add_metadata': True}
            ]
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts_video if type == 'video' else ydl_opts_audio) as ydl:
                ydl.download([link])
            logger('success', f"✓ {label.capitalize()} downloaded successfully")
            return True
        except Exception:
            logger('error', f"✗ Failed to download {label}")
            return False