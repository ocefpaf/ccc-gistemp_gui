#!/usr/bin/env python
# $URL$
# $Rev$
#
# run_gui.py
#
# Filipe Fernandes, 2011-06-20

# http://www.wxpython.org/onlinedocs.php
import wx
# http://www.python.org/doc/2.4.4/lib/module-sys.html
import sys
# http://docs.python.org/release/2.4.4/lib/module-os.path.html
import os
# TODO
from CCCgistemp.tool import run
# http://bazaar.launchpad.net/~stani/phatch/trunk/view/head:/phatch/lib/notify.py
# TODO: need to add the license
from gui.lib import notify

# Constants
WIDHT, HEIGHT = 900, 600
header_w, header_h = 900, 150

# Packaging stuff. NOTE: Maybe this should be moved to lib...
def get_setup():
    """
    Return information if the App is being called from a linux package,
    frozen (py2exe or py2app), or from source.
    """
    if hasattr(sys, 'frozen'):
        frozen = getattr(sys, 'frozen', '')
        return frozen
    elif is_packaged(): # linux
        return 'packaged'
    return 'source'

def is_packaged():
    """Return True if the App is packaged (linux only)."""
    return not sys.argv[0].endswith('.py')

# Get approot directory.
setup = get_setup()
if setup == 'source':
    approot = os.path.dirname(__file__) # not frozen
elif setup in ('dll', 'console_exe', 'windows_exe'):
    approot = os.path.dirname(sys.executable) # py2exe
    #approot = os.path.dirname(
        #unicode(sys.)xecutable, sys.getfilesystemencoding())
elif setup in ('macosx_app',):
    approot = os.environ['RESOURCEPATH'] # py2app
elif get_setup() == 'package':
    pass # linux

"""
# I'll need this to launch default application when opening a file
if hasattr(os, 'startfile'):# windows
    os.startfile(path)
else:
    if sys.platform.startwith('darwin'): # mac
        command = 'open'
    else: # linux
        command = 'xdg-open'
    subprocess.call([command, path])
"""

# Icons and figures directory
header_file = os.path.join(approot, 'resources/ccf-header.png')
ico = os.path.join(approot, 'resources/ccf.ico')
splash = os.path.join(approot, 'resources/splash.png')

