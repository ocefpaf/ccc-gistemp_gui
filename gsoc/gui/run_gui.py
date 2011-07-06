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
import notify # from phatch TODO: url
from CCCgistemp.tool import run
from gui.lib import notify

# Constants
WIDHT, HEIGHT = 900, 600
header_w,  header_h = 900, 150

def get_setup():
    if hasattr(sys, 'frozen'):
        frozen = getattr(sys, 'frozen', '')
        return frozen
    elif is_packaged(): # linux
        return 'packaged'
    return 'source'

def is_packaged():
    """For linux only"""
    return not sys.argv[0].endswith('.py')

"""
open with default app
if hasattr(os, 'startfile'):# windows
    os.startfile(path)
else:
    if sys.platform.startwith('darwin'): # mac
        command = 'open'
    else: # linux
        command = 'xdg-open'
    subprocess.call([command, path])
"""

# Paths
if get_setup() == 'source':
    # not frozen
    approot = os.path.dirname(__file__)
elif frozen in ('dll', 'console_exe', 'windows_exe'):
    # py2exe
    approot = os.path.dirname(sys.executable)
    #approot = os.path.dirname(
        #unicode(sys.)xecutable, sys.getfilesystemencoding())
elif frozen in ('macosx_app',):
    # py2app
    approot = os.environ['RESOURCEPATH']
elif get_setup() == 'package':
    pass # linux

header_file = os.path.join(approot, 'ccf-header.png')
ico = os.path.join(approot, 'ccf.ico')

class RedirectText(object):
    """Redirect text to a wxTextCtrl frame."""

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

        # main panel
        panel = wx.Panel(self, size=(WIDHT, HEIGHT))
        panel.SetBackgroundColour(wx.WHITE)
        picture = wx.StaticBitmap(panel)
        image = wx.Image(header_file, wx.BITMAP_TYPE_PNG)
        picture.SetBitmap(wx.Bitmap(header_file))

        log = wx.TextCtrl(panel, wx.ID_ANY, size=(WIDHT-2*90, HEIGHT-header_h),
                          pos=(90, header_h), style = wx.TE_MULTILINE|
                          wx.TE_READONLY|wx.HSCROLL)

        # redirect text here
        sys.stderr = RedirectText(log)
        sys.stdout = RedirectText(log)

        # buttons
        offset = 30
        run_button = wx.Button(panel, label='Run', pos=(0, header_h+offset))
        stp0_button = wx.Button(panel, id=0, label="Step 0",
                                pos=(0, header_h + 3*offset))
        stp1_button = wx.Button(panel, id=1, label="Step 1",
                                pos=(0, header_h + 4*offset))
        stp2_button = wx.Button(panel, id=2, label="Step 2",
                                pos=(0, header_h + 5*offset))
        stp3_button = wx.Button(panel, id=3, label="Step 3",
                                pos=(0, header_h + 6*offset))
        stp4_button = wx.Button(panel, id=4, label="Step 4",
                                pos=(0, header_h + 7*offset))
        stp5_button = wx.Button(panel, id=5, label="Step 5",
                                pos=(0, header_h + 8*offset))
        stp6_button = wx.Button(panel, id=6, label="Step 6",
                                pos=(0, header_h + 9*offset))
        close_button = wx.Button(panel, wx.ID_CLOSE, label="Exit", 
                                 pos=(0, header_h + 11*offset))
        dir_button = wx.Button(panel, id=-1,
                               label='Project',
                               pos=(WIDHT-88, header_h+offset))

        # buttons actions
        run_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp)
        stp0_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp_steps)
        stp1_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp_steps)
        stp2_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp_steps)
        stp3_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp_steps)
        stp4_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp_steps)
        stp5_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp_steps)
        stp6_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp_steps)
        close_button.Bind(wx.EVT_BUTTON, self.OnClose)
        dir_button.Bind(wx.EVT_BUTTON, self.onDir)
        
        panel.Layout()
        
        self.WORK_DIR = False # constant to check for working directory.

    def OnClose(self, event):
        """Close confirmation."""
        dlg = wx.MessageDialog(self, "Do you want to close the application?",
                            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()

    def showMessageDlg(self, msg, title, style):
        """Dialog messages."""
        dlg = wx.MessageDialog(parent=None, message=msg,
                               caption=title, style=style)
        dlg.ShowModal()
        dlg.Destroy()
 
    def RunCCCgistemp(self, event):
        """Full ccc-gistemp run."""
        if not self.WORK_DIR:
            self.showMessageDlg("You must choose/create a project directory",
                                "Information", wx.OK|wx.ICON_INFORMATION)
            self.proj_dir()
            self.run()
        else:
            self.run()

    def RunCCCgistemp_steps(self, event):
        """Run steps."""
        step = event.GetId() #FIXME: dangerous use of id, find a better way...
        print("running ccc-gistemp.py step %s\n" % step)
        run.main(argv=['dummy','-s', str(step)])
        print("\nFinished step %s\n" % step)
    
    def run(self):
        """call tool/run.py"""
        notify.send(title='ccc-gistemp',
                    message='running ccc-gistemp',
                    icon=ico)
        #run.main()
        notify.send(title='ccc-gistemp',
                    message='Finished ccc-gistemp run',
                    icon=ico)

    def proj_dir(self):
        """Create a project directory and change to it."""
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE| wx.DD_CHANGE_DIR)

        if dlg.ShowModal() == wx.ID_OK:
            print "project directory:\n\t%s" % dlg.GetPath()
            self.WORK_DIR = True
        else:
            self.WORK_DIR = False
        
        dlg.Destroy()
        return self.WORK_DIR

    def onDir(self, event):
        """ Button to change/create project directory."""
        self.proj_dir()

def main():
    app = App(redirect=False)
    frame = Frame()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
