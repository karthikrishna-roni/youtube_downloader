import yt_dlp
import streamlit as st
import os
import time

# Directory to save the downloaded files
SAVE_DIR = './downloads'

def ensure_dir_exists(directory):
    """Ensure the download directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def clear_download_directory(directory):
    """Remove all files in the download directory."""
    for f in os.listdir(directory):
        file_path = os.path.join(directory, f)
        if os.path.isfile(file_path):
            os.remove(file_path)

def generate_unique_filename(title, ext):
    """Generate a unique filename using the title and a timestamp."""
    timestamp = int(time.time())
    return f"{title}_{timestamp}.{ext}"

def download_youtube_media(url, format_id='18', custom_name=None):
    """Download video or audio using the specified format ID and rename if custom_name is provided."""
    ensure_dir_exists(SAVE_DIR)
    clear_download_directory(SAVE_DIR)  # Clear old files
    
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
    title = None
    files = os.listdir(SAVE_DIR)
    for f in files:
        if f.endswith('.mp4') or f.endswith('.mkv') or f.endswith('.webm'):  # Add other video formats if needed
            title, ext = os.path.splitext(f)
            ext = ext[1:]  # remove the dot
            break
    else:
        return None

    new_filename = generate_unique_filename(title, ext)
    new_filepath = os.path.join(SAVE_DIR, new_filename)
    
    os.rename(os.path.join(SAVE_DIR, f"{title}.{ext}"), new_filepath)

    return new_filepath

def download_youtube_audio(url, custom_name=None):
    """Download audio from YouTube video and convert to MP3 with optional custom name."""
    ensure_dir_exists(SAVE_DIR)
    clear_download_directory(SAVE_DIR)  # Clear old files
    
    ydl_opts = {
        'format': 'bestaudio/best',  # Download best audio format available
        'outtmpl': f'{SAVE_DIR}/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Find the downloaded file
    title = None
    files = os.listdir(SAVE_DIR)
    for f in files:
        if f.endswith('.mp3') or f.endswith('.webm'):  # Add other audio formats if needed
            title, ext = os.path.splitext(f)
            ext = ext[1:]  # remove the dot
            break
    else:
        return None

    new_filename = generate_unique_filename(title, ext)
    new_filepath = os.path.join(SAVE_DIR, new_filename)
    
    os.rename(os.path.join(SAVE_DIR, f"{title}.{ext}"), new_filepath)

    return new_filepath

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

if __name__ == "__main__":
    main()
