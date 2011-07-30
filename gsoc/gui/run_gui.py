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
import glob   #NOTE (m): http://docs.python.org/release/2.4.4/lib/module-glob.html
import urllib #NOTE (m): http://docs.python.org/release/2.4.4/lib/module-urllib.html

# Clear Climate Code
from CCCgistemp.tool import run
from CCCgistemp.tool.vischeck import anom, annual_anomalies, asgooglechartURL
from CCCgistemp.code.read_config import generate_defaults
import gui.lib.packaging as pkg
# http://bazaar.launchpad.net/~stani/phatch/trunk/view/head:/phatch/lib/
from gui.lib import notify  # NOTE (m): Need to add the license somewhere.

# Constants
WIDHT, HEIGHT = 920, 600
header_w, header_h = 900, 150

# Get approot directory.
setup = pkg.get_setup()
if setup == 'source':
    approot = os.path.dirname(__file__)  # not frozen
    print("source")  # NOTE (c): removeme
elif setup == 'py2exe':
    approot = os.path.dirname(unicode(sys.executable,
                                      sys.getfilesystemencoding( )))
    print("py2exe")  # NOTE (c): removeme
elif setup == 'py2app':
    approot = os.environ['RESOURCEPATH']
    print("py2app")  # NOTE (c): removeme
elif setup == 'package':
    print("packaged")  # NOTE (c): removeme
    pass  # linux

# Allow to be called from relative, local, or full path.
if not approot:
    approot = os.path.join(os.getcwd())
elif approot == 'gui':
    approot = os.path.join(os.getcwd(), os.path.basename(approot))

# Icons and figures directory.
if setup == 'source':
    approot = os.path.join(approot, 'resources')

header_file = os.path.join(approot, 'ccf-header.png')
ico = os.path.join(approot, 'ccf.ico')
splash = os.path.join(approot, 'splash.png')


