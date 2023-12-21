from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from pytube import YouTube
import os
import pickle
import sys 
import os 


def get_creds():
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', ['https://www.googleapis.com/auth/youtube.readonly'])
        try:
            creds = flow.run_local_server(port=0)
        except KeyboardInterrupt:
            print('Упс! Keyboard Interrupted или что-то сломалось на этапе авторизации :( Попробуй снова позже.')

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def get_playlist_info_by_id(id, topkitems):
    creds = get_creds()
    youtube = build('youtube', 'v3', credentials=creds)
    playlist_items = youtube.playlistItems().list(
            part='snippet',
            playlistId=id,
            maxResults=topkitems  
        ).execute()
    items = []
    for item in playlist_items['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            items.append((video_url))
    return items


def download_audio(audio_url):
    yt = YouTube(str(audio_url)) 
    audio = yt.streams.filter(only_audio=True).first() 
    print("Введи путь для скачивания (оставь поле пустым для текущей директории)") 
    destination = str(input(">> ")) or '.'
    out_file = audio.download(output_path=destination) 
    base, ext = os.path.splitext(out_file) 
    new_file = base + '.mp3'
    os.rename(out_file, new_file) 
    print(f"«{yt.title}» успешно сохранен(о) в формате mp3.")


def download_video(video_url): 
    yt = YouTube(str(video_url))
    video = yt.streams.get_highest_resolution()
    print("Введи путь для скачивания (оставь поле пустым для текущей директории)") 
    destination = str(input(">> ")) or '.'
    out_file = video.download(output_path=destination) 
    base, ext = os.path.splitext(out_file) 
    new_file = base + '.mp4'
    os.rename(out_file, new_file) 
    print(f"«{yt.title}» успешно сохранен(о) в формате mp4.")


if __name__ == "__main__":
    items_to_download = []
    print("Hey there!")
    one_or_playlist = input("Хочешь воспользоваться возможностью скачивания из плейлиста? y/n ")
    if one_or_playlist == 'y':
        playlist_id = input("Введи id плейлиста: ")
        topkitems = input("Введи кол-во видео/аудио для скачивания: ")
        for item in get_playlist_info_by_id(playlist_id, topkitems):
            items_to_download.append(item)
    elif one_or_playlist == 'n':
        id = input("Введи id видео/аудио: ")
        url = f'https://www.youtube.com/watch?v={id}'
        items_to_download.append(url)
    else:
        print("Упс! Кажется, вы ввели некорректные опции. Попробуйте снова.")
        sys.exit()
    
    video_or_audio = input("Хочешь скачать материалы в формате mp4 (видео) или mp3 (аудио)? v/a ")
    if video_or_audio == 'v':
        for item in items_to_download:
            download_video(item)
    else:
        for item in items_to_download:
            download_audio(item)