# Frame class
class Frame(wx.Frame):

    def __init__(self, parent=None, id=-1):
        wx.Frame.__init__(self, parent, id=-1, title='ccc-gistemp',
                          size=(WIDHT, HEIGHT), pos=wx.DefaultPosition)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # top left icon
        icon = wx.Icon(name=ico, type=wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # main panel
        self.panel = wx.Panel(self, size=(WIDHT, HEIGHT))
        self.panel.SetBackgroundColour(wx.WHITE)
        picture = wx.StaticBitmap(self.panel)
        image = wx.Image(header_file, wx.BITMAP_TYPE_PNG)
        picture.SetBitmap(wx.Bitmap(header_file))

        log = wx.TextCtrl(self.panel, wx.ID_ANY,
                          size=(WIDHT-2*90, HEIGHT-header_h-20),
                          pos=(90, header_h),
                          style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL
                         )

        # Create hyper link for the source code.
        url='http://code.google.com/p/ccc-gistemp/'
        link = wx.HyperlinkCtrl(parent=self.panel, id=-1, label='source code',
                                url=url, pos=(WIDHT-80, HEIGHT-20)
                               )

        # Gauge.
        self.timer = wx.Timer(self, 1)
        self.count = 0
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

        self.gauge = wx.Gauge(parent=self.panel, id=-1, range=50,
                              size=(WIDHT-2*90, 20), pos=(90, HEIGHT-20)
                             )

        # Redirect text here.
        sys.stderr = RedirectText(log)
        sys.stdout = RedirectText(log)

        # Buttons.
        offset = 30
        run_button = wx.Button(self.panel, label='Run',
                               pos=(0, header_h+offset))
        stp0_button = wx.Button(self.panel, id=0, label="Step 0",
                                pos=(0, header_h + 3*offset))
        stp1_button = wx.Button(self.panel, id=1, label="Step 1",
                                pos=(0, header_h + 4*offset))
        stp2_button = wx.Button(self.panel, id=2, label="Step 2",
                                pos=(0, header_h + 5*offset))
        stp3_button = wx.Button(self.panel, id=3, label="Step 3",
                                pos=(0, header_h + 6*offset))
        stp4_button = wx.Button(self.panel, id=4, label="Step 4",
                                pos=(0, header_h + 7*offset))
        stp5_button = wx.Button(self.panel, id=5, label="Step 5",
                                pos=(0, header_h + 8*offset))
        stp6_button = wx.Button(self.panel, id=6, label="Step 6",
                                pos=(0, header_h + 9*offset))
        close_button = wx.Button(self.panel, wx.ID_CLOSE, label="Exit",
                                 pos=(0, header_h + 11*offset))
        dir_button = wx.Button(self.panel, id=-1,
                               label='Project',
                               pos=(WIDHT-88, header_h+offset))

        # Button action.
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

        self.panel.Layout()

        self.WORK_DIR = False # constant to check for working directory.

    def OnStop(self, event):
        """Gauge stuff."""
        #FIXME
        if self.count == 0 or self.count >= 50 or not self.timer.IsRunning():
            return
        self.timer.Stop()
        self.text.SetLabel("Task Interrupted")
        wx.Bell()

    def OnTimer(self, event):
        """Gauge stuff."""
        #FIXME
        self.count = self.count +1
        self.gauge.SetValue(self.count)
        if self.count == 50:
            self.timer.Stop()
            self.text.SetLabel("Task Completed")

    def OnClose(self, event):
        """Close confirmation."""
        dlg = wx.MessageDialog(self, "Do you want to close the application?",
                            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            wx.CallAfter(self.Destroy())

    def showMessageDlg(self, msg, title, style):
        """Dialog messages."""
        dlg = wx.MessageDialog(parent=None, message=msg,
                               caption=title, style=style)
        dlg.ShowModal()
        dlg.Destroy()

    def check_dir(self):
        """Check if in a working directory.
        If not create one and change to it.
        """
        if not self.WORK_DIR:
            self.showMessageDlg("You must choose or create a project directory",
                                "Information", wx.OK|wx.ICON_INFORMATION)
            self.WORK_DIR = self.proj_dir()
            return self.WORK_DIR
        else:
            return self.WORK_DIR

    def RunCCCgistemp(self, event):
        """Full ccc-gistemp run."""
        if self.check_dir():
            notify.send(title='ccc-gistemp',
                        message='running ccc-gistemp',
                        icon=ico)
            if self.count >= 50:
                return
            self.timer.Start(100)
            #process = wx.Process()
            #pid = wx.Execute(run.main(), wx.EXEC_ASYNC, process)
            #run.main()
            notify.send(title='ccc-gistemp',
                        message='Finished ccc-gistemp run',
                        icon=ico)

    def RunCCCgistemp_steps(self, event):
        """Run steps."""
        step = event.GetId() #FIXME: dangerous use of id, find a better way...
                             #TODO: add a check for each step
        if self.check_dir():
            notify.send(title='ccc-gistemp',
                        message=('running ccc-gistemp step %s' % step),
                        icon=ico)
            run.main(argv=['dummy','-s', str(step)])
            notify.send(title='ccc-gistemp',
                        message=('Finished ccc-gistemp step %s' % step),
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
        self.WORK_DIR = self.proj_dir()
        return self.WORK_DIR

# Other classes.
class RedirectText(object):
    """Redirect text to a wxTextCtrl frame."""

    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        wx.CallAfter(self.out.WriteText, string)
        wx.Yield()

    def flush(self):
        """ Sometimes stdout is called with the flush() method."""
        wx.Yield()
        pass

class MySplashScreen(wx.SplashScreen):
    """Create a splash screen widget.
    """
    def __init__(self, parent=None):
        # This is a recipe to a the screen.
        bitmap = wx.Bitmap(splash, wx.BITMAP_TYPE_PNG)
        shadow = wx.WHITE
        splashStyle = wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT
        splashDuration = 1000 # milliseconds
        wx.SplashScreen.__init__(self, bitmap, splashStyle,
                                 splashDuration, parent)
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        wx.Yield()

    def OnExit(self, event):
        self.Hide()
        MyFrame = Frame()
        app.SetTopWindow(MyFrame)
        MyFrame.Show(True)
        # The program will freeze without this line.
        event.Skip()

# Application class
class App(wx.App):
    """Application class."""
    def OnInit(self):
        MySplash = MySplashScreen()
        MySplash.Show()
        return True

#NOTE: I do not know why the splash screen does not work when using main()
app = App(redirect=False)
app.MainLoop()
#def main():
    #app = App(redirect=False)
    #frame = Frame()
    #frame.Show()
    #app.MainLoop()

#if __name__ == '__main__':
    #main()