# Frame class
class Frame(wx.Frame):
    """Main GUI window."""
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

        # Header (also a button to the source code).
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

        # Status bar. NOTE (c): FIXME statusbar
        #if 0: status = self.CreateStatusBar()

        # Menu bar.
        menubar = wx.MenuBar()

        first = wx.Menu()
        second = wx.Menu()

        open_proj = first.Append(wx.NewId(), '&Open Project directory...')
        crea_proj = first.Append(wx.NewId(), '&Create Project directory...')

        first.AppendSeparator()
        first.Append(wx.ID_EXIT, "E&xit", "Terminate the program")

        help_proj = second.Append(wx.NewId(), 'Help')
        dwl_info = second.Append(wx.NewId(), '&Download info')
        about = second.Append(wx.ID_ABOUT,
                              "&About",
                              "More information about this program")

        menubar.Append(first, '&File')
        menubar.Append(second, '&Help')

        self.SetMenuBar(menubar)

        #wx.EVT_MENU(self, wx.ID_ABOUT, self.OnAbout) #NOTE (m): remove
        wx.EVT_MENU(self, wx.ID_EXIT,  self.OnClose)
        wx.EVT_MENU(self, wx.ID_ABOUT,  self.OnAbout)
        wx.EVT_MENU(self, open_proj.GetId(),  self.onDir)
        wx.EVT_MENU(self, dwl_info.GetId(),  self.onDownloadInfo)
        # TODO: For now it is the same as open_proj, since a new
        # project is just a new directory with the config directory. However,
        # if we ever create a more sophisticated project management scheme this
        # must be improved. Also, a validated_open_prj() should be created
        # to check the results of a previuos run.
        wx.EVT_MENU(self, crea_proj.GetId(),  self.onDir)

        # Gauge. NOTE (c): Not used, fix.
        if:0 self.timer = wx.Timer(self, 1)
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
        stp6_button = wx.Button(self.panel, id=6, label="Show result",
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
        stp6_button.Bind(wx.EVT_BUTTON, self.OnShow)
        close_button.Bind(wx.EVT_BUTTON, self.OnClose)

        self.panel.Layout()

        self.WORK_DIR = False  # Constant to check for working directory.

    # GUI events:
    def webSource(self, event):
        """Open link for the source code."""
        url = 'http://code.google.com/p/ccc-gistemp/'
        webbrowser.open(url)

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
            #process = wx.Process() NOTE (c): remove
            #pid = wx.Execute(run.main(), wx.EXEC_ASYNC, process) NOTE (c): remove
            run.main()
            notify.send(title='ccc-gistemp',
                        message='Finished ccc-gistemp run',
                        icon=ico)

    def OnShow(self, event):
        """"Show google chart url."""
        if self.check_dir():
            res_files = glob.glob(os.path.join(self.CURR_DIR, 'result', '*.txt'))
            res_list = [os.path.basename(l) for l in res_files]

            box = wx.SingleChoiceDialog(parent=None,
                                        message="List of result",
                                        caption="Choose a result file",
                                        choices=res_list)
            if box.ShowModal() == wx.ID_OK:
                answer = box.GetStringSelection()
                idx = res_list.index(answer)
                answer = res_files[idx]
            box.Destroy()
            try:
                # TODO: Maybe I should revisit vischeck with David...
                url = asgooglechartURL(map(anom, map(urllib.urlopen,
                                       [answer])), options={})
                webbrowser.open(url.strip())
            except IOError:
                print("Could not open result/google-chart.url")

    def RunCCCgistemp_steps(self, event):
        """Run steps."""
        step = str(event.GetId())  # FIXME: Dangerous use of id.
                              # TODO: Add a check for each step.

        self.onStepInfo(step)

        if self.check_dir():
            notify.send(title='ccc-gistemp',
                        message=('running ccc-gistemp step %s' % step),
                        icon=ico)
            #process = wx.Process() NOTE (c): remove
            #pid = wx.Execute(run.main(argv=['dummy', '-s', step]), NOTE (c): remove
                             #wx.EXEC_ASYNC, process) NOTE (c): remove
            run.main(argv=['dummy', '-s', step])
            notify.send(title='ccc-gistemp',
                        message=('Finished ccc-gistemp step %s' % step),
                        icon=ico)

    def onDir(self, event):
        """Button to change/create project directory."""
        self.WORK_DIR = self.proj_dir()
        return self.WORK_DIR

    def onDownloadInfo(self, event):
        """Show information regarding the downloaded files."""
        msg = open(os.path.join(approot, 'GUI-help-input-files.txt'))
        self.showMessageDlg(msg.read(), "Download information",
                            wx.OK | wx.ICON_INFORMATION)
        msg.close()

    def OnAbout(self, event):
        """Show about text."""
        msg = open(os.path.join(approot, 'GUI-about.txt'))
        self.showMessageDlg(msg.read(), "About",
                            wx.OK | wx.ICON_INFORMATION)
        msg.close()

    # Class methods:
    def showMessageDlg(self, msg, title, style):
        """Wrapper for dialog messages."""
        dlg = wx.MessageDialog(parent=None, message=msg,
                               caption=title, style=style)
        answer = dlg.ShowModal()
        dlg.Destroy()
        return answer

    def onStepInfo(self, step):
        """Show information regarding the step process."""
        text = 'GUI-step'+step+'.txt'
        with open(os.path.join(approot, text)) as msg:
            self.showMessageDlg(msg.read(), "Step information.",
                                wx.OK | wx.ICON_INFORMATION)

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

    def deploy_config(self):
        """Add config directory if it does not exists.
        TODO: Open a text editor so the user can modify these.
        """
        if self.WORK_DIR:
            config_hk = generate_defaults()
            if config_hk['directory']:
                print("\nCreated config directory.")
            if config_hk['step1_adjust']:
                print("\nCreated step1_adjust config file.")
            if config_hk['Ts.strange.RSU.list.IN']:
                print("\nCreated Ts.strange.RSU.list.IN config file.")

    def proj_dir(self):
        """Create a project directory and change to it."""
        dlg = wx.DirDialog(self,
                           message="Choose/Create project a directory:",
                           style=wx.DD_NEW_DIR_BUTTON | wx.DD_CHANGE_DIR)

        if dlg.ShowModal() == wx.ID_OK:
            self.CURR_DIR = dlg.GetPath()
            print("Created project directory at:\n\t%s" % self.CURR_DIR)
            self.WORK_DIR = True
            self.deploy_config()
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

# NOTE (c): I do not know why the splash screen does not work when using main()
app = App(redirect=False)
app.MainLoop()
#def main():
    #app = App(redirect=False)
    #frame = Frame()
    #frame.Show()
    #app.MainLoop()

#if __name__ == '__main__':
    #main()
