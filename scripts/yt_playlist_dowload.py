import yt_dlp
import os

class MyLogger:
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


# See "progress_hooks" in help(yt_dlp.YoutubeDL)
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now post-processing ...')


def download_playlist_audio(playlist_url, output_dir='audio_downloads'):
    """Downloads audio from all videos in a YouTube playlist.
    playlist_url (str): URL of the YouTube playlist.
    output_dir (str, optional): Directory where audio files will be saved. Defaults to 'audio_downloads'. """
    ydl_opts = {
        'format': 'bestaudio/best',  # Choose the best audio quality
        'extract_audio': True,       # Extract audio only
        'audio_format': 'mp3',       # Convert to MP3 format
        'outtmpl': os.path.join(output_dir, '%(title)s.mp3'),  # Output file template
        'embed_thumbnail': True,     # Embed thumbnail in metadata
        'embed_metadata': True,      # Embed additional metadata
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(playlist_url, download=True)
        print(f"Downloaded {len(info_dict['entries'])} audio files to {output_dir}")

# Example usage:
output_dir = ""
playlist_url = ""

download_playlist_audio(playlist_url, output_dir)
