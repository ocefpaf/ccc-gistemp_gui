#!/usr/bin/env python
# $URL$
# $Rev$
#
# run.py
#
# Filipe Fernandes, 2011-06-20

import wx
import sys
import subprocess

class InsertFrame(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'run button',
                size=(300, 100))

        panel = wx.Panel(self)
        button = wx.Button(panel, label="run", pos=(125, 10), size=(50, 50))
        self.Bind(wx.EVT_BUTTON, self.RunCCCgistemp, button)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def RunCCCgistemp(self, event):
        print "running ccc-gistemp.py" # need to be able to import and then run!
                                       # the current way requires a separated
                                       # CCCgistemp installation.
        subprocess.check_call('ccc-gistemp.py')

    def OnCloseWindow(self, event):
        print "Done!"
        self.Destroy()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = InsertFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()