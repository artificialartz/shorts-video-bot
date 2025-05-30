import os
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

def create_video(topic, script):
    # 1. Ses oluştur
    tts = gTTS(text=script, lang='en')
    audio_file = f"{topic}_audio.mp3"
    tts.save(audio_file)

    # 2. Görsel (sabit bir görsel kullan)
    image_file = "default.jpg"

    # 3. Video oluştur
    video_file = f"{topic}_video.mp4"
    image_clip = ImageClip(image_file, duration=10)
    audio_clip = AudioFileClip(audio_file)
    video = image_clip.set_audio(audio_clip)
    video.write_videofile(video_file, fps=24)

    # 4. Google Drive'a yükle
    creds = service_account.Credentials.from_service_account_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/drive']
    )
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {'name': video_file}
    media = MediaFileUpload(video_file, mimetype='video/mp4')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = file.get('id')
    video_url = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"

    # 5. Temizlik
    os.remove(audio_file)
    os.remove(video_file)

    return video_url