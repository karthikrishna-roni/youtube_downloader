import yt_dlp
import streamlit as st
import os
import subprocess

# Directory to save the downloaded files
SAVE_DIR = './downloads'

def ensure_dir_exists(directory):
    """Ensure the download directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_youtube_media(url, format_id='18', custom_name=None):
    """Download video or audio using the specified format ID and rename if custom_name is provided."""
    ensure_dir_exists(SAVE_DIR)
    filename_template = '%(title)s.%(ext)s' if not custom_name else f'{custom_name}.%(ext)s'
    filename = os.path.join(SAVE_DIR, filename_template)
    ydl_opts = {
        'outtmpl': f'{SAVE_DIR}/%(title)s.%(ext)s',
        'ffmpeg_location': '/path/to/ffmpeg',  # Update this path
    }

    if format_id:
        ydl_opts['format'] = format_id
    else:
        ydl_opts['format'] = 'best'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Find the downloaded file
    files = [f for f in os.listdir(SAVE_DIR) if os.path.isfile(os.path.join(SAVE_DIR, f))]
    if files:
        return os.path.join(SAVE_DIR, files[-1])
    return None

def download_youtube_audio(url, custom_name=None):
    """Download audio from YouTube video and convert to MP3 with optional custom name."""
    ensure_dir_exists(SAVE_DIR)
    filename_template = '%(title)s.%(ext)s' if not custom_name else f'{custom_name}.%(ext)s'
    filename = os.path.join(SAVE_DIR, filename_template)
    ydl_opts = {
        'format': 'bestaudio/best',  # Download best audio format available
        'outtmpl': filename,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Find the downloaded file
    files = [f for f in os.listdir(SAVE_DIR) if os.path.isfile(os.path.join(SAVE_DIR, f))]
    if files:
        return os.path.join(SAVE_DIR, files[-1])
    return None

def main():
    st.title('YouTube Downloader')

    video_url = st.text_input('Enter the YouTube video URL:')
    download_type = st.radio('Select download type:', ['Video', 'Audio'])
    custom_name = st.text_input('Enter a custom name for the file (optional):')

    if download_type == 'Video':
        if st.button('Pull Video'):
            file_path = download_youtube_media(video_url, 'best', custom_name)
            if file_path:
                st.success('Video downloaded successfully!')
                with open(file_path, 'rb') as f:
                    st.download_button(
                        label='Download Video',
                        data=f,
                        file_name=os.path.basename(file_path),
                        mime='video/mp4'  # Adjust MIME type based on actual file type
                    )
            else:
                st.error('Failed to download video.')

    elif download_type == 'Audio':
        if st.button('Pull Audio'):
            file_path = download_youtube_audio(video_url, custom_name)
            if file_path:
                st.success('Audio downloaded successfully!')
                with open(file_path, 'rb') as f:
                    st.download_button(
                        label='Download Audio',
                        data=f,
                        file_name=os.path.basename(file_path),
                        mime='audio/mpeg'  # Adjust MIME type based on actual file type
                    )
            else:
                st.error('Failed to download audio.')

    # Add a button to clear the cache
    if st.button('Clear Cache'):
        st.cache_data.clear()
        st.success("Cache cleared successfully!")

if __name__ == "__main__":
    main()
