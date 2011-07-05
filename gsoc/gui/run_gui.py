#!/usr/bin/env python
# $URL$
# $Rev$
#
# run_gui.py
#
# Filipe Fernandes, 2011-06-20

import wx
import sys
import os
from CCCgistemp.tool import run

path = os.path.dirname(__file__)

WIDHT, HEIGHT = 900, 600
header_w,  header_h = 900, 150
header_file = os.path.join(path, 'ccf-header.jpg')
ico = os.path.join(os.path.split(path)[0], 'ccf.ico')

class RedirectText(object):

    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        wx.CallAfter(self.out.WriteText, string)
        wx.Yield()

    def flush(self):
        wx.Yield()
        pass

class App(wx.App):
    """Application class."""
    #TODO: directory check, name run, and etc...
    pass


class Frame(wx.Frame):

    def __init__(self, parent=None, id=-1):
        wx.Frame.__init__(self, parent, id=-1, title='ccc-gistemp',
                size=(WIDHT, HEIGHT), pos=wx.DefaultPosition)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # top left icon
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(wx.Bitmap(ico, wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

        # panel
        panel = wx.Panel(self, size=(WIDHT, HEIGHT))
        panel.SetBackgroundColour(wx.WHITE)
        picture = wx.StaticBitmap(panel)
        image = wx.Image(header_file, wx.BITMAP_TYPE_PNG)
        picture.SetBitmap(wx.Bitmap(header_file))

        log = wx.TextCtrl(panel, wx.ID_ANY, size=(WIDHT-110, HEIGHT-header_h),
                          pos=(90, header_h), style = wx.TE_MULTILINE|
                          wx.TE_READONLY|wx.HSCROLL)

        # redirect text here
        sys.stderr = RedirectText(log)
        sys.stdout = RedirectText(log)

        # buttons
        offset = 30
        run_button = wx.Button(panel, label='Run', pos=(0, header_h+offset))
        stp0_button = wx.Button(panel, id=0, label="Step 0", pos=(0, header_h 
                                                                  + 3*offset))
        stp1_button = wx.Button(panel, id=1, label="Step 1", pos=(0, header_h 
                                                                  + 4*offset))
        stp2_button = wx.Button(panel, id=2, label="Step 2", pos=(0, header_h 
                                                                  + 5*offset))
        stp3_button = wx.Button(panel, id=3, label="Step 3", pos=(0, header_h 
                                                                  + 6*offset))
        stp4_button = wx.Button(panel, id=4, label="Step 4", pos=(0, header_h 
                                                                  + 7*offset))
        stp5_button = wx.Button(panel, id=5, label="Step 5", pos=(0, header_h 
                                                                  + 8*offset))
        stp6_button = wx.Button(panel, id=6, label="Step 6", pos=(0, header_h 
                                                                  + 9*offset))
        close_button = wx.Button(panel, wx.ID_CLOSE, label="Exit", 
                                 pos=(0, header_h + 11*offset))

        # actions
        run_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp)
        stp0_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp_steps)
        stp1_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp_steps)
        stp2_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp_steps)
        stp3_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp_steps)
        stp4_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp_steps)
        stp5_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp_steps)
        stp6_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp_steps)
        close_button.Bind(wx.EVT_BUTTON, self.OnClose)

        panel.Layout()

    def OnClose(self, event):
        dlg = wx.MessageDialog(self, "Do you want to close the application?",
                            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()

    def RunCCCgistemp(self, event):
        print "running ccc-gistemp.py\n"
        run.main()
        #self.Destroy() TODO: Add some "I'm done" message here...

    def RunCCCgistemp_steps(self, event):
        step = event.GetId() #FIXME: dangerous use of id, find a better way...
        print("running ccc-gistemp.py step %s\n" % step)
        run.main(argv=['dummy','-s', str(step)])
        print("\nFinished step %s\n" % step)

def main():
    app = App(redirect=False)
    frame = Frame()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
