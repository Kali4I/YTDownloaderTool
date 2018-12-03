#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""YT Downloader - программа для скачивания музыки и видео с YouTube.
"""

import wx
import os
import sys
from pathlib import Path
from downloader import Downloader

basedir = str(Path.home()) + '/YTDownloader/'

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self, *args, **kwds)

        if getattr(sys, 'frozen', False):
            os.chdir(sys._MEIPASS)

        self.__setup()

        self.SetSize((400, 160))
        self.notebook_1 = wx.Notebook(self, wx.ID_ANY)
        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.text_ctrl_1 = wx.TextCtrl(self.notebook_1_pane_1, wx.ID_ANY, "")
        self.choice_1 = wx.Choice(self.notebook_1_pane_1, wx.ID_ANY, choices=["Музыка", "Видео"])
        self.button_1 = wx.Button(self.notebook_1_pane_1, wx.ID_ANY, "Начать скачивание")
        self.bitmap_button_1 = wx.BitmapButton(self.notebook_1_pane_1, wx.ID_ANY, wx.Bitmap("open_img.png", wx.BITMAP_TYPE_ANY))
        self.notebook_1_ = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.notebook_1_pane_2 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.list_box_1 = wx.ListBox(self.notebook_1_pane_2, wx.ID_ANY,
                                     choices=[x for x in os.listdir(basedir + '/music')])

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.__download, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.__trigger_open_dir, self.bitmap_button_1)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.__trigger_open, self.list_box_1)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.__update_listbox, self.notebook_1)

    def __setup(self):
        """Создаем необходимые папки при запуске, если они отсутствуют"""
        if not os.path.exists(basedir):
            os.makedirs(basedir + '/music')
            os.makedirs(basedir + '/video')

    def __set_properties(self):
        self.SetTitle("YT Downloader | (c) @Рам#6692")
        self.SetIcon(wx.Icon("icon.ico"))
        self.text_ctrl_1.SetMinSize((260, 23))
        self.text_ctrl_1.SetToolTip('Введите название песни сюда')
        self.bitmap_button_1.SetToolTip('Просмотр файлов')
        self.choice_1.SetToolTip('Выберите тип медиа (музыка / видео)')
        self.list_box_1.SetToolTip('Двойной клик по названию начнет воспроизведение')
        self.choice_1.SetMinSize((120, 23))
        self.choice_1.SetSelection(0)
        self.button_1.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.bitmap_button_1.SetMinSize((50, 65))

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(self.text_ctrl_1, 0, 0, 0)
        sizer_3.Add(self.choice_1, 0, 0, 0)
        sizer_2.Add(sizer_3, 1, wx.EXPAND, 0)
        sizer_6.Add(self.button_1, 3, wx.EXPAND, 0)
        sizer_6.Add((0, 0), 0, 0, 0)
        sizer_6.Add((0, 0), 0, 0, 0)
        sizer_6.Add(self.bitmap_button_1, 0, wx.EXPAND, 0)
        sizer_2.Add(sizer_6, 1, wx.EXPAND, 0)
        self.notebook_1_pane_1.SetSizer(sizer_2)
        label_1 = wx.StaticText(self.notebook_1_, wx.ID_ANY, 'Эта программа - некая графическая оболочка для\n'
                                                             ' youtube-dl, которая позволяет\n'
                                                             ' скачивать медиа с YouTube без использования\n'
                                                             ' youtube-dl напрямую через командную строку.\n\n'
                                                             '[!] Скачиваемые форматы аудио могут не\n'
                                                             ' поддерживаться проигрывателем Windows Media!!',
                                                             style=wx.ST_NO_AUTORESIZE)
        label_1.SetBackgroundColour(wx.Colour(25, 25, 25))
        label_1.SetForegroundColour(wx.Colour(243, 243, 243))
        label_1.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Lucida Console"))
        sizer_4.Add(label_1, 1, wx.ALL | wx.EXPAND, 1)
        sizer_5.Add(self.list_box_1, 1, wx.EXPAND, 0)
        self.notebook_1_pane_2.SetSizer(sizer_5)
        self.notebook_1_.SetSizer(sizer_4)
        self.notebook_1.AddPage(self.notebook_1_pane_1, 'Главная')
        self.notebook_1.AddPage(self.notebook_1_pane_2, 'Скачанные треки')
        self.notebook_1.AddPage(self.notebook_1_, 'О программе')
        sizer_1.Add(self.notebook_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
    
    def __trigger_open(self, event):
        """Вызывается при двойном клике по треку в списке внутри программы"""
        os.startfile(basedir + '/music/' + event.GetString())

    def __trigger_open_dir(self, event):
        """Вызывается при нажатии кнопки 'Просмотр файлов'"""
        os.startfile(os.path.dirname(basedir + '/YTDownloader'))

    def __update_listbox(self, event):
        """Обновляем список песен внутри программы"""
        self.list_box_1.Set([x for x in os.listdir(basedir + '/music')])

    def __download(self, event):
        """Скачивание"""
        _name = self.text_ctrl_1.GetValue()
        _type = self.choice_1.GetSelection()
        client = Downloader(self, _name, _type, basedir)
        dialog = wx.MessageDialog(self,
                                  caption='YT Downloader', style=wx.NO|wx.YES,
                                  message='Позвольте спросить...'
                                         f'\n\nСкачиваем "{_name}"?').ShowModal()

        import threading, time

        def attention(msgs, t_=2.3):
            for x in msgs:
                self.button_1.SetLabel(x)
                time.sleep(t_)

        if dialog == wx.ID_NO:
            threading.Thread(target=lambda: attention(['Отменено окда',
                                                       'Начать скачивание'])).start()
            return False
        else:
            threading.Thread(target=lambda: attention(['Загрузка началась...', 
                                                       'По завершению загрузки\nпоявится оповещение.',
                                                       'Начать скачивание'])).start()
        try:
            client.run_download()

        except Exception as e:
            wx.MessageDialog(self,
                             caption='YT Downloader', style=wx.OK|wx.ICON_ERROR,
                             message='Произошла ошибка.\n\n%s %s' % (type(e).__name__, e)).ShowModal()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()