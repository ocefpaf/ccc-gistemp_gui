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
# http://docs.python.org/release/2.4.4/lib/module-webbrowser.html
import webbrowser
# Clear Climate Code
from CCCgistemp.tool import run
import gui.lib.packaging as pkg
# http://bazaar.launchpad.net/~stani/phatch/trunk/view/head:/phatch/lib/
from gui.lib import notify  # TODO: need to add the license

# Constants
WIDHT, HEIGHT = 920, 600
header_w, header_h = 900, 150


# Get approot directory.
setup = pkg.get_setup()
if setup == 'source':
    approot = os.path.dirname(__file__)  # not frozen
elif setup in ('dll', 'console_exe', 'windows_exe'):
    approot = os.path.dirname(sys.executable)  # py2exe
    # TODO: Might be necessary for weird directory names.
    #approot = os.path.dirname(
        #unicode(sys.executable, sys.getfilesystemencoding()))
elif setup in ('macosx_app',):
    approot = os.environ['RESOURCEPATH']  # py2app
elif get_setup() == 'package':
    pass  # linux

# All to be called from relative, local, or full path.
approot = os.path.join(os.getcwd(), os.path.basename(approot))

# Icons and figures directory
header_file = os.path.join(approot, 'resources/ccf-header.png')
ico = os.path.join(approot, 'resources/ccf.ico')
splash = os.path.join(approot, 'resources/splash.png')


