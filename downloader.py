#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import youtube_dl
import threading
import wx

class Downloader:
    """Главный класс штуки, которая скачивает музыку и видео с YT"""
    def __init__(self, parent, name, mediatype, basedir):
        self.parent = parent
        self.name = name
        self.mediatype = mediatype

        self.video_opts = {
            'default_search': 'auto',
            'quiet': True,
            'videoformat': 'mp4',
            'outtmpl': basedir + '/video/%(title)s.%(ext)s'
        }

        self.music_opts = {
            'default_search': 'auto',
            'quiet': True,
            'extractaudio': True,
            'audioformat': 'mp3',
            'format': 'bestaudio/best',
            'outtmpl': basedir + '/music/%(title)s.%(ext)s',
            'noplaylist': False
        }

    def run_download(self):
        """Начинаем скачивание"""
        def start():
            if self.mediatype == 1:
                with youtube_dl.YoutubeDL(self.video_opts) as ydl:
                    try:
                        ydl.download([self.name])
                    except youtube_dl.utils.DownloadError:
                        wx.MessageDialog(self.parent,
                         caption='YT Downloader', style=wx.OK|wx.CENTRE|wx.ICON_INFORMATION,
                         message=f'Не удалось загрузить "{self.name}".'
                                  '\n\nЕсли вы ввели название, уберите оттуда эти символы -> :\\/').ShowModal()
                        return False

            if self.mediatype == 0:
                with youtube_dl.YoutubeDL(self.music_opts) as ydl:
                    try:
                        ydl.download([self.name])
                    except youtube_dl.utils.DownloadError:
                        wx.MessageDialog(self.parent,
                         caption='YT Downloader', style=wx.OK|wx.CENTRE|wx.ICON_INFORMATION,
                         message=f'Не удалось загрузить "{self.name}".'
                                  '\n\nЕсли вы ввели название, уберите оттуда эти символы -> :\\/').ShowModal()
                        return False

            wx.MessageDialog(self.parent,
                         caption='YT Downloader', style=wx.OK|wx.CENTRE|wx.ICON_INFORMATION,
                         message='Готово.'
                                 f'\n\n"{self.name}" загружен на компьютер.').ShowModal()

        thread = threading.Thread(target=start, args=())
        thread.start()