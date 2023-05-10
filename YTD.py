import PySimpleGUI as sg
import os
import subprocess

sg.theme('BluePurple')
layout = [[sg.Text('YouTube Downloader')],
                [sg.Text('Playlist or Video URL'), sg.InputText()],
                [sg.Text('Path'), sg.In(), sg.FolderBrowse(target=(2, 1))],
                [sg.Submit(), sg.Exit(), sg.Checkbox('mp3', default=False, key="-FILEFORMATSELECTOR-")]]

window = sg.Window('YouTube Downloader', layout, size=(250, 130), default_element_size=(12,1), resizable=True)

while True:
    event, values = window.read()
    purl = values[0]
    path = values[1]
    if values["-FILEFORMATSELECTOR-"] == True:
        cmd = 'yt-dlp -x --audio-format mp3 ' + purl
    else:
        cmd = 'yt-dlp -S res,ext:mp4:m4a --recode mp4 ' + purl
    if event in (sg.WIN_CLOSED, 'Submit'):
        if "watch" or "playlist" in purl:
            os.chdir(path)
            os.system(cmd)
            sg.popup('Done!')
        else:
            sg.popup('Link Not Compatable')
    elif event in (sg.WIN_CLOSED, 'Exit'):
        window.close()