# Frame class
class Frame(wx.Frame):
    """GUI window"""
    def __init__(self, parent=None, id=-1):
        wx.Frame.__init__(self, parent, id=-1, title='ccc-gistemp',
                          size=(WIDHT, HEIGHT), pos=wx.DefaultPosition)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # Top left icon.
        icon = wx.Icon(name=ico, type=wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # Main panel.
        self.panel = wx.Panel(self, size=(WIDHT, HEIGHT))
        self.panel.SetBackgroundColour(wx.WHITE)

        # Header (actually a button to the source code).
        pic = wx.Image(name=header_file, type=wx.BITMAP_TYPE_PNG)
        pic = pic.ConvertToBitmap()
        self.btn_source = wx.BitmapButton(parent=self.panel, id=-1,
                                          bitmap=pic,
                                          pos=(0, 0),
                                          style=wx.NO_BORDER)
        self.btn_source.Bind(wx.EVT_BUTTON, self.webSource)

        # Text box.
        log = wx.TextCtrl(self.panel, wx.ID_ANY,
                          size=(WIDHT - 2 * 90, HEIGHT - header_h - 55),
                          pos=(90, header_h + 10),
                          style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

        # Status bar.
        #status = self.CreateStatusBar()

        # Menu bar.
        menubar = wx.MenuBar()
        first = wx.Menu()
        second = wx.Menu()
        open_create = first.Append(wx.NewId(), '&Open Project directory...')
        first.Append(wx.NewId(), '&Create Project directory...')
        first.AppendSeparator()
        first.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
        second.Append(wx.NewId(), 'Help')
        second.Append(wx.ID_ABOUT, "&About",
                                   "More information about this program")
        menubar.Append(first, 'File')
        menubar.Append(second, 'Help')
        self.SetMenuBar(menubar)

        #wx.EVT_MENU(self, wx.ID_ABOUT, self.OnAbout)
        wx.EVT_MENU(self, wx.ID_EXIT,  self.OnClose)
        wx.EVT_MENU(self, open_create.GetId(),  self.onDir)

        # Gauge.
        self.timer = wx.Timer(self, 1)
        self.count = 0
        #self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

        self.gauge = wx.Gauge(parent=self.panel, id=-1, range=50,
                              size=(WIDHT - 2 * 90, 20), pos=(90, HEIGHT - 45))

        # Redirect text here.
        sys.stderr = RedirectText(log)
        sys.stdout = RedirectText(log)

        # Buttons.
        offset = 30
        run_button = wx.Button(self.panel, label='Run',
                               pos=(0, header_h + offset))
        stp0_button = wx.Button(self.panel, id=0, label="Step 0",
                                pos=(0, header_h + 3 * offset))
        stp1_button = wx.Button(self.panel, id=1, label="Step 1",
                                pos=(0, header_h + 4 * offset))
        stp2_button = wx.Button(self.panel, id=2, label="Step 2",
                                pos=(0, header_h + 5 * offset))
        stp3_button = wx.Button(self.panel, id=3, label="Step 3",
                                pos=(0, header_h + 6 * offset))
        stp4_button = wx.Button(self.panel, id=4, label="Step 4",
                                pos=(0, header_h + 7 * offset))
        stp5_button = wx.Button(self.panel, id=5, label="Step 5",
                                pos=(0, header_h + 8 * offset))
        stp6_button = wx.Button(self.panel, id=6, label="Step 6",
                                pos=(0, header_h + 9 * offset))
        close_button = wx.Button(self.panel, wx.ID_CLOSE, label="Exit",
                                 pos=(0, header_h + 11 * offset))

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

        self.panel.Layout()

        self.WORK_DIR = False  # constant to check for working directory.

    # Events:
    def webSource(self, event):
        """Open link for the source code."""
        url = 'http://code.google.com/p/ccc-gistemp/'
        webbrowser.open(url)

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
        self.count = self.count + 1
        self.gauge.SetValue(self.count)
        if self.count == 50:
            self.timer.Stop()
            self.text.SetLabel("Task Completed")

    def OnClose(self, event):
        """Close confirmation."""
        dlg = wx.MessageDialog(self,
                               "Do you want to close the application?",
                               "Confirm Exit",
                               wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            wx.CallAfter(self.Destroy())

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
        step = event.GetId()  # FIXME: Dangerous use of id.
                              # TODO: Add a check for each step.
        if self.check_dir():
            notify.send(title='ccc-gistemp',
                        message=('running ccc-gistemp step %s' % step),
                        icon=ico)
            run.main(argv=['dummy', '-s', str(step)])
            notify.send(title='ccc-gistemp',
                        message=('Finished ccc-gistemp step %s' % step),
                        icon=ico)

    def onDir(self, event):
        """ Button to change/create project directory."""
        self.WORK_DIR = self.proj_dir()
        return self.WORK_DIR

    # Methods:
    def showMessageDlg(self, msg, title, style):
        """Wrapper for dialog messages."""
        dlg = wx.MessageDialog(parent=None, message=msg,
                               caption=title, style=style)
        answer = dlg.ShowModal()
        dlg.Destroy()
        return answer

    def check_dir(self):
        """Check if in a working directory.
        If not create one and change to it.
        """
        if not self.WORK_DIR:
            self.showMessageDlg("Choose or create a project directory",
                                "Information", wx.OK | wx.ICON_INFORMATION)
            self.WORK_DIR = self.proj_dir()
            return self.WORK_DIR
        else:
            return self.WORK_DIR

    def proj_dir(self):
        """Create a project directory and change to it."""
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE | wx.DD_CHANGE_DIR)

        if dlg.ShowModal() == wx.ID_OK:
            print "project directory:\n\t%s" % dlg.GetPath()
            self.WORK_DIR = True
        else:
            self.WORK_DIR = False

        dlg.Destroy()
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
        splashDuration = 1000  # milliseconds
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


# Application class.
class App(wx.App):
    """Application class."""
    def OnInit(self):
        MySplash = MySplashScreen()
        MySplash.Show()
        return True

# NOTE: I do not know why the splash screen does not work when using main()
app = App(redirect=False)
app.MainLoop()
#def main():
    #app = App(redirect=False)
    #frame = Frame()
    #frame.Show()
    #app.MainLoop()

#if __name__ == '__main__':
    #main()
