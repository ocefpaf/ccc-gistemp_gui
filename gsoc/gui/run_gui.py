#!/usr/bin/env python
# $URL$
# $Rev$
#
# run_gui.py
#
# Filipe Fernandes, 2011-06-20

import wx
import sys
from CCCgistemp.tool import run

WIDHT, HEIGHT = 900, 600
header_w,  header_h = 900, 150
header_file = 'ccf-header.jpg'

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

        # panel
        panel = wx.Panel(self, size=(WIDHT, HEIGHT))
        panel.SetBackgroundColour(wx.WHITE)
        picture = wx.StaticBitmap(panel)
        image = wx.Image(header_file, wx.BITMAP_TYPE_PNG)
        picture.SetBitmap(wx.Bitmap(header_file))

        log = wx.TextCtrl(panel, wx.ID_ANY, size=(WIDHT-110, HEIGHT-header_h), pos=(90, header_h),
                          style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)

        # redirect text here
        sys.stderr = RedirectText(log)
        sys.stdout = RedirectText(log)

        # buttons
        offset = 30
        run_button = wx.Button(panel, label='Run', pos=(0, header_h+offset))
        stp0_button = wx.Button(panel, label="Step 0", pos=(0, header_h+ 2*offset))
        close_button = wx.Button(panel, wx.ID_CLOSE, label="Exit", pos=(0, header_h+3*offset))

        # actions
        run_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp)
        stp0_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp_step0)
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

    def RunCCCgistemp_step0(self, event):
        print "running ccc-gistemp.py step 0\n"
        data = run.main(argv=['-s 0'])
        #self.Destroy() TODO: Add some "I'm done" message here...

    def OnCloseWindow(self, event):
        print "Done!"
        self.Destroy()

def main():
    app = App(redirect=False)
    frame = Frame()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
