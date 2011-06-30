#!/usr/bin/env python
# $URL$
# $Rev$
#
# run.py
#
# Filipe Fernandes, 2011-06-20

import wx
import sys

class Frame(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'ccc-gistemp',
                size=(600, 400))
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.OnClose, m_exit)
        menuBar.Append(menu, "&File")
        self.statusbar = self.CreateStatusBar()

        # panel
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        m_text = wx.StaticText(panel, -1, "ccc-gistemp")
        m_text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        m_text.SetSize(m_text.GetBestSize())
        box.Add(m_text, 0, wx.ALL, 10)

        log = wx.TextCtrl(panel, wx.ID_ANY, size=(400,400), pos=(150,0),
                          style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)

        # redirect text here
        redir=RedirectText(log)
        sys.stderr=redir
        #sys.stdout=redir

        # run button
        run_button = wx.Button(panel, label="Run!")
        run_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp)
        box.Add(run_button, 0, wx.ALL, 10)

        # close button
        close_button = wx.Button(panel, wx.ID_CLOSE, label="Exit")
        close_button.Bind(wx.EVT_BUTTON, self.OnClose)
        box.Add(close_button, 0, wx.ALL, 10)

        panel.SetSizer(box)
        panel.Layout()

    def OnClose(self, event):
        dlg = wx.MessageDialog(self, "Do you want to close the application?",
                            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()

    def RunCCCgistemp(self, event):
        from CCCgistemp.tool import run
        print "running ccc-gistemp.py"
        run.main()
        #self.Destroy() TODO: some message

    def OnCloseWindow(self, event):
        print "Done!"
        self.Destroy()

class RedirectText(object):
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        self.out.WriteText(string)

if __name__ == '__main__':
    app = wx.App(redirect=False)
    frame = Frame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
