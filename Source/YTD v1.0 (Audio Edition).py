import PySimpleGUI as sg
import os
import subprocess

sg.theme('BluePurple')
layout = [[sg.Text('YouTube Downloader')],
                [sg.Text('Playlist or Video URL'), sg.InputText()],
                [sg.Text('Path'), sg.In(), sg.FolderBrowse(target=(2, 1))],
                [sg.Submit(), sg.Exit()]]

window = sg.Window('YouTube Downloader', layout, size=(250, 130), default_element_size=(12,1), resizable=True)

while True:
    event, values = window.read()
    purl = values[0]
    path = values[1]
    if event in (sg.WIN_CLOSED, 'Submit'):
        if "watch" in purl:
            import pytube
            link = purl
            yt = pytube.YouTube(link)
            yt.streams.get_highest_resolution().download(path)
            sg.popup('Done!')
        elif "playlist" in purl:
            import re
            from pytube import Playlist

            YOUTUBE_STREAM_AUDIO = '140'
            DOWNLOAD_DIR = path

            playlist = Playlist(purl)

            playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

            print("Downloading", len(playlist.video_urls), "video(s)...")

            for url in playlist.video_urls:
                print(url)

            for video in playlist.videos:
                audioStream = video.streams.get_by_itag(YOUTUBE_STREAM_AUDIO)
                audioStream.download(output_path=DOWNLOAD_DIR)
            os.chdir(path)
            os.system('for %i in (*.mp4) do ffmpeg -i "%i" "%~ni.mp3')

            test = os.listdir(path)

            for item in test:
                if item.endswith(".mp4"):
                    os.remove(os.path.join(path, item))
                    
            sg.popup('Done!')
        else:
            sg.popup('Link Not Compatable')
    elif event in (sg.WIN_CLOSED, 'Exit'):
        break